from flask import Flask, jsonify, request
from mini_scraper import get_leaderboard_data
import json

app = Flask(__name__)

@app.route('/mini-data/')
def get_mini_data():
    email = request.args.get('user')
    pass_ = request.args.get('pass')
    cookie = request.args.get('cookie')
    return json.dumps(get_leaderboard_data(x=30, cookie=cookie))
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)