from urllib.parse import urlparse, parse_qs, unquote
from weakref import WeakValueDictionary
from http import HTTPStatus
from . import cls
from ... import common_utils
import os
__http_request_map = WeakValueDictionary()


def get_http_request_info(data):
    try:
        request = data['instance']
        u = urlparse(request.path)
        request_headers = dict(request.headers)
        query_params = parse_qs(u.query)
        for k, v in query_params.items():
            query_params[k] = v[0]

        po_request_header = 'X-Protectonce-Request-Id'
        if po_request_header in request_headers:
            po_request_header_value = request_headers[po_request_header]
            del request_headers[po_request_header]
            request_headers[po_request_header.lower()
                            ] = po_request_header_value

        request_data = {
            'url': unquote(request.path),
            'queryParams': query_params,
            'requestHeaders': request_headers,
            'method': request.command,
            'host': request_headers['Host'] if request_headers['Host'] else os.uname()[1],
            'requestPath': u.path,
            'sourceIP': request.client_address[0],
            'poSessionId': data['result']
        }
        return request_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.get_http_request_info failed with error {e}')
        return {}


def store_request_object(data):
    try:
        po_session_id = data.get('result', '')
        if not po_session_id:
            return

        request = data.get('instance', None)
        if not request:
            return

        __http_request_map[po_session_id] = request
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.store_request_object failed with error {e}')
        return


def cancel_request(data):
    try:
        if common_utils.is_action_blocked(data) == False:
            return

        po_session_id = cls.get_property(data).get('poSessionId', '')
        request = __http_request_map.get(po_session_id, None)

        if not request:
            return

        action = data['result'].get('action', '')
        redirect_url = data['result'].get('redirectUrl', None)

        if(action == 'redirect' and redirect_url):
            request.send_response(HTTPStatus.FOUND)
            request.send_header('Location', redirect_url)
            request.end_headers()
        if(action in ['block', 'abort']):
            request.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
        del __http_request_map[po_session_id]
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.cancel_request failed with error {e}')
        return


def get_rfile(data):
    try:
        return data['instance'].rfile
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.get_rfile failed with error {e}')
        return


def store_post_data(data):
    try:
        if(data['result']):
            post_data = {
                'requestBody': unquote(data['result'].decode('utf-8')),
                'formData': '',  # TODO handle form data
                'poSessionId': cls.get_property(data).get('poSessionId', '')
            }
            return post_data
        return {}
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.store_post_data failed with error {e}')
        return {}


def update_request_and_return_response_data(data):
    try:
        args = data.get('args', {})
        index = data.get('config', {}).get('argsIndex', len(args))
        requestInfo = data.get('result', {}).get('requestInfo', None)
        if not requestInfo:
            return {}
        protectonce_request_id = requestInfo.get('poRequestId', None)
        poSessionId = requestInfo.get('poSessionId', '')
        if len(args) > index:
            request = args[index]
            if request:
                request.add_header('x-protectonce-request-id',
                                   protectonce_request_id)
                outgoingRequestUrl = request.selector
                # request.selector refers to the URI path of the request
        response_data = {
            'poSessionId': poSessionId,
            'statusCode': 200,
            'outgoingRequestUrl': outgoingRequestUrl
        }
        return response_data
    except Exception as e:
        print(
            f'[PROTECTONCE_ERROR] http_server.update_request_and_return_response_data failed with error {e}')
        return {}
