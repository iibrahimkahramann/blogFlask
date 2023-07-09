from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)

@app.route('/')
def blog():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    rows = cursor.fetchall()

    blog_data = []
    for row in rows:
        blog_data.append({
            'id': row[0],
            'title': row[1],
            'summary': row[2],
            'contents': row[3],
            'release_date': row[4]
        })

    conn.close()
    
    return jsonify(blog_data)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    summary = request.form['summary']
    contents = request.form['contents']
    release_date = request.form['release_date']

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (title, summary, contents, release_date) VALUES (?,?,?,?)', (title, summary, contents, release_date))
    id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': id})



app.run()


