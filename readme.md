# AlgoTrade4j Python SDK

This SDK provides a simple Python interface to fetch market data from the AlgoTrade4j Platform. It supports fetching candles for different instruments, brokers, and time periods.

## Installation

### Local Installation

To install the SDK locally into your Python environment, first clone the repository:

```bash
git clone https://github.com/jwtly10/algotrade4j_py.git
```

Then, navigate into the project directory and install it in editable mode:

``` bash
pip install -e .
```

### GitHub Installation

You can also install the SDK directly from GitHub:

```bash
pip install git+https://github.com/jwtly10/algotrade4j_py.git
```

### Usage
The SDK allows you to fetch market data easily. Here’s an example:

```python
from algotrade4j_py.client import MarketDataClient

# Initialize the client (API key is picked up from the environment if not provided)
client = MarketDataClient(api_key="your_api_key_here")

# Fetch candle data for a 15-minute period
df = client.get_candles(
    instrument='NAS100USD',
    broker='OANDA',
    from_date='2020-10-01T00:00:00Z',
    to_date='2024-10-10T00:00:00Z',
    period='M15'
)

# Display the first few rows of data
print(df.head())

```

### Custom API URL
You can override the URL for the api for local testing of the Algotrade4j Platform:

```python
client = MarketDataClient(api_url="http://localhost:8080/api/v1/marketdata/candles")
```

### API Key
By default, the SDK reads the API key from the environment variable `MARKETDATA_API_KEY`. You can set this variable in your environment like so:

```bash
export MARKETDATA_API_KEY=your_api_key_here
```

Alternatively, you can pass the API key directly to the MarketDataClient:

```python
client = MarketDataClient(api_key="your_api_key_here")
```