import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import pymysql.cursors
import bcrypt
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__) 
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')

# إعداد فولدر رفع الصور للبونص
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'registration'),
        cursorclass=pymysql.cursors.DictCursor
    )

def get_library_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database='library',
        cursorclass=pymysql.cursors.DictCursor
    )

# ==========================================
# PROBLEM 1: TODO & AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    filter_type = request.args.get('filter', 'all')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS open_count FROM todos WHERE user_id = %s AND is_done = FALSE", (session['user_id'],))
            open_count_result = cursor.fetchone()
            open_count = open_count_result['open_count'] if open_count_result else 0

            if filter_type == 'active':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = FALSE ORDER BY todo_id DESC"
            elif filter_type == 'completed':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = TRUE ORDER BY todo_id DESC"
            else:
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC"
                
            cursor.execute(sql, (session['user_id'],))
            todos = cursor.fetchall()
            return render_template('index.html', name=session['name'], todos=todos, current_filter=filter_type, open_count=open_count)
    finally:
        conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email or not password or not confirm_password:
            return render_template('register.html', error="All fields are required")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, name, hashed_pw))
                conn.commit()
                
                user_id = cursor.lastrowid
                session['user_id'] = user_id
                session['name'] = name
                return redirect(url_for('index'))
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                return render_template('register.html', error="Email Already Exists")
            return render_template('register.html', error="Database error occurred")
        finally:
            conn.close()

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error="Email and password are required")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT user_id, name, password_hash FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error="Invalid email or password")
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    if not title:
        flash("Title is required")
        return redirect(url_for('index'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO todos (user_id, title) VALUES (%s, %s)"
            cursor.execute(sql, (session['user_id'], title))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE todos SET is_done = NOT is_done WHERE todo_id = %s AND user_id = %s"
            cursor.execute(sql, (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM todos WHERE todo_id = %s AND user_id = %s"
            cursor.execute(sql, (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_title = request.form.get('title', '').strip()
    
    if not new_title:
        flash('Title is required')
        return redirect(url_for('index'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
                (new_title, todo_id, session['user_id'])
            )
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))


# ==========================================
# PROBLEM 2: LIBRARY SYSTEM (With Image Bonus)
# ==========================================

@app.route('/books')
def list_books():
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM BOOK")
            books = cursor.fetchall()
            
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
            
            return render_template('books.html', books=books, authors=authors)
    finally:
        conn.close()
@app.route('/books/add', methods=['POST'])
def add_book():
    book_id = request.form.get('book_id')
    title = request.form.get('title', '').strip()
    price = request.form.get('price')
    author_id = request.form.get('author_id')
    
    file = request.files.get('cover_image')
    filename = ''
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if not book_id or not title or not price or not author_id:
        flash('All fields are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO BOOK (book_id, title, price, author_id, cover_image) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (book_id, title, price, author_id, filename))
            conn.commit()
            flash('Book added successfully!')
    except pymysql.MySQLError as e:
        flash('Error adding book.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))
@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
            conn.commit()
            flash('Deleted book successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/books/edit/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    title = request.form.get('title', '').strip()
    price = request.form.get('price')
    author_id = request.form.get('author_id')

    if not title or not price or not author_id:
        flash('All fields are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                (title, price, author_id, book_id)
            )
            conn.commit()
            flash('Book updated successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))
# ==========================================
# AUTHORS CRUD ROUTES
# ==========================================

@app.route('/authors/add', methods=['POST'])
def add_author():
    author_id = request.form.get('author_id')
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()
    
    file = request.files.get('photo')
    filename = ''
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if not author_id or not name or not country:
        flash('All author fields are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO AUTHOR (author_id, name, country, photo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (author_id, name, country, filename))
            conn.commit()
            flash('Author added successfully!')
    except pymysql.MySQLError as e:
        flash('Error adding author. Make sure Author ID is unique.')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/authors/edit/<int:author_id>', methods=['POST'])
def edit_author(author_id):
    name = request.form.get('name', '').strip()
    country = request.form.get('country', '').strip()

    if not name or not country:
        flash('All fields are required.')
        return redirect(url_for('list_books'))

    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s",
                (name, country, author_id)
            )
            conn.commit()
            flash('Author updated successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))

@app.route('/authors/delete/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    conn = get_library_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
            conn.commit()
            flash('Author and associated books deleted successfully!')
    finally:
        conn.close()
    return redirect(url_for('list_books'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
