"""
Reference Data Extractor for Geo-Addressing.

This module downloads and extracts reference data from the Precisely Data Delivery API
for geo-addressing functionalities. It organizes data by functionality type and handles
authentication, download, and extraction processes.
"""
import argparse
import re
import os
import base64
import json
import time
import requests
import urllib
import os.path
import sys
from builtins import bytes
from zipfile import ZipFile
import subprocess
import logging

def current_milli_time():
    """Get current time in milliseconds."""
    return int(round(time.time() * 1000))

FUNCTIONALITY_SPD_MAPPING = {
  "spark-addressing-data": [
    "Geocoding MLD US#United States#All USA#Spectrum Platform Data",
    "Geocoding NT Street US#United States#All USA#Spectrum Platform Data",
    "Geocoding Reverse PRECISELYID#United States#All USA#Spectrum Platform Data",
  ]
}


class DataDeliveryClient:
    """Client for interacting with the Precisely Data Delivery API."""
    auth_token = ''
    token_expiration = 0

    __api_host = 'https://api.precisely.com'

    api_url = __api_host + '/digitalDeliveryServices/v1/'
    auth_url = __api_host + '/oauth/token'
    pdx_api_url = __api_host + '/pdx/api/public/sdk/v1/'

    @property
    def api_host(self):
        return self.__api_host

    @api_host.setter
    def api_host(self, var):
        self.__api_host = 'https://' + var
        self.api_url = self.api_host + '/digitalDeliveryServices/v1/'
        self.auth_url = self.api_host + '/oauth/token'
        self.pdx_api_url = self.api_host + '/pdx/api/public/sdk/v1/'

    def __init__(self, api_key, shared_secret, app_id):
        self.api_key = api_key
        self.shared_secret = shared_secret
        self.app_id = app_id

    def get_deliveries(self, product_name, geography=None, roster_granularity=None, page_number=1, limit=None,
                       min_release_date=None, data_format=None, preferred_format: bool = False,
                       latest: bool = False):
        """Get data deliveries from the API based on specified criteria."""
        params = {}
        if latest:
            params['byLatest'] = True
        if product_name:
            params['ProductName'] = product_name
        if geography:
            params['geography'] = geography
        if roster_granularity:
            params['rosterGranularity'] = roster_granularity
        if page_number:
            params['pageNumber'] = int(page_number)
        if limit:
            params['pageSize'] = int(limit)
        if min_release_date:
            params['laterThanDate'] = min_release_date
        if data_format:
            params['dataFormat'] = data_format
        if preferred_format:
            params['preference'] = 'true'

        response = self.get(url=self.pdx_api_url + 'data-deliveries', params=params,
                            headers=self.create_headers())
        return json.loads(response.text)

    def create_headers(self):
        """Create HTTP headers with authorization token."""
        return {
            'Authorization': 'Bearer ' + self.get_auth_token()
        }

    def get_auth_token(self):
        """Get the current authentication token, refreshing if necessary."""
        if not self.auth_token or current_milli_time() > self.token_expiration:
            self.get_new_auth_token()

        return self.auth_token

    def get_new_auth_token(self):
        """Request a new authentication token from the API."""
        params = {
            'grant_type': 'client_credentials'
        }

        headers = {
            'Authorization': 'Basic ' + base64.b64encode(
                bytes(self.api_key + ':' + self.shared_secret, 'utf-8')).decode('utf-8')
        }

        response = self.post(self.auth_url, headers, data=params)
        response_json = json.loads(response.text)

        if 'access_token' in response_json:
            self.auth_token = response_json['access_token']
            self.token_expiration = current_milli_time() + (int(response_json['expiresIn']) * 1000)
        else:
            raise ValueError(
                'An error occurred getting authorization info, please check your api key and shared secret.')

    def post(self, url, headers=None, data=None):
        """Send a POST request to the specified URL."""
        if headers is None:
            headers = {}
        if self.app_id:
            headers['x-pb-appid'] = self.app_id
        response = requests.post(url=url, data=data, headers=headers)
        return response

    def get(self, url, headers=None, params=None):
        """Send a GET request to the specified URL."""
        if headers is None:
            headers = {}
        if self.app_id:
            headers['x-pb-appid'] = self.app_id
        response = requests.get(url, stream=True, headers=headers, params=params)
        return response


def unzip(path, zip_filename):
    """Extract a ZIP file to the specified path if the directory is empty."""
    with ZipFile(zip_filename, 'r') as handle:
        if not os.listdir(path):
            logging.info(f"Extracting {zip_filename} to {path} ...")
            handle.extractall(path=path)
            logging.info(f"Extraction completed for {zip_filename} at {path}")
        else:
            logging.info(f"Skipping extraction to {path} as directory is not empty.")


def get_argument_parser():
    """Parse command-line arguments for the reference data extractor."""
    parser = argparse.ArgumentParser(description='Interacts with the Digital Data Delivery API.')
    parser.add_argument('--pdx-api-key', dest='pdx_api_key',
                        help='The API key provided by the Software and Data Marketplace portal.',
                        required=True)
    parser.add_argument('--pdx-api-secret', dest='pdx_api_secret',
                        help='The shared secret provided by the Software and Data Marketplace portal.',
                        required=True)
    parser.add_argument('--local-path', dest='local_path',
                        help='The base path for downloading and extracting spds locally.')
    parser.add_argument('--dest-path',
                        dest='dest_path',
                        help='The mount base path for extracting SPDs')
    parser.add_argument('--fail-fast',
                        dest='fail_fast',
                        help='The fail fast argument validates all the provided input address string first and fail if any one of the provided data string is incorrect or not accessible.',
                        default=False)
    parser.add_argument('--timestamp',
                        dest='timestamp',
                        help='The numerical timestamp folder value where all of the data is present.',
                        default=str(time.strftime("%Y%m%d%H%M")))
    parser.add_argument('--data-mapping',
                        dest='data_mapping',
                        help='Mapping of data in the form of dictionary',
                        default=FUNCTIONALITY_SPD_MAPPING,
                        type=json.loads,
                        required=False)
    return parser.parse_args()


def get_products(spd_list):
    """Get product delivery information from SPD list."""
    product_list = []
    for spd in spd_list:
        pieces = spd.split('#')
        product_name = pieces[0]
        geography = pieces[1]
        roster_gran = pieces[2]
        data_format = pieces[3]
        by_latest = True
        vintage = None
        if len(pieces) > 4:
            by_latest = False
            vintage = pieces[4]

        search_results = client.get_deliveries(
            product_name, geography, roster_gran, 1, None, None, data_format, latest=by_latest
        )
        if not search_results.get('deliveries'):
            raise ValueError(
                f'Deliveries are not available for the product: `{product_name}` of the spd: `{spd}`.'
            )
        for delivery_info in search_results['deliveries']:
            if vintage is None or vintage == delivery_info['vintage']:
                product_list.append((product_name, delivery_info['downloadUrl']))

    return product_list


def download_spds_to_local(products_list, spd_base_path):
    """Download SPD files from product URLs to local path."""
    for name, url in products_list:
        download_file_name = re.sub(r'.*/(.+)\?.*', r'\1', url)
        file_path = os.path.join(spd_base_path, download_file_name)
        if not os.path.isfile(file_path):
            logging.info(f'Downloading {download_file_name} to {file_path} ...')
            urllib.request.urlretrieve(url, file_path)
            logging.info(f'Download complete for {download_file_name} at {file_path}')


def extract_spds_to_mount_path(spd_source_path, extract_base_path, timestamp_folder):
    """Extract SPD files to mount path with vintage and qualifier subdirectories."""
    for filename in os.listdir(spd_source_path):
        spd_file_path = os.path.join(spd_source_path, filename)
        if filename.endswith('.spd'):
            with ZipFile(spd_file_path, "r") as zip_ref:
                data = zip_ref.read('metadata.json')
                metadata = json.loads(data)
                extract_path_spd = os.path.join(
                    extract_base_path,
                    timestamp_folder,
                    metadata['vintage'],
                    metadata['qualifier']
                )
                os.makedirs(extract_path_spd, exist_ok=True)
            unzip(extract_path_spd, spd_file_path)

def is_positive_integer(input_string):
    """Check if the input string represents a positive integer."""
    pattern = r"^[1-9]\d*$"
    return re.match(pattern, input_string)


# Configure logging with timestamp and severity level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

args = get_argument_parser()

PDX_API_KEY = args.pdx_api_key
PDX_SECRET = args.pdx_api_secret
LOCAL_PATH = args.local_path
FUNCTIONALITY_MAPPING = args.data_mapping
date_folder = args.timestamp

if not is_positive_integer(date_folder):
    logging.error("The timestamp folder value where all of the data is present should be numeric and positive.")
    sys.exit(1)

if not FUNCTIONALITY_MAPPING:
    FUNCTIONALITY_MAPPING = FUNCTIONALITY_SPD_MAPPING

if not LOCAL_PATH:
    LOCAL_PATH = os.getcwd()

client = DataDeliveryClient(PDX_API_KEY, PDX_SECRET, "BIGDATA-REFERENCE-DATA-SETUP")

extract_path = args.dest_path
if not args.dest_path:
    extract_path = "/mnt/data/geoaddressing-data"
spd_path = os.path.join(LOCAL_PATH, "spds")

logging.info(f"Prepared ConfigMap for Reference Data Installation: {FUNCTIONALITY_MAPPING}")

FAIL_FAST_ENABLED = args.fail_fast

logging.info(f"Current timestamp folder where the reference data will be installed is: {date_folder}")

os.makedirs(spd_path, exist_ok=True)
os.makedirs(extract_path, exist_ok=True)

for addressing_type, spd_list in FUNCTIONALITY_MAPPING.items():
    logging.info(f"Reference data setup for `{addressing_type}` functionality is in progress ...")
    addressing_type_spd_path = os.path.join(spd_path, addressing_type)
    addressing_type_extract_path = os.path.join(extract_path, addressing_type)
    os.makedirs(addressing_type_spd_path, exist_ok=True)
    os.makedirs(addressing_type_extract_path, exist_ok=True)

    try:
        logging.info(f"Getting products for `{addressing_type}` functionality ...")
        products = get_products(spd_list)
        if not products:
            raise ValueError(
                "Either no Deliveries available for provided OR validate the parameters. "
                "To request access to the particular data, please visit https://data.precisely.com/"
            )

        download_spds_to_local(products, addressing_type_spd_path)

        spds = os.listdir(addressing_type_spd_path)
        if not spds:
            raise ValueError(
                f"No spds available to extract for {addressing_type}, "
                f"please check if the pdx data is accessible."
            )

        extract_spds_to_mount_path(addressing_type_spd_path, addressing_type_extract_path, date_folder)

        logging.info(f'Reference data setup for `{addressing_type}` is completed successfully!')
        logging.info(f'Deleting local directories of spds as extraction is complete: {addressing_type_spd_path}')
        try:
            subprocess.check_output(f'rm -rf {addressing_type_spd_path}', shell=True)
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Unable to delete {addressing_type_spd_path} -> Exception: {e}, Output: {e.output}, "
                f"StdOut: {e.stdout}, StdErr: {e.stderr}"
            )
    except Exception as ex:
        logging.error(f'Error in data setup for {addressing_type}: {ex}')
        logging.error(
            f'Data download and extraction process is not successful for the functionality: {addressing_type}. '
            f'Please run the setup again for {addressing_type} by fixing the issues and using the same timestamp.'
        )
        if FAIL_FAST_ENABLED:
            sys.exit(1)

# Final cleanup: remove all temporary SPD files
try:
    logging.info('Reference data setup is completed!')
    logging.info(f'Deleting local directory of spd as extraction is complete: {spd_path}')
    subprocess.check_output(f'rm -rf {spd_path}', shell=True)
except subprocess.CalledProcessError as e:
    logging.error(
        f"Unable to delete {spd_path} -> Exception: {e}, Output: {e.output}, StdOut: {e.stdout}, StdErr: {e.stderr}"
    )

