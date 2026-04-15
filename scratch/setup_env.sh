#!/bash/bin

# This script installs the necessary system dependencies and browser binaries 
# for browser-use (Playwright) to run on an AWS EC2 instance.

echo "--- Installing browser dependencies (may require sudo password) ---"
sudo ./venv/bin/python -m playwright install-deps

echo "--- Installing Chromium browser ---"
./venv/bin/python -m playwright install chromium

echo "--- Done! You can now run the agent. ---"
