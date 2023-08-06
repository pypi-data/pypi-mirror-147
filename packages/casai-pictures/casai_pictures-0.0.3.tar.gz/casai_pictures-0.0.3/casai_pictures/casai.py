import json
import requests
from getpass import getpass
from json import JSONDecodeError
from requests.adapters import HTTPAdapter
from requests_toolbelt import MultipartEncoder
from urllib3.util.retry import Retry

STAGING_CASAI_BASE_URL = "https://test-api.casai.com/"
PROD_CASAI_BASE_URL = "https://guesty-bridge.casai.com/"


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """
    Send a request with a retry session and backoff factor.
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class CasaiAPI:

    def __init__(self, stage, username=None, password=None):
        self.stage = stage
        self.base_url = PROD_CASAI_BASE_URL if stage else STAGING_CASAI_BASE_URL
        self.username = username
        self.password = password
        self.token = None
        self.extension = "jpeg"

    def initialize(self, file):
        """
        Initialize the Casai Pictures API.
        """
        print("Checking for stored Casai Credentials...")
        creds = {}
        try:
            with open(file, "r") as credentials:
                try:
                    creds = json.load(credentials)
                    stage = "staging" if self.stage else "prod"
                    if stage in creds:
                        self.token = creds[stage]["token"]
                        self.username = creds[stage]["username"]
                        print("Found credentials!\n")
                    else:
                        creds.update(self.request_credentials())
                except JSONDecodeError:
                    creds.update(self.request_credentials())
        except (IOError, FileNotFoundError):
            creds.update(self.request_credentials())

        with open(file, "w") as credentials:
            json.dump(creds, credentials)

    def request_credentials(self):
        """
        Request through CLI Casai Login credentials.
        """
        print("\nCasai Credentials not found, please login:\n")
        creds = {}
        username = input("Please enter your Casai Username:")
        password = getpass(prompt="Please enter your Casai Password:")
        stage = "staging" if self.stage else "prod"
        if self.login(username=username, password=password):
            creds[stage] = {
                "username": username,
                "token": self.token,
            }
        else:
            print("Invalid Authentication!")
            exit(1)
        return creds

    def login(self, username=None, password=None):
        """
        Login to Casai API.
        """
        response = requests_retry_session().post(
            self.base_url + "login/",
            json={
                "email": username or self.username,
                "password": password or self.password,
            },
            timeout=5,
        )
        if response.status_code == 200:
            self.token = response.json().get("result", {}).get("ok")
        return response.status_code == 200

    def upload_picture(
        self,
        original_file,
        backup_file,
        original_extension,
        backup_extension,
        is_backup,
        listing_id,
        building_id,
    ):
        """
        Upload the given files to the specified listing id.
        """
        try:
            data = {
                "caption": "Image",
                "original": (original_file, open(original_file, 'rb'), "image/{}".format(original_extension)),
                "backup": (backup_file, open(backup_file, 'rb'), "image/{}".format(backup_extension)),
                "is_backup": str(is_backup),
            }
            if listing_id:
                data["listing"] = str(listing_id)
            if building_id:
                data["building"] = building_id
            m = MultipartEncoder(fields=data)
            response = requests_retry_session().post(
                url=self.base_url + "pictures/",
                headers={
                    "Content-Type": m.content_type,
                    "Authorization": "Token {}".format(self.token),
                },
                data=m,
                timeout=40,
            )
            return response.status_code == 201
        except Exception as e:
            print(e)
            return False

    def reset_listing_pictures(self, listing_id):
        """
        Remove all the current pictures of a listing.
        """
        response = requests_retry_session().post(
            self.base_url + "pictures/reset/",
            json={"listing_id": listing_id},
            headers={"Authorization": "Token " + self.token}
        )
        if response.status_code != 200:
            print(response.content)
        return response.status_code == 200

    def reset_building_pictures(self, building_id):
        """
        Remove all the current pictures of a listing.
        """
        response = requests_retry_session().post(
            self.base_url + "pictures/reset/",
            json={"building_id": building_id},
            headers={"Authorization": "Token " + self.token}
        )
        if response.status_code != 200:
            print(response.content)
        return response.status_code == 200

    def get_listings_data(
        self,
        skip=None,
        listing_ids=None,
        listing_nicknames=None,
        url="",
        resume=None,
        building_id=None,
        only_new=False,
    ):
        """
        Get all the active_in_casai listings.
        """
        if skip is None:
            skip = list()
        if listing_ids is None or listing_nicknames is None:
            listing_ids = []
            listing_nicknames = []

        if not url:
            url = self.base_url + "listings_pictures/?limit=20&offset=0"
            if building_id:
                url += f"&building_id={building_id}"
            if only_new:
                url += "&no_pictures_lt=2"
        response = requests_retry_session().get(
            url,
            headers={"Authorization": "Token "+self.token},
            timeout=15,
        )
        if response.status_code != 200:
            return listing_ids, listing_nicknames
        response_data = response.json()

        for listing in response_data["results"]:
            casai_id = listing.get("casai_listing")
            nickname = listing.get("nickname").replace(" ", "")
            if str(casai_id) in skip:
                print("Skipping pictures of {}".format(nickname))
                continue
            listing_ids.append(casai_id)
            listing_nicknames.append(nickname)

        if response_data.get("next"):
            return self.get_listings_data(
                skip=skip,
                listing_ids=listing_ids,
                listing_nicknames=listing_nicknames,
                url=response_data.get("next"),
                resume=resume,
            )

        if resume is not None and isinstance(resume, int):
            try:
                resume_index = listing_ids.index(resume)
                listing_ids = listing_ids[resume_index:]
                listing_nicknames = listing_nicknames[resume_index:]
            except ValueError as e:
                print(
                    "\nListing Id {} for resuming was not found, doing all listings!\n"
                    .format(resume)
                )
        return listing_ids, listing_nicknames

    def get_listing_nickname(self, listing_id):
        """
        Get the casai_id and nickname of a given listing id.
        """
        response = requests_retry_session().get(
            self.base_url + "listings_pictures/?id={}".format(listing_id),
            headers={"Authorization": "Token " + self.token},
            timeout=15,
        )
        if response.status_code != 200:
            return None, None
        response_data = response.json().get("results", {})[0]
        return response_data.get("casai_listing"), response_data.get("nickname").replace(" ", "")

    def get_building_name(self, building_id):
        """
        Get the building name with a given id.
        """
        response = requests_retry_session().get(
            self.base_url + "buildings/?id={}".format(building_id),
            headers={"Authorization": "Token " + self.token},
            timeout=15,
        )
        if response.status_code != 200:
            return None
        response_data = response.json().get("results")[0]
        return response_data.get("name", "")
