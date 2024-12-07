#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Filename: sdk.py
* Description:
* Time: 2020.11.25
* Author: liuf5
*/
"""

import getpass
import os

import requests

import graphviz  # Attention!

fields_tables_host = {
    "ip": "ip",
    "app": "portinfo.app",
    "version": "portinfo.version",
    "device": "portinfo.device",
    "port": "portinfo.port",
    "city": "geoinfo.city.names.en",
    "country": "geoinfo.country.names.en",
    "service": "portinfo.service",
    "asn": "asn",
    "banner": "portinfo.banner",
    "time": "timestamp",
    "ssl": "ssl"
}

fields_tables_web = {
    "ip": "ip",
    "app": "webapp",
    "headers": "headers",
    "keywords": "keywords",
    "title": "title",
    "site": "site",
    "city": "geoinfo.city.names.en",
    "country": "geoinfo.country.names.en",
    "webapp": "webapp",
    "component": "component",
    "framework": "framework",
    "server": "server",
    "waf": "waf",
    "os": "os",
    "timestamp": "timestamp"
}


class ZoomEyeDict:

    def __init__(self, data):
        self.dict = dict(data)

    def find(self, key):
        """
        get the value in the nested dictionary by <"key1.key2.key3">
        :param key: str, dictionary key like: "a.b.c"
        :return:
        """
        values = None
        # is dict?
        if isinstance(self.dict, dict):
            keys = key.split(".")
            inputData = self.dict
            for k in keys:
                if k == 'geoinfo' and inputData.get(k) == None:
                    k = "aiweninfo" if inputData.get("aiweninfo") else "ipipinfo"
                if inputData.get(k) is not None:
                    values = inputData.get(k)
                else:
                    values = None
                if isinstance(values, list):
                    if len(values) != 0:
                        values = values[0]
                    else:
                        values = '[unknown]'
                inputData = values
            return values
        else:
            raise TypeError("the parameter you pass in must be a dictionary, not a {}".format(type(self.dict)))


class ZoomEye:

    def __init__(self, api_key=""):
        self.api_key = api_key

        self.raw_data = None
        # process data, list
        self.data_list = None
        self.total = None
        self.search_type = None
        self.facet_data = None

        self.login_api = "https://api.zoomeye.hk/user/login"
        self.search_api = "https://api.zoomeye.hk/{}/search"
        self.user_info_api = "https://api.zoomeye.hk/resources-info"
        self.history_api = "https://api.zoomeye.hk/both/search?history=true&ip={}"

    def _request(self, url, params=None, headers=None, method='GET'):
        """
        encapsulate the requests part
        :param url: send request url
        :param params: request params
        :param headers: request header
        :param method: send request method， only support method GET and POST
        :return: json data
        """
        # if method is "GET" use requests.get
        if method == "GET":
            resp = requests.get(url, params=params, headers=headers)
        # request method is "POST"
        else:
            resp = requests.post(url, data=params, headers=headers)
            print(resp.text)
        # if response succeed and status code is 200 return json data
        if resp and resp.status_code == 200:
            data = resp.json()
            return data
        # Request data exceeds the total amount of ZoomEye data,
        # return all data instead of throwing an exception
        elif resp.status_code == 403 and 'specified resource' in resp.text:
            return None
        # if response succeed and status code is not 200 return error format json
        # others error return unknown error
        else:
            raise ValueError(resp.json().get('message'))

    def _check_header(self):
        """
        2023-04 remove username & password authenticate
        only support API-KEY authenticate
        """
        if self.api_key:
            headers = {
                'API-KEY': self.api_key,
            }
        else:
            headers = {}
        # add user agent
        headers[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        return headers

    def dork_search(self, dork, page=0, resource="host", facets=None):
        """
        Search records with ZoomEye dorks.
        param: dork
               ex: country:cn
               access https://www.zoomeye.hk/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """

        zoomresult = []
        self.search_type = resource
        search_api = self.search_api.format(resource)
        if isinstance(facets, (tuple, list)):
            facets = ','.join(facets)
        headers = self._check_header()
        params = {'query': dork, 'page': page, 'facets': facets}
        resp = self._request(search_api, params=params, headers=headers)
        if resp and "matches" in resp:
            matches = resp.get('matches')
            zoomresult = matches
            self.raw_data = resp
            self.data_list = matches
            self.facet_data = resp.get("facets")
            self.total = resp.get("total")

        return zoomresult

    def multi_page_search(self, dork, page=1, start_page=1, resource="host",
                          facets=None) -> (list, int, str):
        """
        mainly used to search dork data from zoomeyehk data.
        please see: https://www.zoomeye.hk/doc#host-search and
                    https://www.zoomeye.hk/doc#web-search
        :param dork:str,
                    ex:apache:cn
                    dork to search
        :param page: int,
                    specify the number of pages to return data, each page contains 20 data
        :param start_page: int,
                    specify the number of start page to search
        :param resource: str,
                        host search or web search
        :param facets: list or tuple
                     if this parameter is specified,
                     the corresponding data will be displayed
                     at the end of the returned result.
                     supported :'app', 'device', 'service', 'os', 'port', 'country', 'city'
                     tips:the data returned by the app is contained in the product
                        other data are corresponding
        :return: json data
        """
        self.search_type = resource
        search_api = self.search_api.format(resource)

        headers = self._check_header()

        dork_data = []
        all_data = []
        is_search_done = "done"
        for i in range(start_page - 1, page):
            print("downloading contents from page{}".format(i+1))
            if isinstance(facets, (tuple, list)):
                facets = ','.join(facets)

            params = {'query': dork, 'page': i + 1, 'facets': facets}
            try:
                result = self._request(search_api, params=params, headers=headers)
            except Exception as e:
                # return the processed data
                self.data_list = dork_data
                self.raw_data = all_data
                return dork_data, i, "search failed, the log as {}".format(e)
            if result and "matches" in result:
                self.total = result.get("total")
                all_data.append(result)
                for j in result.get("matches"):
                    # get every piece of data
                    dork_data.append(j)
                if facets:
                    # facets field exist, get it.
                    self.facet_data = result.get("facets")

        # dork_data is the processed data and returns a list.
        # nested dictionaries in the list.
        self.data_list = dork_data
        # all_data is the raw data returned by the api.
        # since the api is returned by a dictionary,
        # i added it to a list for easy viewing of each piece of data
        self.raw_data = all_data
        # return processed data
        return dork_data, page, is_search_done

    def resources_info(self) -> dict:
        """
        account resource information, resource limit and package type
        see: https://www.zoomeye.hk/doc#resources-info
        :return: dict
        """
        headers = self._check_header()
        result = self._request(self.user_info_api, headers=headers)
        return result

    def show_count(self):
        """
        display the total amount of dork data currently searched
        :return: int
        """
        return self.total

    def dork_filter(self, keys):
        """
        display data based on input fields
        supported fields:
            host: "app","version","device","ip"","port","hostname","city","country","asn","banner"
            web: "app","headers","keywords","title","ip","site","city","country"
        :param keys: str
        :return:
        """
        result = []
        if self.search_type == "host":
            fields_table = fields_tables_host
        elif self.search_type == "web":
            fields_table = fields_tables_web
        else:
            raise TypeError("the search type must be one of host and web,not {}".format(self.search_type))
        keys = keys.split(",")
        for i in self.data_list:
            item = []
            zmdict = ZoomEyeDict(i)
            for key in keys:
                res = zmdict.find(fields_table.get(key.strip()))
                item.append(res)
            result.append(item)
        return result

    def get_facet(self):
        """
        input facets can return the content of facets through this function
        :return: dict, facets data
        """
        return self.facet_data

    def history_ip(self, ip):
        """
        Query IP History Information.
        see: https://www.zoomeye.hk/doc#history-data
        param: ip
        """
        result = {}

        zoomeye_api = self.history_api.format(ip)
        headers = self._check_header()
        resp = self._request(zoomeye_api, headers=headers)
        if resp and 'data' in resp:
            result = resp
        return result

    def domain_search(self, q, source=0, page=1) -> list:
        """
        Search records with ZoomEye dorks.
        Args:
            q: query content
            source: Search type 0, 1
            page: want to view page

        Returns:
                list
        """
        search_api = self.search_api.format('domain')
        headers = self._check_header()
        request_result = self._request(search_api, params={"q": q, "type": source, "page": page}, headers=headers)
        if request_result:
            self.raw_data = request_result  # json字符串
            self.data_list = request_result.get("list", [])
            self.total = request_result.get("total", 0)

        return [self.data_list, self.total]

    def generate_dot(self, q, source=0, page=1):
        """

        """
        error_info = ''
        search_api = self.search_api.format('domain')
        headers = self._check_header()
        try:
            request_result = self._request(search_api, params={"q": q, "type": source, "page": page}, headers=headers)
        except Exception as e:
            error_info = e
            request_result = None
        if not request_result:
            return False, error_info
        # the request data is successful, and the domain name network map is generated.
        domain = q.replace('.', '_')
        grap_obj = graphviz.Digraph(
            name=domain,
            filename='{}.gv'.format(domain),
            engine='sfdp',
            format='png',
        )
        result = {}
        for item in request_result.get('list'):
            if len(item.get('ip')) != 0:
                for ip in item.get('ip'):
                    result[ip] = item.get('name')

        for ip, name in result.items():
            grap_obj.edge(name, ip)

        try:
            grap_obj.render()
        except Exception as e:
            return False, e
        return True, "successful! saving in {}".format(os.getcwd())


def show_site_ip(data):
    """
    show web search
    :param data: dict, matches data from api
    :return:
    """
    if data:
        for i in data:
            print(i.get('site'), i.get('ip'))


def show_ip_port(data):
    """
    show host search ip and port
    :param data: dict, matches data from api
    :return:
    """
    if data:
        for i in data:
            print(i.get('ip'), i.get('portinfo').get('port'))


def zoomeye_api_test():
    zoomeye = ZoomEye()
    zoomeye.api_key = input('ZoomEye API-KEY:')
    print(zoomeye.resources_info())

    data = zoomeye.dork_search('solr')
    show_ip_port(data)

    data = zoomeye.dork_search('country:cn')
    show_ip_port(data)

    data = zoomeye.dork_search('solr country:cn')
    show_ip_port(data)

    data = zoomeye.dork_search('solr country:cn', resource='web')
    show_site_ip(data)


if __name__ == "__main__":
    zoomeye_api_test()
