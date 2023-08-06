# -*- coding: utf-8 -*-
"""
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""

import requests
from requests.exceptions import (ReadTimeout, RequestException, ConnectTimeout)

from .config import GatewayConfig, ALL_ENV
from .exception import (EnvTypeExp, SetUpUriExp, SetUpRegisterExp, SetUpGatewayExp, GetRegisterTokenErr)


class GatewayProxy(object):
    """
    gateway proxy class
    """
    def __init__(self):
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        self.env = GatewayConfig.uri.get("environment")
        if not isinstance(self.env, str) or self.env not in ALL_ENV:
            raise EnvTypeExp(env=self.env)
        self.register_token = None
        self._set_up_gateway_service_url()
        self._setup_uri_params()
        self._setup_register_params()
        self._get_register_token()
        if not self.register_token:
            raise GetRegisterTokenErr(msg="can't get register token")
        else:
            self.headers.update({"X-Access-Token": self.register_token})

    def _set_up_gateway_service_url(self):
        try:
            self.gateway_base_urls = GatewayConfig.__dict__.get(self.env, {}).get("servers", "").split(",")
            self.port = GatewayConfig.__dict__.get(self.env, {}).get("port")
            url_pre = "http://{}:{}"
            self.gateway_base_urls = [url_pre.format(_url, self.port) for _url in self.gateway_base_urls]
            self.register_meta_data_suffix = "/gateway-shenyu/register-metadata"
            self.register_uri_suffix = "/gateway-shenyu/register-uri"

            self.register_meta_data_path_list = [_url + self.register_meta_data_suffix for _url in
                                                 self.gateway_base_urls]
            self.register_uri_list = [_url + self.register_uri_suffix for _url in self.gateway_base_urls]
        except SetUpGatewayExp as sue:
            raise SetUpUriExp(app_name=GatewayConfig.uri.get("app_name"), msg=str(sue), env=self.env)

    def _setup_uri_params(self):
        """
        setup uri params
        """
        try:
            self.host = GatewayConfig.uri.get("host")
            self.port = GatewayConfig.uri.get("port")
            self.app_name = GatewayConfig.uri.get("app_name")
            self.rpc_type = GatewayConfig.uri.get("rpc_type")
            self.context_path = GatewayConfig.uri.get("context_path")
            self.register_type = GatewayConfig.register.get("register_type")
            self.register_servers = GatewayConfig.register.get("register_servers")
        except SetUpUriExp as se:
            raise SetUpUriExp(app_name=GatewayConfig.uri.get("app_name"), msg=str(se), env=self.env)
        
    def _setup_register_params(self):
        """
        setup register params
        """
        try:
            self.register_token_type = GatewayConfig.register.get("register_type")
            self.register_base_servers = GatewayConfig.register.get("servers").split(",")
            self.register_path = "/platform/login"
            self.register_token_servers = [_url + self.register_uri_suffix for _url in self.register_base_servers]
            self.register_username = GatewayConfig.register.get("props", {}).get("username")
            self.register_password = GatewayConfig.register.get("props", {}).get("password")
        except SetUpRegisterExp as se:
            raise SetUpRegisterExp(app_name=GatewayConfig.uri.get("app_name"), msg=str(se), env=self.env)

    def _request(self, url, json_data):
        """
        base post request
        """
        if not url or not isinstance(url, str) or not isinstance(json_data, dict):
            print("_request url or data format error")
            return False
        try:
            res = requests.post(url, json=json_data, headers=self.headers, timeout=5)
            status_code = res.status_code
            msg = res.text
        except ConnectTimeout as ce:
            print("connect timeout, detail is:{}".format(str(ce)))
            return False
        except ReadTimeout as rte:
            print("read time out, detail is:{}".format(str(rte)))
            return False
        except RequestException as rqe:
            print("request except, detail is:{}".format(str(rqe)))
            return False
        except Exception as e:
            print("request ({}) except, detail is:{}".format(url, str(e)))
            return False
        else:
            # According to the interface return value of the gateway registry, the request is considered successful
            # only when msg==success; if the interface return value of the gateway registry changes, the judgment
            # method should also be modified
            if msg == "success":
                return True
            print("request ({}) fail, status code is:{}, msg is:{}".format(res.url, status_code, msg))
            return False

    def _get_register_token(self):
        """
        base get http request
        """
        default_res = ""
        params = {
            "userName": self.register_username,
            "password": self.register_password
        }
        try:
            for url in self.register_token_servers:
                res = requests.get(url, params=params, timeout=5)
                status_code = res.status_code
                res_data = res.json()
                token = res_data.get("data", {}).get("token", "")
                if token:
                    self.register_token = token
                    break
        except ConnectTimeout as ce:
            print("connect timeout, detail is:{}".format(str(ce)))
            return False
        except ReadTimeout as rte:
            print("read time out, detail is:{}".format(str(rte)))
            return False
        except RequestException as rqe:
            print("request except, detail is:{}".format(str(rqe)))
            return False
        except Exception as e:
            print("get register token except, detail is:{}".format(str(e)))
            return False

    def register_uri(self):
        """
        register uri
        """
        json_data = {
            "appName": self.app_name,
            "contextPath": self.context_path,
            "rpcType": self.rpc_type,
            "host": self.host,
            "port": self.port
        }
        register_flag = False
        for _url in self.register_uri_list:
            res = self._request(_url, json_data)
            if not res:
                continue
            else:
                print("[SUCCESS], register uri success, register data is:{}".format(str(json_data)))
                register_flag = True
                break
        if not register_flag:
            print("[ERROR], register uri fail, app_name is:{}, host is:{}, port is:{}".format(self.app_name,
                                                                                              self.host,
                                                                                              self.port))
        return register_flag

    def register_metadata(self, **kwargs):
        """
        register path to gateway
        path:            The path needs to be unique,  for example, your path is: /order/findById, your request prefix
                         is: /hello, the path must be /hello/order/findById
        register_all     Register all paths ?
        rule_name:       Can be the same as path
        enabled:         Whether to open, If you want to open the gateway proxy, you must fill in True
        path_desc:       Path description, optional filling
        register_meta_data: Need to register metadata, not for http request, fill in false
        """
        if not kwargs.get("register_all") and not kwargs.get("path"):
            return False

        register_all = kwargs.get("register_all", False)
        path = kwargs.get("path", "")
        rule_name = kwargs.get("rule_name", "")
        enabled = kwargs.get("enabled", True)
        path_desc = kwargs.get("path_desc", "")
        register_meta_data = kwargs.get("register_meta_data", False)
        if register_all:
            path = self.context_path + "**" if self.context_path.endswith("/") else self.context_path + "/**"
        rule_name = path if not rule_name else rule_name
        json_data = {
            "appName": self.app_name,
            "contextPath": self.context_path,
            "path": path,
            "pathDesc": path_desc,
            "rpcType": self.rpc_type,
            "ruleName": rule_name,
            "enabled": enabled,
            "registerMetaData": register_meta_data,
            "pluginNames": []

        }
        register_flag = False
        for _url in self.register_meta_data_path_list:
            res = self._request(_url, json_data)
            if not res:
                continue
            else:
                print("[SUCCESS], register metadata success, register data is:{}".format(str(json_data)))
                register_flag = True
                break
        if not register_flag:
            print("[ERROR],register metadata fail, app_name:{}, path:{}, contextPath:{}".format(self.app_name,
                                                                                                path,
                                                                                                self.context_path))
        return register_flag
