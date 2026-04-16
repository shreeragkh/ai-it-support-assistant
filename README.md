# AI-Powered IT Support Agent (Ultra-Turbo)

An autonomous, high-performance IT support agent designed for rapid administrative task automation. Built with **browser-use** and **claude-haiku-4-5-20251001**, this agent can navigate complex dashboards, manage users, and handle security tasks with human-like precision but machine-like speed.

## 🚀 "Ultra-Turbo" Features

- **Flash Mode (Zero Latency)**: Reasoning delays have been disabled (`use_thinking=False`) to allow the agent to react to screen states instantly.
- **Smart Pre-Flight Validation**: Automatically validates Name, Email, and Password **before** launching the browser. Aborts and reports errors instantly if data is missing, saving API costs and time.
- **Duplicate Detection**: Intelligently scans the User Directory before creation to prevent redundant accounts.
- **Security-First Logic**:
    - **Modify Password**: Intelligently enters new data into the "Edit" form when asked to reset or change a password.
    - **Send Link**: Explicitly clicks the table-based "Reset Password" button only when a "link" is specifically requested.
- **Zero-Wait Execution**: All artificial browser delays have been removed for maximum efficiency.

## 🛠️ Tech Stack

- **Framework**: Flask (Mock Admin Panel)
- **AI Agent**: [browser-use](https://docs.browser-use.com/) (v0.12.6)
- **LLM**: Anthropic claude-haiku-4-5-20251001 (Optimized for speed)
- **Automation**: Playwright (Persistent Browser Context)

## 📋 Prerequisites

- Python 3.13 (or 3.9+)
- [Anthropic API Key](https://console.anthropic.com/)

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd ai-it-support-agent
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Install Dependencies (Version Locked)**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

## 🖥️ Usage

### 1. Start the Admin Dashboard
```bash
python app.py
```
Access the panel at `http://127.0.0.1:5050`.

### 2. Admin Credentials (Hint)
- **Username**: `admin`
- **Password**: `admin`

### 3. Running AI Commands
- **Via Dashboard**: Use the **AI Command Center** console at the top of the directory.
- **Via CLI**: In a separate terminal run:
  ```bash
  python agent.py "reset password for Jane Smith to SecretPass123"
  ```

## 📁 Project Structure

- `agent.py`: Optimized AI Agent logic with Flash Mode and Pre-Flight Validation.
- `app.py`: Flask dashboard with real-time log polling and report history.
- `browser_session/`: (Ignored) Local persistent browser data/history.
- `templates/`: Professional, modern UI layout and dashboard styles.

## 🛡️ Security / .gitignore Tips
- **Keep `.env` private**: It contains your API credentials.
- **Ignore `browser_session/`**: This folder contains your active login cookies. **NEVER** push this to GitHub.

## 🛡️ License

MIT License
