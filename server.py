from flask import Flask, request, send_from_directory
from detect import process
import base64

app = Flask(__name__, static_url_path='')

@app.route("/ui/<path:path>")
def static_route(path):
    return send_from_directory('ui', path)

@app.route("/detect", methods=['POST'])
def detect():
    if request.headers["Content-Type"] == "text/base64":
        data = request.data.decode('utf-8')
        data = data.split(",", maxsplit=2)
        header, data = data
        result = process(base64.b64decode(data))
        result = base64.b64encode(result).decode('utf-8')
        return '%s,%s' % (header, result) 
    return app.make_response(('unknown mime-type %s' % (request.headers["Content-Type"]), 400))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8999, debug=True)
