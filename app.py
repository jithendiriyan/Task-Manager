from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="taskmanager"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    cursor.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)", 
                   (title, description, due_date, priority))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    status = request.form['status']
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, id))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
