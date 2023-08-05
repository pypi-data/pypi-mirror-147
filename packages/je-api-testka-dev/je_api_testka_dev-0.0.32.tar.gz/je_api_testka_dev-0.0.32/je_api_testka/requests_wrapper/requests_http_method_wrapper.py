import sys

import requests
from requests import Session
from requests import delete
from requests import get
from requests import head
from requests import options
from requests import patch
from requests import post
from requests import put

from je_api_testka.utils.exception.api_test_eceptions_tag import http_method_have_wrong_type
from je_api_testka.utils.exception.api_test_exceptions import APITesterException
from je_api_testka.utils.exception.api_test_eceptions_tag import wrong_http_method_error_message

from je_api_testka.utils.test_record.record_test_result_class import test_record


session = Session()

http_method_dict = {
    "get": get,
    "put": put,
    "patch": patch,
    "post": post,
    "head": head,
    "delete": delete,
    "options": options,
    "session_get": session.get,
    "session_put": session.put,
    "session_patch": session.patch,
    "session_post": session.post,
    "session_head": session.head,
    "session_delete": session.delete,
    "session_options": session.options,
}


def get_http_method(http_method: str) -> [
            requests.get, requests.put, requests.patch, requests.post, requests.head, requests.delete,
            Session.get, Session.put, Session.patch, Session.post, Session.head, Session.head, Session.options
        ]:
    try:
        if http_method is not str or http_method not in http_method_dict.keys:
            if http_method is not str:
                raise APITesterException(wrong_http_method_error_message)
            else:
                raise APITesterException(http_method_have_wrong_type)
        http_method = str(http_method).lower()
        return http_method_dict.get(http_method)
    except APITesterException as error:
        print(repr(error), file=sys.stderr)
        test_record.error_record_list.append(repr(error))


def api_tester_method(http_method: str, test_url: str, **kwargs) -> requests.Response:
    response = get_http_method(http_method)
    if response is None:
        raise APITesterException(wrong_http_method_error_message)
    else:
        response = response(test_url, **kwargs)
    return response
