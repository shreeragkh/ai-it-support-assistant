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
    return render_template('dashboard.html', users=users)

@app.route('/agent/run', methods=['POST'])
@login_required
def run_ai_agent():
    query = request.form.get('query')
    if not query:
        flash("Please enter a query for the agent.", "error")
        return redirect(url_for('dashboard'))
    
    # Start the agent in a background thread
    thread = threading.Thread(target=start_agent_thread, args=(query,))
    thread.daemon = True
    thread.start()
    
    flash(f"AI Agent dispatched: '{query}'. It will perform the task in the background.", "info")
    return redirect(url_for('dashboard'))

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        new_user = {
            "id": str(uuid.uuid4()),
            "name": request.form['name'],
            "email": request.form['email'],
            "role": request.form['role'],
            "status": "Active"
        }
        users.append(new_user)
        flash(f"User {new_user['name']} created successfully!", "success")
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

if __name__ == '__main__':
    app.run(debug=False, port=5051)
