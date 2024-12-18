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

    SUPPORTED_BROKERS = ["OANDA"]
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

    def get_candles(self, instrument, broker, from_date, period, limit, to_date=None):
        """
        Fetch candle data for a specific instrument, broker, and time range.

        Args:
            instrument (str): The trading instrument (e.g., 'NAS100USD', 'EURUSD'). Must be one of the SUPPORTED_INSTRUMENTS.
            broker (str): The broker from which to fetch data (e.g., 'OANDA'). Must be one of the SUPPORTED_BROKERS.
            from_date (str): The start date in ISO 8601 format (e.g., '2020-10-01T00:00:00Z').
            period (str): The candlestick period (e.g., 'M1', 'M5', 'M15', 'H1', etc.). Must be one of the SUPPORTED_PERIODS.
            limit (int): The maximum number of candles to fetch. Defaults to 10,000 (To support backtesting.py & bokeh dependency by default).
            to_date (str): The end date in ISO 8601 format (e.g., '2024-10-10T00:00:00Z'). Will default to the current date @ UTC if not provided.

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

        if limit == None or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        if from_date == None:
            raise ValueError("From date must be provided.")

        if to_date == None:
            to_date = pd.Timestamp.now(tz="UTC").isoformat()

        params = {
            "instrument": instrument,
            "broker": broker,
            "from": from_date,
            "to": to_date,
            "period": period,
            "limit": limit
        }

        headers = {"X-API-Key": self.api_key}

        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            candles = response.json()
            df = pd.DataFrame(candles)

            # Convert 'openTime' to datetime and set it as the index
            df["openTime"] = pd.to_datetime(df["openTime"], unit="s")
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
