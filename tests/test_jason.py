# coding=utf-8
from django.conf import settings
settings.configure()

import json
from django.http import HttpRequest
import jason


def test_json_response_defaults():
    response = jason.response()
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8")) == {
        "status": 200, "message": "OK", "data": {}
    }
    assert response['Content-Type'] == 'application/json'

def test_json_response():
    response = jason.response({u'ØÆÅ': u'ø'}, 401, 'NO')
    assert response.status_code == 401
    assert json.loads(response.content.decode("utf-8"), encoding='utf-8') == {
        "status": 401, "message": "NO", "data": {u"ØÆÅ": u"ø"}
    }
    assert response['Content-Type'] == 'application/json'

@jason.view(allowed_methods=['GET'])
def view1(request):
    return {'cool': 42},

def test_view_method_not_allowed():
    request = HttpRequest()
    request.method = 'POST'
    assert json.loads(view1(request).content.decode("utf-8")) == {
        "status": 405, "message": "Method Not Allowed", "data": {},
    }

@jason.view(allowed_methods=['GET'])
def view2(request):
    return {'cool': 42},

def test_view_ok():
    request = HttpRequest()
    request.method = 'GET'
    assert json.loads(view2(request).content.decode("utf-8")) == {
        "status": 200, "message": "OK", "data": {'cool': 42},
    }

@jason.view(allowed_methods=['GET'])
def view3(request):
    raise jason.Bail({}, 402, "Nooooo")

def test_view_bail():
    request = HttpRequest()
    request.method = 'GET'
    assert json.loads(view3(request).content.decode("utf-8")) == {
        "status": 402, "message": "Nooooo", "data": {},
    }

class CustomException(Exception):
    pass

@jason.view(allowed_methods=['GET'])
def view4(request):
    raise CustomException()

def test_view_other_exception():
    request = HttpRequest()
    request.method = 'GET'
    assert json.loads(view4(request).content.decode("utf-8")) == {
        "status": 500, "message": "Internal Server Error", "data": {},
    }

@jason.view(allowed_methods=['GET'], exceptions={
    CustomException: lambda e: (19, 278, 'Custom'),
})
def view5(request):
    raise CustomException()

def test_view_custom_exception():
    request = HttpRequest()
    request.method = 'GET'
    assert json.loads(view5(request).content.decode("utf-8")) == {
        "status": 278, "message": "Custom", "data": 19,
    }

@jason.view(allowed_methods=['GET'], exceptions={
    CustomException: lambda e: (19, 278, 'Custom'),
})
def view6(request):
    raise Exception()

def test_view_base_exception():
    request = HttpRequest()
    request.method = 'GET'
    assert json.loads(view6(request).content.decode("utf-8")) == {
        "status": 500, "message": "Internal Server Error", "data": {},
    }

class UserHasPerm():
    def has_perm(self, perm):
        return perm == 'myapp.perm_ok'

@jason.permission_required('myapp.perm_ok')
@jason.view(allowed_methods=['GET'])
def view7(request):
    return {'cool': 42},

def test_permission_required_has_perm():
    request = HttpRequest()
    request.method = 'GET'
    request.user = UserHasPerm()
    assert json.loads(view7(request).content.decode("utf-8")) == {
        "status": 200, "message": "OK", "data": {'cool': 42},
    }

@jason.permission_required('myapp.perm_not_ok')
@jason.view(allowed_methods=['GET'])
def view8(request):
    return {'cool': 42},

def test_permission_required_hasnt_perm():
    request = HttpRequest()
    request.method = 'GET'
    request.user = UserHasPerm()
    assert json.loads(view8(request).content.decode("utf-8")) == {
        "status": 401, "message": "Unauthorized", "data": {},
    }