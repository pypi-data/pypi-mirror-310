import os
import time
import httpx
import pytest
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv
from pyfingridapi import fingridapi

logger = logging.getLogger(__name__)
log_format = "%(asctime)-15s - %(name)-15s - %(levelname)-8s - %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    handlers=[
        logging.StreamHandler()
    ]
)


@pytest.fixture
def get_x_api_key():
    higher_level_path = Path(os.getcwd()).joinpath("secrets.env")
    logger.debug(f"{higher_level_path=}")
    load_dotenv(higher_level_path)


@pytest.fixture
def get_data_ids_str():
    return ["188", "181", "22", "191"]

@pytest.fixture
def get_data_ids_int():
    return [188,181,22,191]

@pytest.mark.order(1)
def test_fetching_lates_data(get_x_api_key):
    with httpx.Client() as client:
        key = os.getenv('fg_api_key')
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=key)
        result = fg_client.get_last_data_by_dataset('345')
        logger.debug(f"{result=}")
        assert result.startTime.day == datetime.datetime.now().day
    time.sleep(5)

@pytest.mark.order(2)
def test_getting_multiple_timeseries_data(get_x_api_key, get_data_ids_int, get_data_ids_str):
    with httpx.Client(timeout=29) as client:
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=os.getenv('fg_api_key'))
        
        result = fg_client.get_multiple_timeseries_data(get_data_ids_int)
        logger.debug(f"{result}")
        assert result.data[0].value != None
        time.sleep(10)
        result = fg_client.get_multiple_timeseries_data(get_data_ids_str)
        logger.debug(f"{result}")
        assert result.data[0].value != None
    time.sleep(5)

@pytest.mark.order(3)
def test_get_healt_status(get_x_api_key):
    with httpx.Client(timeout=29) as client:
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=os.getenv('fg_api_key'))
        
        result = fg_client.get_health_status()
        logger.debug(f"{result}")
        assert result != None
        assert result.network.status == "OK"
        assert result.database.status == "OK"
    time.sleep(5)

@pytest.mark.order(4)
def test_get_active_notifications(get_x_api_key):
    with httpx.Client(timeout=29) as client:
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=os.getenv('fg_api_key'))
        
        result = fg_client.get_active_notifications()
        logger.debug(f"{result}")
        assert result == None
    time.sleep(5)

@pytest.mark.order(5)
def test_get_dataset(get_x_api_key):
    with httpx.Client(timeout=29) as client:
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=os.getenv('fg_api_key'))
        
        result = fg_client.get_dataset(188)
        logger.debug(f"{result}")
        assert result.id == 188
    time.sleep(5)

@pytest.mark.order(6)
def test_get_dataset_data(get_x_api_key):
    with httpx.Client(timeout=29) as client:
        fg_client = fingridapi.FingridApi(client=client,
                                          x_api_key=os.getenv('fg_api_key'))
        
        result = fg_client.get_dataset_data(188)
        logger.debug(f"{result}")
        assert result.data[0].datasetId == 188
    time.sleep(5)

# TODO: create tests for get_dataset_data, 

