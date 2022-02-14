import json

import requests
from django.http import HttpResponse
from mykoodous import settings

from django.views.decorators.csrf import csrf_exempt


def make_api_response(data, status=200):
    api_resp = HttpResponse(json.dumps(
        data, sort_keys=True,
        indent=4, separators=(',', ': ')), content_type="application/json; charset=utf-8", status=status)
    api_resp['Access-Control-Allow-Origin'] = '*'
    return api_resp


def api_key():
    return settings.API_TOKEN


def api_auth(request):
    return bool(api_key() == request.POST.get('key'))


def get_checkbox(param):
    if param == "on":
        return True
    else:
        return False


@csrf_exempt
def api_scan(request):
    if api_auth(request):
        if request.method == 'POST':
            api_key = request.POST['api_key']
            resp = scan(request, api_key)
            if resp is not None and "error" in resp:
                response = make_api_response(resp, 500)
            else:
                response = make_api_response(resp)
        else:
            response = make_api_response({"error": "Method Not Allowed"}, 405)
    else:
        response = make_api_response({"error": "You are Unauthorized."}, 401)
    return response


def get_result(final_resp, base_url, headers=None, params=None):
    result = requests.get(url=base_url, headers=headers, params=params)
    res_json = result.json()

    if res_json['previous'] is None:
        final_resp = res_json
    elif 'results' in res_json:
        final_resp['results'].extend(res_json['results'])
    if res_json['next'] is not None:
        get_result(final_resp, base_url=res_json['next'], headers=headers)

    return final_resp


def scan(request, apikey):
    try:
        resp = {}
        base_url = "https://api.koodous.com/apks"
        headers = {"Authorization": "Token " + apikey}

        # Lookup
        if 'search' in request.POST:
            search = request.POST.get('search')
            if search is not None:
                params = {'search': search}
                resp.update(get_result(resp, base_url, headers, params))

        if 'hash' in request.POST:
            file_hash = request.POST.get('hash')
            if file_hash is not None:
                url = '%s/%s/analysis' % (base_url, file_hash)
                result = requests.get(url=url, headers=headers)
                resp = result.json()

        return resp
    except Exception as ex:
        return {"Error": str(ex)}
