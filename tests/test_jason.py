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
def x(request):
    return {'cool': 42},

def test_view():
    assert json.loads(x(HttpRequest()).content.decode("utf-8")) == {
        "status": 405, "message": "Method Not Allowed", "data": {}
    }