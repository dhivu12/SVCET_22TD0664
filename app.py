from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    conn.commit()
    conn.close()

# Route to display all tasks
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route to add multiple tasks
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Get the tasks from the textarea, split by newlines
        tasks_input = request.form['tasks']
        tasks_list = [task.strip() for task in tasks_input.split('\n') if task.strip()]

        # Insert each task into the database
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        for task in tasks_list:
            c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('add_task.html')

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)