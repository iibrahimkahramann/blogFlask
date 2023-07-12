import sqlite3
from flask import Flask, jsonify

def check_user(username, password):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?", (username,password))
    results = cursor.fetchall()
    conn.close()
    if results is not None:
        return True
    else:
        return False
