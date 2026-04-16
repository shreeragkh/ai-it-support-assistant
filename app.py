from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import uuid

import threading
import asyncio
from agent import run_agent

app = Flask(__name__)
app.secret_key = "super-secret-key"

# Helper to run the async agent in a background thread
def start_agent_thread(query):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_agent(query))
    loop.close()

# Mock Database
users = [
    {"id": "1", "name": "John Doe", "email": "john@company.com", "role": "Employee", "status": "Active"},
    {"id": "2", "name": "Jane Smith", "email": "jane@company.com", "role": "Manager", "status": "Active"},
]

agent_reports = [] # Stores last 5 agent tasks
active_task_logs = [] # Stores live steps of the CURRENT running task

@app.route('/agent/report', methods=['POST'])
def agent_report():
    report = request.json
    if report:
        agent_reports.insert(0, report)
        if len(agent_reports) > 5:
            agent_reports.pop()
    return {"status": "ok"}

@app.route('/agent/log_step', methods=['POST'])
def log_step():
    data = request.json
    if data and 'message' in data:
        active_task_logs.append(data['message'])
    return {"status": "ok"}

@app.route('/agent/get_logs', methods=['GET'])
def get_logs():
    return {"logs": active_task_logs}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', users=users, reports=agent_reports)

@app.route('/agent/run', methods=['POST'])
@login_required
def run_ai_agent():
    query = request.form.get('query')
    if not query:
        flash("Please enter a query for the agent.", "error")
        return redirect(url_for('dashboard'))
    
    active_task_logs.clear()
    active_task_logs.append(f"Starting process: {query}")

    thread = threading.Thread(target=start_agent_thread, args=(query,))
    thread.daemon = True
    thread.start()
    
    flash(f"AI Agent dispatched: '{query}'. It will perform the task in the background.", "info")
    return redirect(url_for('dashboard'))

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'Employee')

        if not name or not email or not password:
            flash("All fields (Name, Email, Password) are required.", "error")
            return render_template('user_form.html')

        if any(u['email'].lower() == email.lower() for u in users):
            flash(f"Error: A user with email '{email}' already exists.", "error")
            return render_template('user_form.html')

        new_user = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "role": role,
            "status": "Active"
        }
        users.append(new_user)
        flash(f"User {name} created successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('user_form.html')

@app.route('/users/<user_id>/reset', methods=['POST'])
@login_required
def reset_password(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        flash(f"Password reset link sent to {user['email']}", "success")
    else:
        flash("User not found", "error")
    return redirect(url_for('dashboard'))

@app.route('/users/<user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        users = [u for u in users if u['id'] != user_id]
        flash(f"User {user['name']} has been deleted.", "success")
    else:
        flash("User not found", "error")
    return redirect(url_for('dashboard'))

@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        flash("User not found", "error")
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user['name'] = request.form.get('name')
        user['email'] = request.form.get('email')
        user['role'] = request.form.get('role', user['role'])
        flash(f"User {user['name']} updated successfully!", "success")
        return redirect(url_for('dashboard'))
        
    return render_template('user_edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=False, port=5050)
