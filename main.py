from flask import Flask, request, current_app
from flask_restful import Resource, Api
import sqlite3 as sql

app = Flask(__name__, static_url_path='/')
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'Hello': "World"}

class Quote(Resource):
    def get(self):
        args = request.args
        with sql.connect('HeliumDB.db') as conn:
            return conn.execute('SELECT * FROM quote WHERE id = ?', args['id']).fetchall()


api.add_resource(HelloWorld, '/')
api.add_resource(Quote, '/quote', endpoint='quote')

if __name__ == '__main__':
    app.run(debug=True)
