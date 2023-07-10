from flask import Flask, jsonify, request
from datetime import datetime
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
            'release_date': row[4],
            'update_time' : row[5]
        })

    conn.close()
    
    return jsonify(blog_data)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    summary = request.form['summary']
    contents = request.form['contents']
    release_date = request.form['release_date']


    release_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (title, summary, contents, release_date) VALUES (?,?,?,?)', (title, summary, contents, release_date))
    id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'msg' : 'Başarıyla eklendi.'})



@app.route('/update/<int:id>', methods=['POST'])
def update_record(id):
    new_title = request.form['title']
    new_summary = request.form['summary']
    new_contents = request.form['contents']
    release_date = request.form['release_date']
    update_time = request.form['update_time']
    


    update_time = datetime.now().strftime(" %d-%m-%Y %H:%M:%S")

    if new_title and new_summary:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE posts SET title = ?, summary = ?, contents = ?, update_time = ? WHERE id = ?', (new_title, new_summary, new_contents, update_time,id))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({'msg': 'Başarıyla güncellendi'})
        else:
            return 'Kayıt bulunamadı.'
    cursor.close()
    conn.close()

@app.route('/delete/<int:id>' , methods=['DELETE'])
def delete(id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
            return jsonify({'msg': 'Başarıyla silindi'})
    else:
        return 'Kayıt bulunamadı.'



#comments


def blog():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    rows = cursor.fetchall()

    comments_data = []
    for row in rows:
        comments_data.append({
            'comments_id': row[0],
            'name': row[1],
            'comment': row[2],
            'release_date': row[3],
        })

    conn.close()
    
    return jsonify(comments_data)




@app.route('/comments-add', methods=['POST'])
def comments_add():
    name = request.form['name']
    comment = request.form['comment']
    release_date = request.form['release_date']
    


    release_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comments (name ,comment, release_date) VALUES (?,?,?)', (name, comment, release_date))
    conn.commit()
    conn.close()
    return jsonify({'msg' : 'Başarıyla eklendi.'})



@app.route('/comments/<int:post_id>')
def comments(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT comments.name, comments.comment, comments.release_date FROM comments LEFT JOIN posts ON posts.id = comments.blog_id WHERE posts.id = ?', (post_id,))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)





app.run()


