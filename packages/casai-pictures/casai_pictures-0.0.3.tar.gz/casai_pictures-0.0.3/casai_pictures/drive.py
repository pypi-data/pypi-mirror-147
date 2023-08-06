import re

from pydrive2.auth import AuthenticationError, GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError, GoogleDriveFile


class DriveDownloader:

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_code = None
        self.access_token = None
        self.refresh_token = None
        self.gauth = None
        self.drive = None

    def initialize(self, file):
        """
        Login to Google Drive.
        """
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile(file)
        try:
            self.gauth.Authorize()
        except AuthenticationError:
            self.gauth.LocalWebserverAuth()
            self.gauth.SaveCredentialsFile(file)
        self.drive = GoogleDrive(self.gauth)
        return self.drive

    async def get_files_in_folder(self, folder_id):
        """
        Get all the files in a Drive Folder and store them in folder_name.
        """
        try:
            file_list = self.drive.ListFile(
                {"q": "'{}' in parents and trashed=false".format(folder_id)}
            ).GetList()
            sortable_list = [SortableGoogleDriveFile(file) for file in file_list]
            return sorted(sortable_list)
        except ApiRequestError:
            print("Error Downloading Files from folder in Drive!")
            return []

    def find_folder(self, folder_name, parent_folder_id):
        """
        Look for a given folder name within a folder id.
        """
        file_list = self.drive.ListFile(
            {"q": "'{}' in parents and trashed=false".format(parent_folder_id)}
        ).GetList()
        for file in file_list:
            if file["mimeType"] == "application/vnd.google-apps.folder" \
                    and file["title"] == folder_name:
                return file["id"]
        return None

    def create_web_folder(self, folder_name, parent_folder_id):
        """
        Create a Web folder to upload all the new format pictures to.
        """
        file_list = self.drive.ListFile(
            {"q": "'{}' in parents and trashed=false".format(parent_folder_id)}
        ).GetList()
        for file in file_list:
            if file["mimeType"] == "application/vnd.google-apps.folder" \
                    and file["title"] == folder_name:
                # If folder already exists, delete it and all its content.
                file.Delete()
        folder = self.drive.CreateFile({
            "title": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"id": parent_folder_id}]
        })
        folder.Upload()
        return folder["id"]

    def upload_picture_to_folder(
        self,
        file_path,
        parent_folder_id,
        image_format="webp",
    ):
        """
        Upload a picture to the given parent folder.
        """
        try:
            filename = file_path.split("/")[-1]
            picture = self.drive.CreateFile({
                "title": filename,
                "mimeType": "image/{}".format(image_format),
                "parents": [{"id": parent_folder_id}],
            })
            picture.SetContentFile(file_path)
            picture.Upload()
            return picture["id"]
        except ApiRequestError:
            print("Error Uploading File {} to folder in Drive!".format(file_path))
            return None

    def save_to_local(self, file, path):
        """"""
        try:
            file.GetContentFile(path)
            return True
        except ApiRequestError:
            print("Failed to download {}".format(file["title"]))
            return False


class SortableGoogleDriveFile(GoogleDriveFile):

    def __init__(self, file, *args, **kwargs):
        self.file = file
        super().__init__(*args, **kwargs)

    def __lt__(self, other):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        self_title = self.file["title"].replace("(", "").replace(")", "")
        other_title = other.file["title"].replace("(", "").replace(")", "")
        return alphanum_key(self_title) < alphanum_key(other_title)

    def __repr__(self):
        return self.file["title"]
