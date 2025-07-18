from flask import Flask, jsonify
import pymysql
import os
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "App is running!", 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/data')
def get_data():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 database=DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT message FROM messages ;")
    result = cursor.fetchall()
    connection.close()
    messages = [row[0] for row in result]
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
