from __future__ import absolute_import

import re  # noqa: F401
import six

from ionoscloud_object_storage_management.api_client import ApiClient
from ionoscloud_object_storage_management.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class AccesskeysApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def accesskeys_delete(self, accesskey_id, **kwargs):  # noqa: E501
        """Delete AccessKey  # noqa: E501

        Deletes the specified AccessKey.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_delete(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_delete_with_http_info(accesskey_id, **kwargs)  # noqa: E501

    def accesskeys_delete_with_http_info(self, accesskey_id, **kwargs):  # noqa: E501
        """Delete AccessKey  # noqa: E501

        Deletes the specified AccessKey.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_delete_with_http_info(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'accesskey_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_delete" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'accesskey_id' is set
        if self.api_client.client_side_validation and ('accesskey_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['accesskey_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `accesskey_id` when calling `accesskeys_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'accesskey_id' in local_var_params:
            path_params['accesskeyId'] = local_var_params['accesskey_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = None
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys/{accesskeyId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def accesskeys_find_by_id(self, accesskey_id, **kwargs):  # noqa: E501
        """Retrieve AccessKey  # noqa: E501

        Returns the AccessKey by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_find_by_id(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AccessKeyRead
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_find_by_id_with_http_info(accesskey_id, **kwargs)  # noqa: E501

    def accesskeys_find_by_id_with_http_info(self, accesskey_id, **kwargs):  # noqa: E501
        """Retrieve AccessKey  # noqa: E501

        Returns the AccessKey by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_find_by_id_with_http_info(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AccessKeyRead, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'accesskey_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_find_by_id" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'accesskey_id' is set
        if self.api_client.client_side_validation and ('accesskey_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['accesskey_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `accesskey_id` when calling `accesskeys_find_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'accesskey_id' in local_var_params:
            path_params['accesskeyId'] = local_var_params['accesskey_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'AccessKeyRead'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys/{accesskeyId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def accesskeys_get(self, **kwargs):  # noqa: E501
        """Retrieve all Accesskeys  # noqa: E501

        This endpoint enables retrieving all Accesskeys using pagination and optional filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_get(async_req=True)
        >>> result = thread.get()

        :param offset: The first element (of the total list of elements) to include in the response. Use together with limit for pagination.
        :type offset: int
        :param limit: The maximum number of elements to return. Use together with offset for pagination.
        :type limit: int
        :param filter_accesskey_id: The accesskey ID to filter by.
        :type filter_accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AccessKeyReadList
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_get_with_http_info(**kwargs)  # noqa: E501

    def accesskeys_get_with_http_info(self, **kwargs):  # noqa: E501
        """Retrieve all Accesskeys  # noqa: E501

        This endpoint enables retrieving all Accesskeys using pagination and optional filters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param offset: The first element (of the total list of elements) to include in the response. Use together with limit for pagination.
        :type offset: int
        :param limit: The maximum number of elements to return. Use together with offset for pagination.
        :type limit: int
        :param filter_accesskey_id: The accesskey ID to filter by.
        :type filter_accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AccessKeyReadList, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'offset',
            'limit',
            'filter_accesskey_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_get" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `accesskeys_get`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 1000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `accesskeys_get`, must be a value less than or equal to `1000`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `accesskeys_get`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = list(local_var_params.get('query_params', {}).items())
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'filter_accesskey_id' in local_var_params and local_var_params['filter_accesskey_id'] is not None:  # noqa: E501
            query_params.append(('filter.accesskeyId', local_var_params['filter_accesskey_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'AccessKeyReadList'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def accesskeys_post(self, access_key_create, **kwargs):  # noqa: E501
        """Create AccessKey  # noqa: E501

        Creates a new AccessKey.  The full AccessKey needs to be provided to create the object. Optional data will be filled with defaults or left empty.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_post(access_key_create, async_req=True)
        >>> result = thread.get()

        :param access_key_create: AccessKey to create. (required)
        :type access_key_create: AccessKeyCreate
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AccessKeyRead
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_post_with_http_info(access_key_create, **kwargs)  # noqa: E501

    def accesskeys_post_with_http_info(self, access_key_create, **kwargs):  # noqa: E501
        """Create AccessKey  # noqa: E501

        Creates a new AccessKey.  The full AccessKey needs to be provided to create the object. Optional data will be filled with defaults or left empty.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_post_with_http_info(access_key_create, async_req=True)
        >>> result = thread.get()

        :param access_key_create: AccessKey to create. (required)
        :type access_key_create: AccessKeyCreate
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AccessKeyRead, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'access_key_create'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_post" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'access_key_create' is set
        if self.api_client.client_side_validation and ('access_key_create' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_key_create'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_key_create` when calling `accesskeys_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'access_key_create' in local_var_params:
            body_params = local_var_params['access_key_create']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'AccessKeyRead'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def accesskeys_put(self, accesskey_id, access_key_ensure, **kwargs):  # noqa: E501
        """Ensure AccessKey  # noqa: E501

        Ensures that the AccessKey with the provided ID is created or modified. The full AccessKey needs to be provided to ensure (either update or create) the AccessKey. Non present data will only be filled with defaults or left empty, but not take previous values into consideration.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_put(accesskey_id, access_key_ensure, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param access_key_ensure: update AccessKey (required)
        :type access_key_ensure: AccessKeyEnsure
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AccessKeyRead
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_put_with_http_info(accesskey_id, access_key_ensure, **kwargs)  # noqa: E501

    def accesskeys_put_with_http_info(self, accesskey_id, access_key_ensure, **kwargs):  # noqa: E501
        """Ensure AccessKey  # noqa: E501

        Ensures that the AccessKey with the provided ID is created or modified. The full AccessKey needs to be provided to ensure (either update or create) the AccessKey. Non present data will only be filled with defaults or left empty, but not take previous values into consideration.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_put_with_http_info(accesskey_id, access_key_ensure, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey. (required)
        :type accesskey_id: str
        :param access_key_ensure: update AccessKey (required)
        :type access_key_ensure: AccessKeyEnsure
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AccessKeyRead, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'accesskey_id',
            'access_key_ensure'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_put" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'accesskey_id' is set
        if self.api_client.client_side_validation and ('accesskey_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['accesskey_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `accesskey_id` when calling `accesskeys_put`")  # noqa: E501
        # verify the required parameter 'access_key_ensure' is set
        if self.api_client.client_side_validation and ('access_key_ensure' not in local_var_params or  # noqa: E501
                                                        local_var_params['access_key_ensure'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `access_key_ensure` when calling `accesskeys_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'accesskey_id' in local_var_params:
            path_params['accesskeyId'] = local_var_params['accesskey_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'access_key_ensure' in local_var_params:
            body_params = local_var_params['access_key_ensure']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'AccessKeyRead'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys/{accesskeyId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def accesskeys_renew(self, accesskey_id, **kwargs):  # noqa: E501
        """Ensure AccessKey  # noqa: E501

        Renew will replace the existing secret access key with a new one.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_renew(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey that should be ensured. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AccessKeyRead
        """
        kwargs['_return_http_data_only'] = True
        return self.accesskeys_renew_with_http_info(accesskey_id, **kwargs)  # noqa: E501

    def accesskeys_renew_with_http_info(self, accesskey_id, **kwargs):  # noqa: E501
        """Ensure AccessKey  # noqa: E501

        Renew will replace the existing secret access key with a new one.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.accesskeys_renew_with_http_info(accesskey_id, async_req=True)
        >>> result = thread.get()

        :param accesskey_id: The ID (UUID) of the AccessKey that should be ensured. (required)
        :type accesskey_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(AccessKeyRead, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'accesskey_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accesskeys_renew" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'accesskey_id' is set
        if self.api_client.client_side_validation and ('accesskey_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['accesskey_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `accesskey_id` when calling `accesskeys_renew`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'accesskey_id' in local_var_params:
            path_params['accesskeyId'] = local_var_params['accesskey_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['tokenAuth']  # noqa: E501

        response_type = 'AccessKeyRead'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/accesskeys/{accesskeyId}/renew', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
