from setuptools import setup, find_packages

PROJECT_AUTHOR = "Alfonso Brown"
PROJECT_EMAIL = "alfonso.gonzalez@casai.com"
PROJECT_PACKAGE_NAME = "casai_pictures"

DOWNLOAD_URL = ""

MIN_PY_VERSION = "3.6.0"

REQUIRES = [
    "cachetools==4.1.0",
    "certifi==2020.6.20",
    "chardet==3.0.4",
    "docopt==0.6.2",
    "httplib2==0.18.1",
    "idna==2.9",
    "oauthlib==3.1.0",
    "Pillow==8.4.0",
    "protobuf==3.12.2",
    "pyasn1==0.4.8",
    "pyasn1-modules==0.2.8",
    "PyDrive2==1.10.0",
    "pytz==2020.1",
    "requests==2.27.1",
    "requests-oauthlib==1.3.0",
    "requests-toolbelt==0.9.1",
    "rsa==4.6",
    "setuptools==47.3.1",
    "six==1.15.0",
    "uritemplate==3.0.1",
    "urllib3==1.26.9",
]

setup(
    name=PROJECT_PACKAGE_NAME,
    version="0.0.3",
    download_url=DOWNLOAD_URL,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=find_packages(),
    install_requires=REQUIRES,
    python_requires=">={}".format(MIN_PY_VERSION),
    test_suite="tests",
    entry_points={"console_scripts": ["pic_upload = casai_pictures.main:main"]},
)