"""
Casai Pictures Upload

Usage:
  pic_upload (--listing=<listing_id> | --building=<building_id>) (--folder=<folder_id>) [options]
  pic_upload all (--folder=<folder_id>) [--resume=<listing_id>] [options]
  pic_upload building (--id=<building_id>) (--folder=<folder_id>) [--resume=<listing_id>] [options]

Options:
  -h --help                     Show this screen.
  -p --prod                        If set, the photos will be uploaded to the production
                                backend. If not, they will be uploaded to staging.
  --folder=<folder_id>          Id of the folder in Google Drive. If not specified,
                                skip download, and use the pictures
                                stored in temp_pictures.
  --format=<file_extension>     Format in which the images should be uploaded (default: webp).
  --skip=<listing_ids>          Comma separated list of listing_ids that should be skipped.
  --resume=<listing_id>         Used to resume script from one listing if it was previously interrupted.
  --drive_creds=<file_path>     Path of the drive credentials file.
  --casai_creds=<file_path>     Path of the casai credentials file.
  -r --rename                   Rename the Pictures in Google Drive to correctly order
                                them by name.
  --drive-upload                Upload the compressed files to the "Web" folder in drive.
  -n --new                      Only upload pictures of new units, that have no pictures currently.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Coroutine, List, Tuple, Union

import PIL
import docopt
import os
import shutil
from datetime import datetime

import casai_pictures.drive as downloader
import casai_pictures.casai as uploader
import casai_pictures.utils as utils

DEFAULT_DRIVE_CREDS_PATH = "drive_creds.json"
DEFAULT_CASAI_CREDS_PATH = "casai_creds.json"
DEFAULT_COMPRESSED_PICTURES_FOLDER = "compressed_originals"
DEFAULT_NEW_FORMAT_PICTURES_FOLDER = "new_format"
DEFAULT_WEB_FOLDER_NAME = "Web"

num_pictures_per_listing = dict()
listings_download_stack = dict()
listings_upload_stack = dict()
stored_files = 0
success_count = 0
not_found = []
errors = set()
failed_tasks = []
logger = logging.getLogger(__name__)


def parse_args() -> dict:
    args = docopt.docopt(__doc__)
    print("\n================ Casai Pictures Update ================\n")

    is_prod = args["--prod"]
    casai_config = args.get("--casai_creds") or DEFAULT_CASAI_CREDS_PATH
    drive_config = args.get("--drive_creds") or DEFAULT_DRIVE_CREDS_PATH

    all_listings = args["all"]
    of_building = args["building"]

    return {
        "is_prod": is_prod,
        "casai_config": casai_config,
        "drive_config": drive_config,
        "all_listings": all_listings,
        "of_building": of_building,
        "folder_id": args["--folder"],
        "skip": args["--skip"],
        "resume": args["--resume"],
        "rename": args["--rename"],
        "new_format": args["--format"],
        "drive_upload": args["--drive-upload"],
        "listing_id": args["--listing"],
        "building_id": args["--id"] if of_building else args["--building"],
        "only_new": args["--new"]
    }


async def initialize(casai_config, drive_config, stage):
    """
    Initialize Casai API and Drive API credentials.
    """
    casai_api = uploader.CasaiAPI(stage)
    casai_api.initialize(casai_config)

    drive_downloader = downloader.DriveDownloader()
    drive_downloader.initialize(drive_config)
    return casai_api, drive_downloader


async def create_all_listings_task(
    casai_api: uploader.CasaiAPI,
    drive_downloader: downloader.DriveDownloader,
    skip: str,
    resume: Union[int, str],
    folder_id: str,
    only_new: bool = False,
    **kwargs,
) -> List[Tuple[str, Coroutine]]:
    """Run the script for all active listings."""
    global stored_files, listings_download_stack, listings_upload_stack
    print("Getting all Active Listings...")
    if skip:
        skip = skip.split(",")
    if isinstance(resume, str):
        resume = int(resume)

    listing_ids, listing_nicknames = casai_api.get_listings_data(
        skip=skip, resume=resume, only_new=only_new,
    )
    tasks = []
    for listing_id, nickname in zip(listing_ids, listing_nicknames):

        listing_folder_id = drive_downloader.find_folder(nickname, folder_id)
        if listing_folder_id is None:
            print("Listing '{}' folder not found".format(nickname))
            not_found.append(nickname)
            continue

        listings_download_stack[nickname] = set()
        listings_upload_stack[nickname] = set()
        tasks.append(
            (
                nickname,
                download_and_upload(
                    drive_downloader,
                    casai_api,
                    listing_id,
                    None,
                    nickname,
                    listing_folder_id,
                    **kwargs,
                )
            )
        )
    return tasks


async def create_of_building_task(
    casai_api: uploader.CasaiAPI,
    drive_downloader: downloader.DriveDownloader,
    skip: str,
    resume: Union[int, str],
    folder_id: str,
    building_id: int,
    only_new: bool = False,
    **kwargs,
) -> List[Tuple[str, Coroutine]]:
    """Run the script for all the listings in a building."""
    global stored_files, listings_download_stack, listings_upload_stack
    print("Getting all Active Listings of Building {}...".format(building_id))
    if skip:
        skip = skip.split(",")
    if isinstance(resume, str):
        resume = int(resume)

    kwargs.pop("listing_id", None)
    listing_ids, listing_nicknames = casai_api.get_listings_data(
        skip=skip, resume=resume, building_id=building_id, only_new=only_new,
    )
    tasks = []
    for listing_id, nickname in zip(listing_ids, listing_nicknames):
        listing_folder_id = drive_downloader.find_folder(nickname, folder_id)
        if listing_folder_id is None:
            print("Listing '{}' folder not found".format(nickname))
            not_found.append(nickname)
            continue

        listings_download_stack[nickname] = set()
        listings_upload_stack[nickname] = set()
        tasks.append(
            (
                nickname,
                download_and_upload(
                    drive_downloader,
                    casai_api,
                    listing_id,
                    None,
                    nickname,
                    listing_folder_id,
                    **kwargs,
                )
            )
        )
    return tasks


async def create_single_object_task(
    casai_api: uploader.CasaiAPI,
    drive_downloader: downloader.DriveDownloader,
    folder_id: str,
    listing_id: Union[int, str, None] = None,
    building_id: Union[int, str, None] = None,
    **kwargs,
) -> Tuple[str, Coroutine]:
    global stored_files, listings_download_stack, listings_upload_stack
    casai_id, nickname = None, None
    if listing_id and not building_id:
        casai_id, nickname = casai_api.get_listing_nickname(listing_id)
        if casai_id is None or nickname is None:
            print("Listing not found!")
            exit(1)
    elif building_id and not listing_id:
        nickname = casai_api.get_building_name(building_id)
        if nickname is None:
            print("Building not found!")
            exit(1)
    else:
        print("No valid upload option!")
        exit(1)
    listings_download_stack[nickname] = set()
    listings_upload_stack[nickname] = set()
    return (
        nickname,
        download_and_upload(
            drive_downloader,
            casai_api,
            casai_id,
            building_id,
            nickname,
            folder_id,
            **kwargs
        )
    )


async def download_and_upload(
    drive_downloader,
    casai_api,
    listing_id,
    building_id,
    nickname,
    folder_id,
    rename=False,
    new_format="webp",
    drive_upload=False,
    **kwargs,
):
    """
    Download pictures from Google Drive and upload them to Casai Website.
    """
    if folder_id:
        web_folder_id = drive_downloader.create_web_folder(
            DEFAULT_WEB_FOLDER_NAME, folder_id,
        )
        if listing_id:
            pictures_reset = await utils.async_to_sync(
                casai_api.reset_listing_pictures,
                listing_id,
            )
        elif building_id:
            pictures_reset = await utils.async_to_sync(
                casai_api.reset_building_pictures,
                building_id,
            )
        else:
            pictures_reset = False
        if not pictures_reset:
            print("\nFailed to Reset pictures of listing {}".format(nickname))
            return
        download_task = asyncio.create_task(download_from_folder(
            drive_downloader,
            nickname,
            folder_id,
            rename=rename,
        ))
        upload_task = asyncio.create_task(upload_from_folder(
            drive_downloader,
            casai_api,
            listing_id,
            building_id,
            nickname,
            web_folder_id,
            new_format=new_format,
            drive_upload=drive_upload,
        ))
        download_task.set_name("{}_download".format(nickname))
        upload_task.set_name("{}_upload".format(nickname))


async def download_from_folder(
    drive_downloader,
    nickname,
    folder_id,
    rename=False,
    **kwargs,
):
    global listings_download_stack, stored_files, num_pictures_per_listing

    print("\nAttempting download for listing '{}'".format(nickname))

    if folder_id:
        files = await drive_downloader.get_files_in_folder(folder_id)
        num_pictures_per_listing[nickname] = len(files)

        for sortable_file in files:
            file = sortable_file.file
            if "image" not in file["mimeType"]:
                num_pictures_per_listing[nickname] -= 1
                continue
            local_filename = file["title"].replace(" ", "")
            if rename:
                if "Copyof" in local_filename:
                    local_filename = local_filename.replace("Copyof", "")
                    file["title"] = local_filename
                    file.Upload()
                filename, file_extension = os.path.splitext(local_filename)
                name_parts = filename.split("-")
                try:
                    order = 1000 + int(name_parts[-1])
                    name_parts[-1] = str(order)
                except Exception:
                    pass
                nickname_wo_spaces = nickname.replace(" ", "")
                new_filename = nickname_wo_spaces + "-".join(name_parts) + "" + file_extension
                if new_filename != local_filename:
                    local_filename = new_filename

            file_path = "%s/%s" % (DEFAULT_COMPRESSED_PICTURES_FOLDER, local_filename)

            downloaded = await utils.async_to_sync(drive_downloader.save_to_local, file, file_path)
            if downloaded:
                listings_download_stack[nickname].add(file_path)
                stored_files += 1
                print(
                    f"Done Downloading: {file['title']}, id: {file['id']} "
                    f"with name: {local_filename}"
                )
            else:
                num_pictures_per_listing[nickname] -= 1


async def upload_from_folder(
    drive_downloader,
    casai_api,
    listing_id,
    building_id,
    nickname,
    web_folder_id,
    new_format="webp",
    drive_upload=False,
    **kwargs,
):
    """
    Download all the pictures in a Drive folder, and upload them to Casai Backend.
    """
    global success_count,\
        not_found,\
        errors,\
        listings_download_stack,\
        listings_upload_stack,\
        stored_files,\
        num_pictures_per_listing

    print(
        f"\nAttempting upload of {num_pictures_per_listing[nickname]} "
        f"pictures for listing '{nickname}'"
    )
    file_extension = new_format
    while (
        len(listings_download_stack[nickname]) < num_pictures_per_listing[nickname]
        or listings_download_stack[nickname] != listings_upload_stack[nickname]
    ):

        if len(listings_download_stack[nickname]) <= len(listings_upload_stack[nickname]):
            await asyncio.sleep(0.5)
            continue
        filename = None
        for file in sorted(listings_download_stack[nickname]):
            if file in listings_upload_stack[nickname]:
                continue
            filename = file
            break
        if filename is None:
            continue

        error_file = await compress_and_upload(
            filename,
            drive_downloader,
            casai_api,
            listing_id,
            building_id,
            web_folder_id,
            file_extension,
            drive_upload=drive_upload,
        )
        if error_file is None:
            success_count += 1
            listings_upload_stack[nickname].add(filename)
            if os.path.isfile(filename) or os.path.islink(filename):
                os.unlink(filename)
                stored_files -= 1
        else:
            errors.add(error_file)
            listings_download_stack[nickname].remove(filename)
    print(f"\nFinished uploading {nickname}!\n")


async def compress_and_upload(
    filename,
    drive_downloader,
    casai_api,
    listing_id,
    building_id,
    web_folder_id,
    file_extension,
    drive_upload=False,
    **kwargs,
):
    """
    Compress the given image, change its format, and upload to Casai Backend.
    """
    print("Compressing and uploading: {}".format(filename))

    try:
        original_compressed, new_format_path = await compress_and_format(
            filename, file_extension
        )
    except PIL.UnidentifiedImageError:
        original_compressed = new_format_path = None
    if original_compressed is None or new_format_path is None:
        print("Error while compressing file: {}".format(filename))
        return filename

    tasks = [
        asyncio.create_task(
            utils.async_to_sync(
                casai_api.upload_picture,
                new_format_path,
                original_compressed,
                (file_extension or "webp"),
                "jpeg",
                False,
                listing_id,
                building_id,
            )
        )
    ]
    if drive_upload:
        tasks.append(
            asyncio.create_task(
                upload_to_drive(
                    drive_downloader,
                    new_format_path,
                    web_folder_id,
                    file_extension,
                )
            )
        )

    results = await asyncio.gather(*tasks)

    if not results[0]:
        print("Error uploading file: {}".format(filename))
        return filename

    if os.path.isfile(new_format_path) or os.path.islink(new_format_path):
        os.unlink(new_format_path)
    return None


async def compress_and_format(
    filename,
    file_extension,
    **kwargs,
):
    """
    Reduce a picture's quality and change its format.
    """
    original_compressed = await utils.async_to_sync(
        utils.compress_original_format, filename,
    )
    if original_compressed is None:
        return None, None

    new_format = await utils.async_to_sync(
        utils.change_picture_format,
        DEFAULT_NEW_FORMAT_PICTURES_FOLDER,
        original_compressed,
        (file_extension or "webp"),
    )
    if new_format is None:
        return None, None

    new_format_path = os.path.join("{}/".format(DEFAULT_NEW_FORMAT_PICTURES_FOLDER), new_format)
    return original_compressed, new_format_path


async def upload_to_drive(
    drive_downloader,
    file_path,
    folder_id,
    file_extension,
    **kwargs,
):
    """
    Async friendly coroutine for uploading a picture to a drive folder.
    """
    task = utils.async_to_sync(
        drive_downloader.upload_picture_to_folder,
        file_path,
        folder_id,
        file_extension,
    )
    await asyncio.gather(task)


async def remove_cached_photos(folder_name, **kwargs):
    """
    Delete all previously cached photos to store only the new ones.
    """
    for filename in os.listdir(folder_name):
        if filename.endswith(".py"):
            continue
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


async def async_main():
    start = datetime.now()
    print("Started at: {}".format(start))

    config = parse_args()
    casai_api, drive_downloader = await initialize(
        config["casai_config"],
        config["drive_config"],
        config["is_prod"],
    )

    await asyncio.gather(
        asyncio.create_task(remove_cached_photos(DEFAULT_COMPRESSED_PICTURES_FOLDER)),
        asyncio.create_task(remove_cached_photos(DEFAULT_NEW_FORMAT_PICTURES_FOLDER)),
    )

    if config["all_listings"]:
        coroutines = await create_all_listings_task(
            casai_api,
            drive_downloader,
            **config,
        )
    elif config["of_building"]:
        coroutines = await create_of_building_task(
            casai_api,
            drive_downloader,
            **config,
        )
    else:
        coroutines = [
            await create_single_object_task(
                casai_api,
                drive_downloader,
                **config,
            )
        ]

    for nickname, coro in coroutines:
        task = asyncio.create_task(coro)
        task.set_name(f"{nickname}_photos")

        pending_tasks = asyncio.all_tasks()
        while (
            len(pending_tasks) > 2 or
            (stored_files > 0 and (success_count == 0 and len(not_found) == 0 and len(errors) == 0))
            or (stored_files > 20)
        ):
            await asyncio.sleep(1)
            pending_tasks = asyncio.all_tasks()

    try:
        pending_tasks = asyncio.all_tasks()
        prev_pending = len(pending_tasks)
        timeout_counter = 0
        while len(pending_tasks) > 1:
            await asyncio.sleep(1)
            timeout_counter += 1
            pending_tasks = asyncio.all_tasks()
            if timeout_counter > 600 and len(pending_tasks) == prev_pending:
                current_task = asyncio.current_task()
                print(
                    f"\nTimed out running: {current_task.get_name()}\n"
                    f"Tasks remaining: {', '.join(t.get_name() for t in pending_tasks)}\n"
                )
                try:
                    current_task.cancel("Timed out!")
                except asyncio.CancelledError:
                    failed_tasks.append(current_task.get_name())
            prev_pending = len(pending_tasks)

    except KeyboardInterrupt:
        print("Interrupted!")
        pass

    now = datetime.now()
    total_time = round(now.timestamp() - start.timestamp(), 2)
    print("Finished after {}s ({}h)".format(total_time, round(total_time/3600, 2)))
    if success_count > 0:
        print("\nUploaded {} photos successfully!".format(success_count))

    if len(not_found) > 0:
        print("\nCouldn't find pictures of: {}".format(not_found))

    if len(errors) > 0:
        print("\n{} photos failed: {}".format(len(errors), errors))

    if len(failed_tasks) > 0:
        print("\nTasks failed for: {}".format(failed_tasks))

    print("\nDone!\n")


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nInterrupted!\n")


if __name__ == "__main__":
    main()
