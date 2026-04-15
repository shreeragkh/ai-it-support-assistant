# AI-Powered IT Support Agent

An autonomous AI agent designed to automate IT administrative tasks on a mock admin panel using LLM-driven browser navigation.

## 🚀 Features

- **Autonomous Navigation**: Uses the `browser-use` library to interact with the web interface like a human.
- **Natural Language Commands**: Carry out complex tasks like "Create user Alice" or "Reset password for Jane" using plain English.
- **Integrated Command Center**: An AI console built directly into the Admin Dashboard for parallel task execution.
- **Optimized for Efficiency**: Tuned vision settings and DOM attribute filtering to minimize API costs and improve response times.
- **Mock IT Admin Panel**: A functional Flask-based dashboard with user directory and administrative actions.

## 🛠️ Tech Stack

- **Framework**: Flask (Mock Admin Panel)
- **AI Agent**: [browser-use](https://docs.browser-use.com/)
- **LLM**: Google Gemini 2.x (via `langchain-google-genai`)
- **Automation**: Playwright (Browser steering)

## 📋 Prerequisites

- Python 3.9+
- [Gemini API Key](https://aistudio.google.com/app/apikey)

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd ai-it-support-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_key_here
   ```

## 🖥️ Usage

### 1. Start the Admin Panel
```bash
python app.py
```
Wait for the server to start at `http://127.0.0.1:5051`.

### 2. Access the Dashboard
Log in at `http://127.0.0.1:5051/login` with:
- **Username**: `admin`
- **Password**: `admin`

### 3. Run AI Tasks
- **Via the Dashboard**: Use the **AI Command Center** box at the top of the directory to type and run commands.
- **Via CLI**: In a separate terminal, run:
  ```bash
  source venv/bin/activate
  python agent.py "Reset password for John Doe"
  ```

## 📁 Project Structure

- `app.py`: Flask application server and background task runner.
- `agent.py`: AI Agent logic and configuration.
- `templates/`: HTML templates for the dashboard and login.
- `.env`: (Ignored) Your API credentials.
- `.gitignore`: Standard exclusions for Python and local data.

## 🛡️ License

MIT License
