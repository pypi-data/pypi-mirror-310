import httpx
import logging
from datetime import datetime
from typing import Union, Optional, List, Literal
from pydantic import BaseModel, AliasChoices, Field, RootModel


logger = logging.getLogger(__name__)

class DataRecord(BaseModel):
    datasetId: int
    startTime: datetime
    endTime: datetime
    value: float

class Pagination(BaseModel):
    total: int
    lastPage: int
    prevPage: Optional[int]
    nextPage: Optional[int]
    perPage: int
    currentPage: int
    from_: int = Field(validation_alias=AliasChoices('from', 'from_')) # using from_ to avoid conflict with the Python keyword 'from'
    to: int

class TimeSeriesDataResponse(BaseModel):
    data : List[DataRecord]
    pagination : Pagination

class ActiveNotification(BaseModel):
    id: int
    modifiedAtUtc: Optional[datetime]
    startTimeUtc: datetime
    endTimeUtc: datetime
    messageFi: str
    messageEn: str
    linkFi: Optional[str]
    linkEn: Optional[str]
    linkTextFi: Optional[str]
    linkTextEn: Optional[str]

class ActiveNotifications(RootModel):
    root: List[ActiveNotification]

class License(BaseModel):
    name:str
    termsLink:str

class DataSet(BaseModel):
    id: int
    modifiedAtUtc: datetime
    type: Literal["timeseries", "file"]
    isPublic: bool
    status: Literal["active", "inactive"]
    organization: str
    nameFi: str
    nameEn: str
    descriptionFi: str
    descriptionEn: str
    dataPeriodFi: str
    dataPeriodEn: str
    unitFi: str
    unitEn: str
    updateCadenceFi: Optional[str] = None
    updateCadenceEn: Optional[str] = None
    contactPersons: Optional[str] = None
    license: Optional[License] = None
    keyWordsFi: Optional[List[str]] = None
    keyWordsEn: Optional[List[str]] = None
    contentGroupsFi: Optional[List[str]] = None
    contentGroupsEn: Optional[List[str]] = None
    availableFormats: Optional[List[Literal["csv", "json", "app", "7zip", "zip", "xlsx", "xml"]]] = None

class StatusResponse(BaseModel):
    status:str
    message: Optional[str] = None

class HealtStatus(BaseModel):
    network: StatusResponse
    database: StatusResponse
    network: StatusResponse

class FingridApi:
    """
    A client for interacting with the Fingrid API.
    """
    def __init__(self,client : httpx.Client,  x_api_key:str, base_url:str="https://data.fingrid.fi/api"):
        """
        Initialize the Fingrid API client.

        Parameters:
            client (httpx.Client): 
                An instance of httpx.Client for making HTTP requests.
            x_api_key (str): 
                The API key for authenticating requests to the Fingrid API.
            base_url (str, optional): 
                The base URL for the Fingrid API. Defaults to 
                "https://data.fingrid.fi/api".
        """
        self.client = client
        self.x_api_key = x_api_key
        self.client.base_url = base_url
        self.client.headers = {"X-Api-Key" : str(self.x_api_key)}

    def get_last_data_by_dataset(self, datasetId:int)->DataRecord:
        """datasetId: int
        
        fetches latest data from dataset.

        return: DataRecord

        """
        response = self.client.get(url=f"/datasets/{datasetId}/data/latest")
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occured while trying to get last data by dataset with response status code: {response.status_code} with content: {response.content}",
                         exc_info=True)
            raise
        data = DataRecord(**response.json())
        return data
    
    def get_multiple_timeseries_data(self, datasetId:Union[List[str],List[int]], **kwargs)->TimeSeriesDataResponse:
        """
        Retrieves multiple time series data for the specified dataset IDs.

        Parameters:
            datasetId (Union[List[str], List[int]]): 
                A list of dataset IDs, which can be strings or integers. These IDs 
                are used to specify the datasets for which time series data will 
                be retrieved.

            **kwargs (dict, optional): 
                Additional query parameters to be included in the API request. 
                These are passed as key-value pairs and merged with the required 
                `datasets` parameter.

        Returns:
            TimeSeriesDataResponse: 
                An instance of `TimeSeriesDataResponse` containing the parsed data 
                retrieved from the API.

        Raises:
            HTTPError: 
                Raised if the HTTP request to the API endpoint fails, with 
                additional error details logged.

        Behavior:
            1. Constructs a query parameter named `datasets` by joining the 
            provided dataset IDs with commas.
            2. Merges additional keyword arguments (`kwargs`) into the query 
            parameters.
            3. Makes an HTTP GET request to the `/data` endpoint using the 
            provided client.
            4. If the request fails, logs the error details, including the status 
            code and response content, and re-raises the exception.
            5. On a successful response, parses the JSON data into a 
            `TimeSeriesDataResponse` object and returns it.

        Example Usage:
            from typing import List
            from pyfingridapi import FingridApi
            import httpx

            // Example dataset IDs
            dataset_ids: List[int] = [123, 456, 789]

            // Initialize the Fingrid API client
            with httpx.Client() as http_client:
                api_client = FingridApi(client=http_client, x_api_key="your_api_key"
                try:
                    response = api_client.get_multiple_timeseries_data(
                        datasetId=dataset_ids, startDate="2024-01-01", endDate="2024-01-31"
                    )
                    print(response)
                except Exception as e:
                    print(f"Failed to fetch time series data: {e}")
        """
        params = {
            "datasets" : ",".join([str(id) for id in datasetId])
        }
        params.update(dict(kwargs))
        response = self.client.get(url=f"/data", params=params)
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occured while trying to get multiple timeseries data with response status code: {response.status_code} with content: {response.content}",
                         exc_info=True)
            raise
        data = TimeSeriesDataResponse(**response.json())
        return data

    def get_active_notifications(self)->ActiveNotifications:
        """
        Retrieves the list of active notifications from the API.

        Returns:
            ActiveNotifications: 
                An instance of `ActiveNotifications` containing the parsed 
                data retrieved from the API.

        Raises:
            HTTPError: 
                Raised if the HTTP request to the API endpoint fails, with 
                additional error details logged.

        Behavior:
            1. Makes an HTTP GET request to the `/notifications/active` 
               endpoint using the provided client.
            2. If the request fails, logs the error details, including the 
               status code and response content, and re-raises the exception.
            3. On a successful response, parses the JSON data into an 
               `ActiveNotifications` object and returns it.

        Example Usage:
            import httpx
            from pyfingridapi import FingridApi

            // Initialize the Fingrid API client
            with httpx.Client() as http_client:
                api_client = FingridApi(client=http_client, x_api_key="your_api_key"

                // Fetch active notifications
                try:
                    active_notifications = api_client.get_active_notifications()
                    print(active_notifications)
                except Exception as e:
                    print(f"Failed to fetch active notifications: {e}")
        """
        response = self.client.get(url=f"/notifications/active")
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occured while trying to get multiple timeseries data with response status code: {response.status_code} with content: {response.content}",
                         exc_info=True)
            raise
        logger.debug(f"{response.json()=}")
        if response.json():
            data = ActiveNotifications(**response.json())
        else:
            data = None
        return data

    def get_dataset(self, datasetId:int)->DataSet:
        """
        Retrieves details of a specific dataset by its ID from the Fingrid API.

        Parameters:
            datasetId (int): 
                The ID of the dataset to retrieve.

        Returns:
            DataSet: 
                An instance of `DataSet` containing the parsed data retrieved 
                from the API.

        Raises:
            HTTPError: 
                Raised if the HTTP request to the API endpoint fails, with 
                additional error details logged.

        Behavior:
            1. Sends an HTTP GET request to the `/datasets/{datasetId}` endpoint.
            2. If the request fails, logs the error details, including the 
            status code and response content, and re-raises the exception.
            3. On a successful response, parses the JSON data into a `DataSet` 
            object and returns it.

        Example Usage:
            import httpx
            from pyfingridapi import FingridApi

            // Initialize the Fingrid API client
            with httpx.Client() as http_client:
                api_client = FingridApi(client=http_client, x_api_key="your_api_key")

                // Fetch a dataset by ID
                try:
                    dataset = api_client.get_dataset(datasetId=12345)
                    print(dataset)
                except Exception as e:
                    print(f"Failed to fetch dataset: {e}")

        Notes:
            - Ensure that the `DataSet` class is properly defined and matches the 
            expected structure of the API response.
            - Logging is enabled to provide detailed information in case of 
            errors, aiding in debugging.
        """
        response = self.client.get(url=f"/datasets/{datasetId}")
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occurred while trying to get dataset with ID {datasetId}. " \
                             f"Response status code: {response.status_code}, content: {response.content}",
                         exc_info=True)
            raise
        data = DataSet(**response.json())
        return data

    def get_dataset_data(self, datasetId:int, **kwargs)->TimeSeriesDataResponse:
        """
        Retrieves time series data for a specific dataset from the Fingrid API.

        Parameters:
            datasetId (int): 
                The ID of the dataset for which data is being retrieved.
            **kwargs (dict, optional): 
                Additional query parameters to be included in the API request. 
                These are passed as key-value pairs.

        Returns:
            TimeSeriesDataResponse: 
                An instance of `TimeSeriesDataResponse` containing the parsed 
                data retrieved from the API.

        Raises:
            HTTPError: 
                Raised if the HTTP request to the API endpoint fails, with 
                additional error details logged.

        Behavior:
            1. Constructs query parameters using `datasetId` and additional 
            keyword arguments (`kwargs`).
            2. Sends an HTTP GET request to the `/datasets/{datasetId}/data` 
            endpoint.
            3. If the request fails, logs the error details, including the 
            status code and response content, and re-raises the exception.
            4. On a successful response, parses the JSON data into a 
            `TimeSeriesDataResponse` object and returns it.

        Example Usage:
            import httpx
            from pyfingridapi import FingridApi

            // Initialize the Fingrid API client
            with httpx.Client() as http_client:
                api_client = FingridApi(client=http_client, x_api_key="your_api_key")

                // Fetch dataset data
                try:
                    dataset_data = api_client.get_dataset_data(datasetId=12345, startTime="2023-06-28T12:30:00Z", endTime="2023-06-28T14:40:00Z")
                    print(dataset_data)
                except Exception as e:
                    print(f"Failed to fetch dataset data: {e}")
        """
        params = dict(kwargs)
        response = self.client.get(url=f"/datasets/{datasetId}/data", params=params)
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occurred while trying to get dataset data with ID {datasetId}. " \
                             f"Response status code: {response.status_code}, content: {response.content}",
                         exc_info=True)
            raise
        data = TimeSeriesDataResponse(**response.json())
        return data

    def get_health_status(self)->HealtStatus:
        """
        Retrieves the health status of the Fingrid API.

        Returns:
            HealthStatus: 
                An instance of `HealthStatus` containing the parsed data 
                retrieved from the API.

        Raises:
            HTTPError: 
                Raised if the HTTP request to the API endpoint fails, with 
                additional error details logged.

        Behavior:
            1. Sends an HTTP GET request to the `/health` endpoint.
            2. If the request fails, logs the error details, including the 
            status code and response content, and re-raises the exception.
            3. On a successful response, parses the JSON data into a 
            `HealthStatus` object and returns it.

        Example Usage:
            import httpx
            from pyfingridapi import FingridApi

            //Initialize the Fingrid API client
            with httpx.Client() as http_client:
                api_client = FingridApi(client=http_client, x_api_key="your_api_key")

                //Check health status
                try:
                    health_status = api_client.get_health_status()
                    print(health_status)
                except Exception as e:
                    print(f"Failed to fetch health status: {e}")
        """
        response = self.client.get(url=f"/health")
        try: 
            response.raise_for_status()
        except Exception:
            logger.error(msg=f"Exception occurred while trying to get health status. " \
                             f"Response status code: {response.status_code}, content: {response.content}",
                         exc_info=True)
            raise
        data = HealtStatus(**response.json())
        return data



    # TODO: add functions for these api calls, GetDatasetFile, GetDatasetFileData, GetDatasetShorts

