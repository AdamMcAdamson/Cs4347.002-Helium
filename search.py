import sqlite3 as sql
from flask import request
from flask_restful import Resource

from consts import DB_FILE, SEARCH_PAGE_SIZE

#TODO: Book availability
class Search(Resource):

    def get(self):
        args = {'q':request.args.get('q', '').lower(), 'p':request.args.get('p', ''), 's':SEARCH_PAGE_SIZE}

        with sql.connect(DB_FILE) as conn:
            conn.row_factory = sql.Row
            c = conn.cursor()

            sql_query = '''
            WITH q_authors AS (
                SELECT GROUP_CONCAT(Name,', ') AS Author_names, Isbn
                FROM AUTHORS NATURAL JOIN BOOK_AUTHORS
                GROUP BY Isbn
            )
            SELECT Isbn, Title, Author_names, Cover_url
            FROM BOOK NATURAL JOIN q_authors
            WHERE INSTR(LOWER(Title), :q) > 0
            OR INSTR(LOWER(Author_names), :q) > 0
            OR INSTR(LOWER(Isbn), :q) > 0
            ORDER BY INSTR(LOWER(Isbn), :q), INSTR(LOWER(Author_names), :q), INSTR(LOWER(Title), :q)
            LIMIT :s OFFSET (:p-1)*:s
            ;
            '''

            return [dict(x) for x in c.execute(sql_query, args).fetchmany(size=SEARCH_PAGE_SIZE)]