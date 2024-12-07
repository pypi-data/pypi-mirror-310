[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=alert_status)](https://sonarcloud.io/summary?id=sdk-python-object-storage-management)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sdk-python-object-storage-management)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-object-storage-management)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-object-storage-management)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-object-storage-management)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-object-storage-management&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sdk-python-object-storage-management)
[![Release](https://img.shields.io/github/v/release/ionos-cloud/sdk-python-object-storage-management.svg)](https://github.com/ionos-cloud/sdk-python-object-storage-management/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/ionos-cloud/sdk-python-object-storage-management.svg)](https://github.com/ionos-cloud/sdk-python-object-storage-management/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/ionoscloud-object-storage-management)](https://pypi.org/project/ionoscloud-object-storage-management/)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")


# Python API client for ionoscloud_object_storage_management

Object Storage Management API is a RESTful API that manages the object storage
service configuration for IONOS Cloud.


## Overview
The IONOS Cloud SDK for Python provides you with access to the IONOS Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. All API operations are performed over SSL and authenticated using your IONOS Cloud portal credentials. The API can be accessed within an instance running in IONOS Cloud or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.


### Installation & Usage

**Requirements:**
- Python >= 3.5

### pip install

Since this package is hosted on [Pypi](https://pypi.org/) you can install it by using:

```bash
pip install ionoscloud-object-storage-management
```

If the python package is hosted on a repository, you can install directly using:

```bash
pip install git+https://github.com/ionos-cloud/sdk-python-object-storage-management.git
```

Note: you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ionos-cloud/sdk-python-object-storage-management.git`

Then import the package:

```python
import ionoscloud_object_storage_management
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python setup.py install --user
```

or `sudo python setup.py install` to install the package for all users

Then import the package:

```python
import ionoscloud_object_storage_management
```

> **_NOTE:_**  The Python SDK does not support Python 2. It only supports Python >= 3.5.

### Authentication

All available server URLs are:

- *https://s3.ionos.com* - Production

By default, *https://s3.ionos.com* is used, however this can be overriden at authentication, either
by setting the `IONOS_API_URL` environment variable or by specifying the `host` parameter when
initializing the sdk client.

The username and password **or** the authentication token can be manually specified when initializing the SDK client:

```python
configuration = ionoscloud_object_storage_management.Configuration(
                username='YOUR_USERNAME',
                password='YOUR_PASSWORD',
                token='YOUR_TOKEN',
                host='SERVER_API_URL'
                )
client = ionoscloud_object_storage_management.ApiClient(configuration)
```

Environment variables can also be used. This is an example of how one would do that:

```python
import os

configuration = ionoscloud_object_storage_management.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                token=os.environ.get('IONOS_TOKEN'),
                host=os.environ.get('IONOS_API_URL')
                )
client = ionoscloud_object_storage_management.ApiClient(configuration)
```

**Warning**: Make sure to follow the Information Security Best Practices when using credentials within your code or storing them in a file.


### HTTP proxies

You can use http proxies by setting the following environment variables:
- `IONOS_HTTP_PROXY` - proxy URL
- `IONOS_HTTP_PROXY_HEADERS` - proxy headers

Each line in `IONOS_HTTP_PROXY_HEADERS` represents one header, where the header name and value is separated by a colon. Newline characters within a value need to be escaped. See this example:
```
Connection: Keep-Alive
User-Info: MyID
User-Group: my long\nheader value
```


### Changing the base URL

Base URL for the HTTP operation can be changed in the following way:

```python
import os

configuration = ionoscloud_object_storage_management.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                host=os.environ.get('IONOS_API_URL'),
                server_index=None,
                )
client = ionoscloud_object_storage_management.ApiClient(configuration)
```

## Certificate pinning:

You can enable certificate pinning if you want to bypass the normal certificate checking procedure,
by doing the following:

Set env variable IONOS_PINNED_CERT=<insert_sha256_public_fingerprint_here>

You can get the sha256 fingerprint most easily from the browser by inspecting the certificate.


## Documentation for API Endpoints

All URIs are relative to *https://s3.ionos.com*
<details >
    <summary title="Click to toggle">API Endpoints table</summary>


| Class | Method | HTTP request | Description |
| ------------- | ------------- | ------------- | ------------- |
| AccesskeysApi | [**accesskeys_delete**](docs/api/AccesskeysApi.md#accesskeys_delete) | **DELETE** /accesskeys/{accesskeyId} | Delete AccessKey |
| AccesskeysApi | [**accesskeys_find_by_id**](docs/api/AccesskeysApi.md#accesskeys_find_by_id) | **GET** /accesskeys/{accesskeyId} | Retrieve AccessKey |
| AccesskeysApi | [**accesskeys_get**](docs/api/AccesskeysApi.md#accesskeys_get) | **GET** /accesskeys | Retrieve all Accesskeys |
| AccesskeysApi | [**accesskeys_post**](docs/api/AccesskeysApi.md#accesskeys_post) | **POST** /accesskeys | Create AccessKey |
| AccesskeysApi | [**accesskeys_put**](docs/api/AccesskeysApi.md#accesskeys_put) | **PUT** /accesskeys/{accesskeyId} | Ensure AccessKey |
| AccesskeysApi | [**accesskeys_renew**](docs/api/AccesskeysApi.md#accesskeys_renew) | **PUT** /accesskeys/{accesskeyId}/renew | Ensure AccessKey |
| RegionsApi | [**regions_find_by_region**](docs/api/RegionsApi.md#regions_find_by_region) | **GET** /regions/{region} | Retrieve Region |
| RegionsApi | [**regions_get**](docs/api/RegionsApi.md#regions_get) | **GET** /regions | Retrieve all Regions |

</details>

## Documentation For Models

All URIs are relative to *https://s3.ionos.com*
<details >
<summary title="Click to toggle">API models list</summary>

 - [AccessKey](docs/models/AccessKey)
 - [AccessKeyCreate](docs/models/AccessKeyCreate)
 - [AccessKeyEnsure](docs/models/AccessKeyEnsure)
 - [AccessKeyRead](docs/models/AccessKeyRead)
 - [AccessKeyReadList](docs/models/AccessKeyReadList)
 - [AccessKeyReadListAllOf](docs/models/AccessKeyReadListAllOf)
 - [Bucket](docs/models/Bucket)
 - [BucketCreate](docs/models/BucketCreate)
 - [BucketEnsure](docs/models/BucketEnsure)
 - [BucketRead](docs/models/BucketRead)
 - [BucketReadList](docs/models/BucketReadList)
 - [BucketReadListAllOf](docs/models/BucketReadListAllOf)
 - [Error](docs/models/Error)
 - [ErrorMessages](docs/models/ErrorMessages)
 - [Links](docs/models/Links)
 - [Metadata](docs/models/Metadata)
 - [MetadataWithStatus](docs/models/MetadataWithStatus)
 - [MetadataWithStatusAllOf](docs/models/MetadataWithStatusAllOf)
 - [MetadataWithSupportedRegions](docs/models/MetadataWithSupportedRegions)
 - [MetadataWithSupportedRegionsAllOf](docs/models/MetadataWithSupportedRegionsAllOf)
 - [Pagination](docs/models/Pagination)
 - [Region](docs/models/Region)
 - [RegionCapability](docs/models/RegionCapability)
 - [RegionCreate](docs/models/RegionCreate)
 - [RegionEnsure](docs/models/RegionEnsure)
 - [RegionRead](docs/models/RegionRead)
 - [RegionReadList](docs/models/RegionReadList)
 - [RegionReadListAllOf](docs/models/RegionReadListAllOf)
 - [StorageClass](docs/models/StorageClass)
 - [StorageClassCreate](docs/models/StorageClassCreate)
 - [StorageClassEnsure](docs/models/StorageClassEnsure)
 - [StorageClassRead](docs/models/StorageClassRead)
 - [StorageClassReadList](docs/models/StorageClassReadList)
 - [StorageClassReadListAllOf](docs/models/StorageClassReadListAllOf)


[[Back to API list]](#documentation-for-api-endpoints) [[Back to Model list]](#documentation-for-models)

</details>
