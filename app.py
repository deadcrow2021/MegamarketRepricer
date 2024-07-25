from flask import Flask, render_template, request
from waitress import serve

from src.constants import WORK_DIR
from src.services import (
    get_similar_data,
    find_cards_by_title,
    change_remote_price
)

app = Flask(
    __name__,
    static_folder=WORK_DIR / 'static',
    template_folder=WORK_DIR / 'templates'
)


@app.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')


@app.route('/get_data/', methods=['POST'])
def get_data():
    data = request.get_json()
    result = get_similar_data(data['title'])
    return result


@app.route('/find_cards/', methods=['POST'])
def find_cards():
    data = request.get_json()
    result = find_cards_by_title(data['title'])
    return result


@app.route('/send_prices/', methods=['POST'])
def send_prices():
    data = request.get_json()
    result = change_remote_price(data['data'])
    return result



if __name__ == '__main__':
    port = input('Input port (default 8080):  ')
    if not port:
        port = 8080

    serve(app, host='0.0.0.0', port=int(port))
