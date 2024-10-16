import pandas as pd
from pandas import DataFrame


class IndicationCalculator(object):
    """
    Produce true/false information about current stock data and generate some outputs derived from other info
    """

    def __init__(self, stock_data: pd.DataFrame):
        """
        :param stock_data: dataframe data from network request to previous apis
        """
        self.stock_data: pd.DataFrame = stock_data

    def is_stock_supported(self, index: int = 0) -> bool:
        """
        Determine whether current data shows that the stock is supported or not
        :param index: provide index dependent on how much it needs to be iterated over
        :return: bool based on whether stock is supported or not
        """
        return (self.stock_data['Low'][index] < self.stock_data['Low'][index - 1] < self.stock_data['Low'][index - 2]
                and self.stock_data['Low'][index] < self.stock_data['Low'][index + 1] < self.stock_data['Low'][index + 2])

    def is_stock_resistant(self, index: int = 0) -> bool:
        """
        Determine whether current data shows that the stock is resistant or not
        :param index: provide index dependent on how much you want to iterate over it
        :return: bool based on whether stock is supported or not
        """
        return self.stock_data['High'][index] > self.stock_data['High'][index - 1] > self.stock_data['High'][
            index - 2] and self.stock_data['High'][index] > self.stock_data['High'][index + 1] > self.stock_data['High'][index + 2]

    def check_rsi(self) -> bool:
        """
        Check the relative value of the RSI of a given stock. (Relative Strength Index)
        :return: bool based on whether the RSI is at a higher more acceptable value or lower less acceptable value
        """
        if self.stock_data.iloc[:, 0].gt(70, 90).all():
            print(
                "Values of 70 or above indicate that an asset is becoming overbought and may be primed for a "
                "trend reversal or experience correction in the price of the asset.")
            return True
        elif self.stock_data.iloc[:, 0].lt(0, 35).all():
            print("An RSI reading of 30 or below indicates an oversold or undervalued condition.")
        return False

    def output_rsi_for_df(self, key: str = "RSI") -> None:
        """
        Loop through a given dataframe and output the given RSI for said stock data
        :param key: key will default to RSI as that is what the response body looks like
        """
        for index in range(0, len(self.stock_data)):
            self.stock_data[key] = pd.to_numeric(self.stock_data[key], errors='coerce').fillna(0, downcast='infer')
            print(f"Row {index}: {self.stock_data[key][index]} Check on : {self.check_rsi()}")


    def output_support_or_resistance(self) -> None:
        """
        Output whether given stock data is currently supported or resistant, will use the dataframe passed in when the
        class is instantiated
        """
        for index in range(2, len(self.stock_data)):
            print(f"Row {index}: {self.stock_data['High'][index]} {self.stock_data['Low'][index]} "
                  f"Supported: {self.is_stock_supported()} "
                  f"Resistant: {self.is_stock_supported()}")


    @staticmethod
    def collect_with_key(key: str, time_series_key: str, api_response: dict) -> DataFrame:
        """
        Collect a given json response to a Dataframe
        :param key: key used to append to list with
        :param time_series_key: key to parse api response with
        :param api_response: api response from stock api
        :return: new data frame built from data from the api
        """
        output: list = []
        for v in api_response[time_series_key].values():
            output.append(v[key])
        return pd.DataFrame({
            key: output
        })