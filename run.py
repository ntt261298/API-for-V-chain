from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

BASE_URL = 'http://178.128.217.110:8302/quanLyXuatNhapHang'

def get_request(url, params=None, headers=None):
    res = requests.get(BASE_URL + url, params=params, headers=headers)
    # return if status code is not 200 OK
    if res.status_code != 200:
        res.raise_for_status()
        return

    # status == 200
    return res.json()

def post_request(url, data=None, headers=None):
    headers = dict(headers) if headers else {}
    headers["Content-Type"] = "application/json"

    res = requests.post(
        BASE_URL + url, data=json.dumps(data) if data else json.dumps({}), headers=headers
    )
    # return if status code is not 200 OK
    if res.status_code != 200:
        res.raise_for_status()
        return

    # status == 200
    return res.json()


@app.route('/getProducts/<product_type>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getProduct(product_type):
    params = {'type': product_type}
    headers = {'authorization': request.headers['authorization']}

    res = get_request('/get', params=params, headers=headers)
    return jsonify(res)

@app.route('/createProduct', methods=['POST'])
@cross_origin(supports_credentials=True)
def createProduct():
    headers = {'authorization': request.headers['authorization']}
    data = request.get_json()
    
    res = post_request('/create', data, headers)
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 