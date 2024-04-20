from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
from flask_caching import Cache


app = Flask(__name__)
CORS(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


file_name = 'DataCoSupplyChainDataset.csv'
table_name = 'supply_chain'
db_filename = 'supply_chain_db.db'


@app.route('/')
@cache.cached(timeout=60)
def get_columns():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}')")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'columns': columns})


@app.route('/fetch_data', methods=['POST'])
# @cache.cached(timeout=60, key=lambda c: (c.column, c.json.get('page', 1), c.json.get('limit', 10)))
def fetch_data():
    selected_column = request.json['column']
    page = request.json.get('page', 1)
    limit = request.json.get('limit', 10)
    offset = (page-1) * limit
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    query = f"select distinct [{selected_column}] from {table_name} limit {limit} offset {offset}"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return jsonify({'rows': data})


@app.route('/fetch_rows', methods=['POST'])
# @cache.cached(timeout=60)
def fetch_rows():
    selected_column = request.json['column']
    selected_data = request.json['data']
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    query = f"select distinct * from {table_name} where [{selected_column}] = '{selected_data}'"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return jsonify({'rows': data})


if __name__ == '__main__':
    app.run()