from  flask import Flask, jsonify, request
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
    conn.commit()
    conn.close()
    return jsonify({'msg' : 'Başarıyla eklendi.'})



#blog güncellemek için bunu kullan
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

#Blog silmek için bunu kullan
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
            'comment_id': row[0],
            'name': row[1],
            'comment': row[2],
            'release_date': row[3],
        })

    conn.close()
    
    return jsonify(comments_data)



#Yorum eklemek için bunu kullan
@app.route('/comments-add', methods=['POST'])
def comments_add():
    name = request.form['name']
    comment = request.form['comment']
    release_date = request.form['release_date']
    post_id = request.form['id']



    release_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comments (name ,comment, release_date,id) VALUES (?,?,?,?)', (name, comment, release_date,post_id))
    conn.commit()
    conn.close()
    return jsonify({'msg' : 'Başarıyla eklendi.'})

#yorum sorgulama
@app.route('/comments/<int:id>')
def comments(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT comments.comment_id comments.name, comments.comment, comments.release_date FROM comments LEFT JOIN posts ON posts.id = comments.id WHERE posts.id = ?', (post_id,))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)


#yorum silmek için bunu kullan
@app.route('/comments-del/<int:id>/<int:comment_id>', methods=['DELETE'])
def comments_delete(id, comment_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comments WHERE id = ? AND comment_id = ?', (id, comment_id))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({'msg': 'Yorum başarıyla silindi.'})
    else:
        return 'Yorum bulunamadı veya silinemedi.'



#Yorum güncellemek için bunu kullan
@app.route('/comments-update/<int:comment_id>', methods=['POST'])
def comment_update(comment_id):
    name = request.form['name']
    comment = request.form['comment']
    
    update_time = datetime.now().strftime(" %d-%m-%Y %H:%M:%S")

    if name and comment:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE comments SET name = ?, comment = ?,  update_time = ? WHERE comment_id = ?', (name, comment, update_time,comment_id))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({'msg': 'Başarıyla güncellendi'})
        else:
            return 'Kayıt bulunamadı.'
    cursor.close()
    conn.close()





#USERNAME



@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        cursor.execute("INSERT INTO users(user_name, password) VALUES (?, ?)", (user_name,password))
        conn.commit()
        return 'Kayıt başarılı!'
    

app.run()


