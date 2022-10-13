from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3 as sql

app = Flask(__name__, static_url_path='/')
api = Api(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')

class Quote(Resource):
    def get(self):
        args = request.args
        with sql.connect('HeliumDB.db') as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()
            return [dict(x) for x in (c.execute('SELECT * FROM quote').fetchall())]


api.add_resource(Quote, '/quote', endpoint='quote')

if __name__ == '__main__':
    app.run(debug=True)
