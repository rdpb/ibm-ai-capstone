from flask import Flask, jsonify, request

from dashboards import create_dash_app

from application.model import model_train, model_load, model_predict
from application.model import MODEL_VERSION, MODEL_VERSION_NOTE

server = Flask(__name__)

@server.route('/check')
def index():
    return 'Flask app is running'

app = create_dash_app(server)

if __name__ == '__main__':
    app.run_server(debug=True)