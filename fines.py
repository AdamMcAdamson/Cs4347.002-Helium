import sqlite3 as sql
from flask_restful import Resource

from consts import DB_FILE#, SEARCH_PAGE_SIZE

class FinesAll(Resource):

    # @TODO: Pagination or no?
    def get(self):

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''SELECT * FROM FINES;'''

            return [dict(x) for x in c.execute(sql_query).fetchall()]