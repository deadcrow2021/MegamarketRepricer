from flask import Flask, render_template, request
from waitress import serve

from src.services import get_similar_data

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')


@app.route('/get_data/', methods=['POST'])
def get_data():
    data = request.get_json()
    print(data, type(data))
    return {'status': 'ok'}
    # return get_similar_data()


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
