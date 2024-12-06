
# Pyfingridapi

`pyfingridapi` is a Python client library for interacting with the Fingrid API. It provides convenient methods for accessing time-series data, dataset information, notifications, and the health status of the Fingrid API.

## Features

- Fetch real-time and historical time-series data.
- Retrieve detailed dataset metadata.
- Access active notifications and alerts.
- Check the health status of the Fingrid API services.
- Built using `httpx` for robust HTTP interactions and `pydantic` for data validation.

## Installation

Install the library using pip:

```bash
pip install pyfingriaApi
```

## Usage

### Initialization

Create an instance of the `FingridApi` client:

```python
import httpx
from pyfingridapi import FingridApi

# Initialize the API client
with httpx.Client() as client
    api_client = FingridApi(client=client, x_api_key="your_api_key")
```

### Fetching the Latest Data by Dataset

```python
latest_data = api_client.get_last_data_by_dataset(datasetId=12345)
print(latest_data)
```

### Fetching Multiple Time Series Data

```python
time_series_data = api_client.get_multiple_timeseries_data(
    datasetId=[123, 456],
    startTime="2024-01-01T00:00:00Z",
    endTime="2024-01-31T23:59:59Z"
)
print(time_series_data)
```

### Retrieving Dataset Information

```python
dataset_info = api_client.get_dataset(datasetId=12345)
print(dataset_info)
```

### Fetching Active Notifications

```python
notifications = api_client.get_active_notifications()
print(notifications)
```

### Checking API Health Status

```python
health_status = api_client.get_health_status()
print(health_status)
```

## Models

The library uses `pydantic` models to structure and validate the data retrieved from the API. Key models include:

- `DataRecord`: Represents a single data point in a time series.
- `TimeSeriesDataResponse`: Encapsulates time-series data and pagination information.
- `DataSet`: Contains detailed metadata about a dataset.
- `ActiveNotifications`: Represents active notifications from Fingrid.
- `HealthStatus`: Describes the health status of the Fingrid API.

## Logging

`pyfingridapi` uses Python's `logging` module to log errors and debug information. To configure logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fingridapi")
```

## TODO

- Add support for API endpoints such as `GetDatasetFile`, `GetDatasetFileData`, and `GetDatasetShorts`.
- test this as module
- push this to pypi_test
- push this to pypi
- create documentation site

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the library.


