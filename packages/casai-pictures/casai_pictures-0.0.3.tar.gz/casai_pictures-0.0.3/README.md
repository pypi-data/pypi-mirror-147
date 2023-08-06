# Casai Pictures Upload Script

Script to upload Casai Pictures, downloading them from Google Drive.

## Installation

This script requires Python 3.8+.

To install the script, run:

```
pip install casai_pictures
```

Alternatively, it can be installed through this repo, by running:
```buildoutcfg
git clone https://github.com/casai-org/pictures_upload.git
cd pictures_upload
python setup.py develop
```

## Authentication

In order for the script to work, you must include a file named `client_secrets.json` 
in the working directory that contains the OAuth2 Client Key ID and secret of the Google Drive API.
This file can be obtained from the Google Cloud Platform Console, under Credentials and OAuth2.0 Cliend IDs.

Once the credentials file is set, the first time the script runs it will show two authentication prompts.
The first prompt will be to authenticate to Google Drive, opening a website and completing the oauth2 flow.
The second prompt will be to authenticate to Casai's backend, directly putting the username and password into the terminal.

## Usage

Script can be run in 3 ways:

### Single listing:

This way involves knowing the Casai Listing ID to which the pictures will be uploaded.

```
pic_upload --listing={listing_id} [--folder={folder_id}] [--rename] [--prod]
```

When no `folder_id` is specified, the cached pictures in the `temp_pictures` directory will be uploaded.

### All listings inside a building:

This way involves knowing the Casai Building ID to which the listings belong.

```
pic_upload building --id={building_id} --folder={folder_id} [--rename] [--prod] [-n]
```


### All listings:

```
pic_upload all --folder={folder_id} [--rename] [--prod] [-n]
```


### Options

Some of the common options for running the script are:

| Command Flag            | Option                                                                                                                               |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `--casai_creds={path}`  | Optional path where the `casai_creds.json` is located. Default: working directory                                                    |
| `--drive_creds={path}`  | Optional path where the `drive_creds.json` is located. Default: working directory                                                    |
| `--drive-upload`        | Uploads the compressed and re-formatted pictures into a Web folder in Drive.                                                         |
| `--format={format}`     | Format in which the pictures should be uploaded. Default: `webp`                                                                     |
| `-h --help`             | Shows the command help dialog.                                                                                                       |
| `-p --prod`             | If the flag is set, the pictures are uploaded to production environment.                                                             |
| `-n --new`              | Upload only pictures for the listings that have less than 2 pictures.                                                                |
| `--rename`              | Ensures that the files are renamed so that they are ordered by natural language. (e.g. 2 goes before 10)                             |
| `--resume={listing_id}` | Resumes running the script from the given Casai ID. Example: `--resume=4`                                                            |
| `--skip={listing_ids}`  | Skips the given list of comma-separated Casai ID of listings when running the `building` and `all` commands. Example: `--skip=1,2,3` |

