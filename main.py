from flask import Flask, jsonify, request
import pandas as pd
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


file_name = 'DataCoSupplyChainDataset.csv'
table_name = 'supply_chain'
db_filename = 'supply_chain_db.db'


@app.route('/')
def get_columns():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}')")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'columns': columns})


@app.route('/fetch_data', methods=['POST'])
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