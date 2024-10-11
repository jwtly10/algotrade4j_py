import requests
import pandas as pd
import os


class MarketDataClient:
    """
    MarketDataClient is a Python client for fetching market data from the AlgoTrade4J platform.
    It supports fetching candle data for various instruments, brokers, and periods within a specified time range.

    Attributes:
        api_key (str): API key for authentication. Defaults to reading from the 'MARKETDATA_API_KEY' environment variable.
        api_url (str): Base URL of the AlgoTrade4J market data API. Defaults to the production URL.

    Constants:
        SUPPORTED_BROKERS (list): List of supported brokers.
        SUPPORTED_INSTRUMENTS (list): List of supported instruments.
        SUPPORTED_PERIODS (list): List of supported candle periods.

    Methods:
        get_candles(instrument, broker, from_date, to_date, period): Fetches candle data for the specified instrument, broker, period, and time range.
    """

    SUPPORTED_BROKERS = ["OANDA", "MT4"]
    SUPPORTED_INSTRUMENTS = ["NAS100USD", "EURUSD", "GBPUSD"]
    SUPPORTED_PERIODS = ["M1", "M5", "M15", "M30", "H1", "H4", "D"]

    def __init__(
        self,
        api_key=None,
        api_url="https://api.algotrade4j.trade/api/v1/marketdata/candles",
    ):
        """
        Initialize the MarketDataClient with an optional API key and base API URL.

        Args:
            api_key (str, optional): API key for authentication. Defaults to None, in which case it will read from the 'MARKETDATA_API_KEY' environment variable.
            api_url (str, optional): Base API URL for the market data endpoint. Defaults to the production API URL.

        Raises:
            ValueError: If no API key is provided and it cannot find one in the environment.
        """
        self.api_key = api_key or os.getenv("MARKETDATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either directly or via the environment variable 'MARKETDATA_API_KEY'."
            )
        self.api_url = api_url

    def get_candles(self, instrument, broker, from_date, to_date, period):
        """
        Fetch candle data for a specific instrument, broker, and time range.

        Args:
            instrument (str): The trading instrument (e.g., 'NAS100USD', 'EURUSD'). Must be one of the SUPPORTED_INSTRUMENTS.
            broker (str): The broker from which to fetch data (e.g., 'OANDA', 'MT4'). Must be one of the SUPPORTED_BROKERS.
            from_date (str): The start date in ISO 8601 format (e.g., '2020-10-01T00:00:00Z').
            to_date (str): The end date in ISO 8601 format (e.g., '2024-10-10T00:00:00Z').
            period (str): The candlestick period (e.g., 'M1', 'M5', 'M15', 'H1', etc.). Must be one of the SUPPORTED_PERIODS.

        Returns:
            pandas.DataFrame: A DataFrame containing the candle data. By default formatted for compatibility with backtesting.py (open, high, low, close, volume).


        Raises:
            ValueError: If the provided broker, instrument, or period is not supported.
            Exception: If the API request fails.
        """
        if broker not in self.SUPPORTED_BROKERS:
            raise ValueError(
                f"Broker '{broker}' is not supported. Supported brokers: {self.SUPPORTED_BROKERS}"
            )

        if instrument not in self.SUPPORTED_INSTRUMENTS:
            raise ValueError(
                f"Instrument '{instrument}' is not supported. Supported instruments: {self.SUPPORTED_INSTRUMENTS}"
            )

        if period not in self.SUPPORTED_PERIODS:
            raise ValueError(
                f"Period '{period}' is not supported. Supported periods: {self.SUPPORTED_PERIODS}"
            )

        params = {
            "instrument": instrument,
            "broker": broker,
            "from": from_date,
            "to": to_date,
            "period": period,
        }

        headers = {"X-API-Key": self.api_key}

        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            candles = response.json()
            df = pd.DataFrame(candles)

            # Convert 'openTime' to datetime and set it as the index
            df["openTime"] = pd.to_datetime(df["openTime"], unit="ns")

            df.set_index("openTime", inplace=True)

            # Rename columns for backtesting.py compatibility
            df.rename(
                columns={
                    "open": "Open",
                    "high": "High",
                    "low": "Low",
                    "close": "Close",
                    "volume": "Volume",
                },
                inplace=True,
            )

            # Ensure correct column ordering
            df = df[["Open", "High", "Low", "Close", "Volume"]]

            return df
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
