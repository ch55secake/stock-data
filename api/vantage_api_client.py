import json
import time
from typing import Dict

import pandas as pd
import requests as req

from exception.vantage_api_exception import VantageApiRequestException


class VantageApiClient(object):
    """
    Client for interacting with the vantage api and also converting data into dataframes
    """

    def __init__(self, url: str, api_key: str, data_type: str):
        """
        Create vantage client, will have to provide your own rapid api key and the host needing to be used
        :param url: url of vantage api
        :param api_key: users rapid api key
        :param data_type: data_type of response from rapid api
        """
        self.url = url
        self.api_key = api_key
        self.data_type = data_type
        self.headers = self.get_default_headers()

    def get_default_headers(self) -> dict[str, str]:
        """
        Get default headers needed for making every request
        :return: dictionary of default headers, contains host and api key
        """
        return {
            "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
            "X-RapidAPI-Key": self.api_key
        }

    def build_query_params(self,
                           symbol: str = "BTCGBP",
                           interval: str = "5min",
                           function: str = "RSI",
                           series_type: str = "close") -> dict[str, str]:
        """
        Builds query params for interacting with the api, most params will default to a preset value
        :param series_type: when you want to fetch data from market close or market open
        :param function: what data you want to collect, in this case will default and collect Relative Strength Index
        :param symbol: ticker that you want to collect data about
        :param interval: interval that data is split up into
        :return: params as dictionary
        """
        return {
            "time_period": "60",
            "interval": interval,
            "series_type": series_type,
            "function": function,
            "symbol": symbol,
            "datatype": self.data_type
        }

    def make_request(self, params: dict = build_query_params) -> json | VantageApiRequestException:
        """
        Make request to the Vantage API, query params built for you unless passed in
        :params: defaults to prior method, if not own query params can be provided
        :return: either the response as json or a client exception
        """
        try:
            response = req.get(self.url, headers=self.headers, params=params)
            return response.json()
        except req.exceptions.Timeout:
            print(f"Timeout whilst making request to Vantage API")
        except req.exceptions.RequestException as e:
            raise VantageApiRequestException(e.strerror)

    def make_request_and_export_to_df(self, key: str, time_series_key: str, params: dict = build_query_params) -> (pd.DataFrame
                                                                                                                   | VantageApiRequestException):
        """
        Makes request and then exports json response out into its own dataframe
        :param key: key from response to append to output list
        :param time_series_key: the key for parsing the way that the response is split
        :param params: will default to build_query_params, unless different params are provided
        :return: Dataframe built from json response
        """
        request: json = self.make_request(params)
        output: list = []
        for v in request[time_series_key].values():
            output.append(v[key])
        return pd.DataFrame({
            key: output
        })

