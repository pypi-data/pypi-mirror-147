#
import ast
import io
import json
import os
import time
import uuid
from datetime import datetime, timedelta
from math import nan
from typing import List, Union
from urllib.parse import parse_qs, urlparse

import ipywidgets as widgets
import markdown
import numpy as np
import pandas as pd
import pkg_resources
import requests
from dateutil.parser import parse
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from ipywidgets import HTML
from requests.structures import CaseInsensitiveDict
from typeguard import typechecked
from urllib3.exceptions import HTTPError

from . import __version__
from .access import delete_jwt, get_previous_jwt, restore_previous_jwt, save_jwt, AUTH_ENDPOINT
from .queries import *
from .util import HubException, hub_authenticated, timer

# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HUB_BASE_URL = "https://data.academic.osisoft.com"
REGISTRATION_URL = "https://academic.osisoft.com/register"
GRAPHQL_ENDPOINT = "https://academichub-gw.azurewebsites.net/graphql"

MAX_STORED_DV_ROWS = 2000000
UXIE_CONSTANT = 100 * 1000

hub_db_namespaces = CaseInsensitiveDict({})

ocstype2hub = {
    "PI-Digital": "Category",
    "PI-String": "String",
    "PI-Timestamp": "Timestamp",
    "PI-Int16": "Integer",
    "PI-Int32": "Integer",
}

resource_package = __name__
resource_path = "/".join((".", "hub_datasets.json"))
default_hub_data = pkg_resources.resource_filename(resource_package, resource_path)

stream_queries = {
    "streams": q_streams,
    "stream": q_stream,
    "data": q_stream_data,
    "ends": q_stream_ends,
    "interpolated": q_stream_interpolated,
}


def asset_id_fix(gqlh):
    for i, database in enumerate(gqlh["Database"]):
        for j, asset in enumerate(database["asset_with_dv"]):
            if asset.get("asset_id", None) is None:
                asset["asset_id"] = asset["name"]
            else:
                asset["name"] = asset["asset_id"]
    return gqlh


def initialize_hub_data(data_file):
    global hub_db_namespaces
    with open(data_file) as f:
        gqlh = json.loads(f.read())
    db_index = CaseInsensitiveDict({})
    hub_db_namespaces.clear()
    for i, database in enumerate(gqlh["Database"]):
        db_index[database["asset_db"]] = i
        hub_db_namespaces[database["name"]] = database["namespace"]
    return asset_id_fix(gqlh), gqlh["Database"][0]["asset_db"], db_index


def assets_and_metadata(gqlh, db_index, current_db):
    assets_info = gqlh["Database"][db_index[current_db]]["asset_with_dv"]
    asset_key = "name"
    assets = sorted([i[asset_key].lower() for i in assets_info])
    dv_column_key = {}
    for i in assets_info:
        for dv in i["has_dataview"]:
            dv_column_key[dv["id"]] = dv.get("ocs_column_key", None)

    def metaf(x):
        return {} if x is None else eval(x)

    metadata = {
        assets_info[j][asset_key]: metaf(assets_info[j]["asset_metadata"])
        for j in range(len(assets_info))
    }
    for key in metadata.keys():
        d = metadata[key]
        d.update({"Asset_Id": key})
    return assets, metadata, dv_column_key


class GraphQLException(Exception):
    pass


def process_digital_states(df):
    ds_columns = [col for col in list(df.columns) if col[-4:] == "__ds"]
    if len(ds_columns) > 0:
        for ds_col in ds_columns:
            val_col = ds_col[:-4]
            index = df[val_col].index[df[val_col].apply(np.isnan)]
            df.loc[index, [ds_col]] = ""
        df = df.drop(columns=[ds_col[:-4] for ds_col in ds_columns])
        df = df.rename(columns={ds_col: ds_col[:-4] for ds_col in ds_columns})
    return df


def remap_campus_dataview_id(dv_id):
    if "campus.building-" in dv_id:
        if not any(ss in dv_id for ss in ["-electricity", "-chilled_water", "-steam"]):
            return dv_id + "-electricity"
    return dv_id


def asdict(item_metadata):
    return {i["Name"]: i["Value"] for i in item_metadata}


class HubClient:
    @typechecked
    def __init__(
        self,
        hub_data: str = "hub_datasets.json",
        options: List[str] = [],
        debug: bool = False,
    ):
        self.__authenticated = False
        self.__jwt = {"access_token": "none"}
        self.__session_id = str(uuid.uuid4())
        self.__graphql_transport = None
        self.__graphql_client = None

        self.__options = options
        self.__debug = debug
        data_file = hub_data if os.path.isfile(hub_data) else default_hub_data
        self.__default_data = data_file == default_hub_data
        if debug and self.__default_data:
            print(f"@ Hub data file: {data_file}")
        self.__gqlh, self.__current_db, self.__db_index = initialize_hub_data(data_file)
        self.__current_db_index = 0
        (
            self.__assets,
            self.__assets_metadata,
            self.__dv_column_key,
        ) = assets_and_metadata(self.__gqlh, self.__db_index, self.__current_db)
        self.__dataview_next_page = None

    @typechecked
    def session_id(self) -> str:
        return self.__session_id

    @typechecked
    def get_jwt(self) -> dict:
        return self.__jwt

    @typechecked
    def set_jwt(self, jwt: dict, gw_url):
        self.__jwt = jwt.copy()
        self.__graphql_transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT if gw_url is None else gw_url,
            use_json=True,
            headers={"Authorization": f"Bearer {self._id_token()}"},
            verify=False,
            retries=3,
        )
        self.__graphql_client = Client(
            transport=self.__graphql_transport, fetch_schema_from_transport=False
        )

    @typechecked
    def _id_token(self) -> str:
        token = self.__jwt.get("id_token", None)
        if token is None:
            raise HubException("@@@ Please (re)start Hub login sequence")
        return token

    @typechecked
    def set_authenticated(self) -> None:
        self.__authenticated = True

    @typechecked
    def authenticated(self) -> bool:
        return self.__authenticated

    @typechecked
    def default_data(self) -> bool:
        return self.__default_data

    def gqlh(self):
        return self.__gqlh

    @hub_authenticated
    @typechecked
    def asset_metadata(self, asset: str):
        if asset.lower() not in self.__assets:
            raise HubException(
                f"@@ error: asset {asset} not in dataset asset list, check hub.assets()"
            )

        return self.__assets_metadata[asset]

    def all_assets_metadata(self):
        metadata = [
            self.__assets_metadata[key] for key in self.__assets_metadata.keys()
        ]
        return pd.DataFrame(metadata).sort_values(by=["Asset_Id"])

    @hub_authenticated
    @typechecked
    def datasets(self, first="") -> List[str]:
        data_sets = list(hub_db_namespaces.keys())
        data_sets.sort(key=lambda s: s == first, reverse=True)
        return data_sets

    @hub_authenticated
    @typechecked
    def current_dataset(self) -> str:
        return self.__gqlh["Database"][self.__current_db_index]["name"]

    @typechecked
    def dataset_version(self) -> str:
        version = self.__gqlh["Database"][self.__current_db_index].get(
            "version", "not available"
        )
        status = self.__gqlh["Database"][self.__current_db_index].get(
            "status", "-not set-"
        )
        return f"{version} (status: {status})"

    @hub_authenticated
    def set_dataset(self, dataset: str):
        if not isinstance(dataset, str):
            raise HubException(
                f"@@ Dataset most be a string, please check hub.datasets()"
            )
        if hub_db_namespaces.get(dataset, None) is None:
            raise HubException(
                f"@@ Dataset {dataset} does not exist, please check hub.datasets()"
            )

        for j in range(len(self.__gqlh["Database"])):
            if self.__gqlh["Database"][j]["name"] == dataset:
                self.__current_db_index = j
                self.__current_db = self.__gqlh["Database"][j]["asset_db"]
                (
                    self.__assets,
                    self.__assets_metadata,
                    self.__dv_column_key,
                ) = assets_and_metadata(self.__gqlh, self.__db_index, self.__current_db)
                break

    @hub_authenticated
    def namespace_of(self, dataset: str):
        if not isinstance(dataset, str):
            raise HubException(
                f"@@ Dataset most be a string, please check hub.datasets()"
            )
        if hub_db_namespaces.get(dataset, None) is None:
            raise HubException(
                f"@@ Dataset {dataset} does not exist, please check hub.datasets()"
            )
        return hub_db_namespaces[dataset]

    @hub_authenticated
    @typechecked
    def assets(self, filter: str = ""):
        df = pd.DataFrame(columns=("Asset_Id", "Description"))
        asset_description = {
            i["name"]: i["description"]
            for i in self.__gqlh["Database"][self.__db_index[self.__current_db]][
                "asset_with_dv"
            ]
            if filter.lower() in i["name"].lower()
        }
        sorted_assets = sorted(list(asset_description.keys()))
        for i, asset in enumerate(sorted_assets):
            df.loc[i] = [asset, asset_description[asset]]
        return df

    @hub_authenticated
    @typechecked
    def asset_dataviews(
        self, filter: str = "default", asset: str = "", multiple_asset: bool = False
    ) -> Union[None, List[str]]:
        if len(asset) > 0:
            if asset.lower() not in self.__assets:
                raise HubException(
                    f"@@ error: asset {asset} not in dataset asset list, check hub.assets()"
                )

        if not multiple_asset:

            def len_test(li):
                return len(li) == 1

        else:

            def len_test(li):
                return len(li) > 1

        if asset == "":

            def asset_test(_x, _y):
                return True

        else:

            def asset_test(this_asset, asset_list):
                return this_asset.lower() in [i.lower() for i in asset_list]

        dataviews = []
        for j in self.__gqlh["Database"][self.__db_index[self.__current_db]][
            "asset_with_dv"
        ]:
            if len(asset) > 0 and j["name"].lower() == asset.lower():
                dataviews = j["has_dataview"]
                break
            else:
                dataviews.extend(j["has_dataview"])

        return sorted(
            list(
                set(
                    [
                        i["id"]
                        for i in dataviews
                        if (
                            filter.lower() in i["id"]
                            or filter.lower() in i["description"].lower()
                        )
                        and asset_test(asset, i["asset_id"])
                        and len_test(i["asset_id"])
                    ]
                )
            )
        )

    @hub_authenticated
    @typechecked
    def dataview_definition(
        self, namespace_id: str, dataview_id: str, stream_id: bool = False
    ):
        columns = [
            "Asset_Id",
            "Column_Name",
            "Stream_Type",
            "Stream_UOM",
            "Stream_Name",
        ]
        if stream_id:
            columns += ["Stream_Id"]
        df = pd.DataFrame(columns=columns)

        data_items = self.graphql_query(
            q_resolved,
            {"id": dataview_id, "namespace": namespace_id, "queryId": "Asset_value"},
        )
        if len(data_items["dataview"]) == 0:
            raise HubException(
                f"@@ Bad namespace ({namespace_id}) and/or dataview ID ({dataview_id})"
            )
        v2_column_key = self.__dv_column_key.get(dataview_id, None)
        column_key = (
            "column_name" if v2_column_key is None else f"{v2_column_key}|column"
        )
        items = data_items["dataview"][0]["resolvedDataItems"]["Items"]
        for i, item in enumerate(items):
            item_meta = CaseInsensitiveDict(asdict(item["Metadata"]))
            column_values = [
                item_meta["asset_id"],
                item_meta[column_key],
                ocstype2hub.get(item["TypeId"], "Float"),
                item_meta.get("engunits", "-n/a-").replace("Â", ""),
                item["Name"],
            ]
            if stream_id:
                column_values += [item["Id"]]
            df.loc[i] = column_values
        return df.sort_values(["Column_Name", "Asset_Id"])

    def dataview_columns(self, namespace_id: str, dataview_id: str):
        data_items = self.graphql_query(
            q_resolved,
            {"id": dataview_id, "namespace": namespace_id, "queryId": "Asset_value"},
        )
        digital_items = self.graphql_query(
            q_resolved,
            {"id": dataview_id, "namespace": namespace_id, "queryId": "Asset_digital"},
        )
        return (
            len(data_items["dataview"][0]["resolvedDataItems"]["Items"])
            + len(digital_items["dataview"][0]["resolvedDataItems"]["Items"])
            + 1
        )

    def __get_data_interpolated(
        self,
        namespace_id,
        dataview_id,
        start_index,
        end_index,
        interval,
        count,
        next_page,
    ):
        # count_arg = {} if count is None else {"count": count}
        reply = self.graphql_query(
            q_interpolated,
            dict(
                namespace=namespace_id,
                id=dataview_id,
                startIndex=start_index,
                endIndex=end_index,
                interpolation=interval,
                nextPage=next_page,
                count=count,
            ),
        )
        if len(reply["dataview"]) == 0:
            print("@@ NO DATA: Check namespace_id, dataview_id and/or date range")
            return None, [], None
        result = reply["dataview"][0]["data"]
        return result["nextPage"], result["data"], result["firstPage"]

    def __get_data_stored(
        self,
        namespace_id,
        dataview_id,
        start_index,
        end_index,
        interval,  # not used
        count,
        next_page,
    ):
        # count_arg = {} if count is None else {"count": count}
        reply = self.graphql_query(
            q_stored,
            dict(
                namespace=namespace_id,
                id=dataview_id,
                startIndex=start_index,
                endIndex=end_index,
                nextPage=next_page,
                count=count,
            ),
        )
        if len(reply["dataview"]) == 0:
            print("@@ NO DATA: Check dataview_id and/or date range")
            return None, [], None
        result = reply["dataview"][0]["data"]
        return result["nextPage"], result["data"], result["firstPage"]

    @hub_authenticated
    def remaining_data(self) -> bool:
        return False if self.__dataview_next_page is None else True

    @hub_authenticated
    def reset_remaining_data(self) -> bool:
        self.__dataview_next_page = None

    @timer
    @hub_authenticated
    @typechecked
    def dataview_interpolated_pd(
        self,
        namespace_id: str,
        dataview_id: str,
        start_index: str,
        end_index: str,
        interval: str,
        count: int = 0,
        sub_second_interval: bool = False,
        verbose: bool = False,
        stored: bool = False,
    ):
        try:
            return self.dataview_get_data_pd(
                namespace_id,
                dataview_id,
                start_index,
                end_index,
                interval,
                count,
                sub_second_interval,
                verbose,
                stored,
            )
        except GraphQLException as e:
            raise e

    def dataview_get_data_pd(
        self,
        namespace_id: str,
        dataview_id: str,
        start_index: str,
        end_index: str,
        interval: str,
        count: int = 0,
        sub_second_interval: bool = False,
        verbose: bool = False,
        stored: bool = False,
        resume: bool = False,
        max_stored_rows=MAX_STORED_DV_ROWS,
    ):
        df = pd.DataFrame()
        next_page = None
        if not resume:
            if not sub_second_interval and not stored:
                try:
                    datetime.strptime(interval, "%H:%M:%S")
                except ValueError as e:
                    print(f"@Error: interval has invalid format: {e}")
                    return df
            try:
                parse(end_index)
                parse(start_index)
            except ValueError as e:
                print(f"@Error: start_index and/or end_index has invalid format: {e}")
                return df
            if verbose:
                now = datetime.now().isoformat()
                summary = f"<@dataview_interpolated_pd/{dataview_id}/{start_index}/{end_index}/{interval}  t={now}"
                print(summary)

        else:
            if not self.remaining_data():
                print(f"@Error: no remaining data for stored dataview id {dataview_id}")
                return df
            next_page = self.__dataview_next_page

        dataview_f = self.__get_data_stored if stored else self.__get_data_interpolated
        dataview_id = remap_campus_dataview_id(dataview_id)

        delay_50x = 1
        while True:
            try:
                # print(f"[{next_page}]", end="")
                next_page, csv_or_json, _ = dataview_f(
                    namespace_id=namespace_id,
                    dataview_id=dataview_id,
                    count=count,
                    start_index=start_index,
                    end_index=end_index,
                    interval=interval,
                    next_page=next_page,
                )
                # print(f"[{len(csv)}, {type(csv)}, {str(csv)}]", end="")
                if not stored:
                    df = df.append(
                        pd.read_csv(
                            io.StringIO(csv_or_json), parse_dates=["Timestamp"]
                        ),
                        ignore_index=True,
                    )
                else:
                    df = df.append(pd.read_json(json.dumps(csv_or_json)))
                    if len(df) >= max_stored_rows:
                        self.__dataview_next_page = next_page
                        print()
                        break

                if next_page is None:
                    print()
                    self.__dataview_next_page = None
                    break
                print("+", end="", flush=True)
            except HTTPError as e:
                if "502" in str(e):
                    print("@", end="")
                    continue
            except Exception as e:
                if not any(
                    ss in str(e).lower()
                    for ss in ["408", "503", "504", "409", "502", "unauthenticated"]
                ):
                    raise e
                if "unauthenticated" in str(e).lower():
                    self.__authenticated = False
                    raise GraphQLException(
                        "@@@ Please (re)start Hub login sequence (cell with hub_login() )"
                    )
                if "409" in str(e):
                    print("#", end="")
                    continue
                if "502" in str(e): #  or "504" in str(e):
                    print("[@]", end="")
                    time.sleep(delay_50x)
                    delay_50x *= 2
                    if delay_50x > 8:
                        raise e
                    continue
                if "408" not in str(e):
                    print(f"[restart-{str(e)}]", end="")
                    raise GraphQLException(f"Got: {str(e)}")

                df = pd.DataFrame()
                next_page = None
                if count == 0:
                    count = UXIE_CONSTANT // self.dataview_columns(
                        namespace_id, dataview_id
                    )
                count = count // 2
                print(f"@({count})", end="")
                if count < 40:
                    raise e

        return process_digital_states(df)

    @timer
    @hub_authenticated
    @typechecked
    def dataview_stored_pd(
        self,
        namespace_id: str,
        dataview_id: str,
        start_index: str,
        end_index: str,
        count: int = 0,
        resume: bool = False,
        max_rows=MAX_STORED_DV_ROWS,
    ):
        try:
            result = self.dataview_get_data_pd(
                namespace_id,
                dataview_id,  # + "_narrow",
                start_index,
                end_index,
                "",
                count=count,
                stored=True,
                resume=resume,
                max_stored_rows=max_rows,
            )
        except GraphQLException as e:
            raise e
        except Exception as e:
            if "404" in str(e):
                print(
                    f"### Error: data view with Id {dataview_id} has no version for stored data.\n"
                    "###  If data view id is correct, contact Hub support if stored data is required instead of "
                    "interpolated. "
                )
                return
            else:
                raise e
        return result

    def __stream_ops(self, kind, namespace, stream_id="", extra_args=None):
        q_values = dict(namespace=namespace, stream_id=stream_id)
        if extra_args:
            q_values.update(extra_args)
        try:
            reply = self.graphql_query(stream_queries[kind], q_values)
        except Exception as e:
            ed = ast.literal_eval(str(e))
            if "404:" in ed["message"] or "400:" in ed["message"]:
                raise GraphQLException(ed["extensions"]["message"]) from None
            else:
                raise e from None

        if len(reply["namespaces"]) == 0:
            raise GraphQLException(
                f"@@@ Namespace `{namespace}` not found (check hub.datasets())"
            )

        return reply

    @hub_authenticated
    @typechecked
    def get_streams(
        self, namespace: str, query: str = "", count: int = 0, skip: int = 0
    ):
        args = dict(count=2000)
        if query:
            args["query"] = query
        if count:
            args["count"] = count
        if skip:
            args["skip"] = skip
        reply = self.__stream_ops("streams", namespace, "", args)
        return reply["namespaces"][0]["streams"]

    @hub_authenticated
    @typechecked
    def get_stream(self, namespace: str, stream_id):
        reply = self.__stream_ops("stream", namespace, stream_id)["namespaces"][0]
        return reply["stream"], reply["metadata"], reply["tags"]

    @hub_authenticated
    @typechecked
    def get_stream_ends(self, namespace: str, stream_id):
        reply = self.__stream_ops("ends", namespace, stream_id)["namespaces"][0]
        return (
            parse(reply["first"]["Timestamp"]),
            reply["first"].get("Value", None),
            parse(reply["last"]["Timestamp"]),
            reply["last"].get("Value", None),
        )

    @hub_authenticated
    @typechecked
    def stream_window_pd(
        self, namespace: str, stream_id, start: str, end: str, column_name: str = ""
    ):
        reply = self.__stream_ops(
            "data", namespace, stream_id, dict(start=start, end=end)
        )
        df = pd.DataFrame(reply["namespaces"][0]["data"])
        if len(df) > 0:
            time_column = list(df.columns)[0]
            df[time_column] = pd.to_datetime(df[time_column])
            if column_name:
                df.columns = [time_column, column_name]
        return df

    @hub_authenticated
    @typechecked
    def stream_interpolated_pd(
        self,
        namespace: str,
        stream_id,
        start: str,
        end: str,
        interval: str,
        column_name: str = "",
        raw: bool = False,
    ):
        try:
            t_interval = datetime.strptime(interval, "%H:%M:%S")
            delta = t_interval - parse("1900-01-01")
            count = int((parse(end) - parse(start)) / delta) + 1
        except ValueError as e:
            raise GraphQLException(
                f"@Error: start, end or interval (HH:MM:SS) has invalid format: {e}"
            ) from None

        reply = self.__stream_ops(
            "interpolated",
            namespace,
            stream_id,
            dict(start=start, end=end, count=count),
        )
        df = pd.DataFrame(reply["namespaces"][0]["data"])
        if len(df) > 0:
            time_column = list(df.columns)[0]
            df[time_column] = pd.to_datetime(df[time_column])
            if not raw:
                df = df.drop(df.columns[2:], axis=1)
            if column_name:
                df.columns = [df.columns[0], column_name] + list(df.columns[2:])
        return df

    @hub_authenticated
    @typechecked
    def refresh_datasets(
        self,
        hub_data: str = "hub_datasets.json",
        additional_status: str = "production",
        experimental: bool = True,
    ) -> None:
        db = self.graphql_query(
            q_datasets, variable_values={"status": additional_status}
        )
        with open(hub_data, "w") as f:
            f.write(json.dumps(db, indent=2))

    def graphql_query(self, query_string, variable_values=None):
        if self.__graphql_client is None:
            raise GraphQLException(
                "@@@ Please (re)start Hub login sequence (cell with hub_login() )"
            )
        if variable_values is None:
            variable_values = {}
        query = gql(query_string)
        try:
            reply = self.__graphql_client.execute(
                query, variable_values=variable_values
            )
        except Exception as e:
            raise e
        return reply


def set_token_and_check(hub, jwt, custom_url):
    hub.set_jwt(jwt, custom_url)
    reply = hub.graphql_query(q_endpoint_check)
    if reply.get("databases", False):
        hub.set_authenticated()
        return True
    else:
        return False


def hub_connect(jwt: dict, gw_url: str = None):
    hub = HubClient()
    if set_token_and_check(hub, jwt, gw_url):
        return hub
    else:
        raise GraphQLException("@@ Got bad JWT")


def login_state(hub, jwt: dict, found_jwt: bool = False):
    status = "+" if found_jwt else ""
    status += "@" if not hub.default_data() else ""
    status += "#" if jwt.get("creds", None) else ""
    return status


def hub_login(force: bool = False, gw_url: str = None, quiet=False):
    if force:
        delete_jwt()
    hub = HubClient()
    new_tab = 'target="_blank"'
    registration_link = f'(<a {new_tab} href="{REGISTRATION_URL}"><font color="blue">register here</font></a>)'
    step1 = '<font color="purple"><b>Click here to initiate login sequence on new tab</b></font>'
    login_md = f"""![AVEVA banner](https://academichub.blob.core.windows.net/images/aveva-banner.png)<br>
    <b>Academic Hub Login {registration_link}, version {__version__}</b> 

Follow the steps below:

<ol>
  <li><b>If Login status is "OK" (at bottom of this cell), you can continue with the rest of the notebook</b></li>
  <li>Click on the purple link to open a new browser tab and:</li>
  <ol type="a">
     <li>Enter "academic-hub" when asked for the organization</li>
     <li>Select your Google account and enter your credentials</li>
     <li>When successfully logged in with AVEVA authentication web page, come back to this notebook</li>
     <li> <a {new_tab} href="{AUTH_ENDPOINT}/login?hub-id={hub.session_id()}">{step1}</a> </li>
  </ol>
  <li>Complete authentication procedure by the clicking button below</li>
</ol>
"""
    html = markdown.markdown(login_md)
    button = widgets.Button(
        description="Click me",
        disabled=False,
        button_style="warning",
        tooltip="Click me when Google login is successful",
        icon="cloud-download",
    )

    restore_previous_jwt(hub.session_id())
    time.sleep(1)
    jwt = get_previous_jwt(hub.session_id())
    login_status = "-- not logged in --"
    try:
        if set_token_and_check(hub, jwt, gw_url):
            login_status = f"OK, you can proceed {login_state(hub, jwt, True)}"
            if "#" in login_status:
                quiet = True
    except HubException:
        pass
    except Exception as e:
        if "unauthenticated" in str(e).lower():
            pass
        else:
            raise e

    status = widgets.Text(
        value=login_status,
        placeholder="Type something",
        description="Login status:",
        disabled=True,
    )

    def button_confirm(_):
        r = requests.get(
            f"{AUTH_ENDPOINT}/token?jwt=1",
            headers={"hub-id": hub.session_id()},
            verify=False,
        )
        if 200 == r.status_code:
            if set_token_and_check(hub, eval(r.text), gw_url):
                status.value = f"OK, you can proceed {login_state(hub, eval(r.text))}"
            else:
                status.value = "ERROR: Hub endpoint failed, go to Step 1"
        else:
            status.value = "ERROR: Go back to Step 1"

    button.on_click(button_confirm)
    output = widgets.Output()

    def on_value_change(change):
        with output:
            if "OK" in change["new"]:
                save_jwt(hub.get_jwt())

    status.observe(on_value_change, names="value")

    to_display = [status, output] if quiet else [HTML(html), button, status, output]
    return widgets.VBox(to_display), hub
