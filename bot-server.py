from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import sys

app = Flask(__name__)
bot_process = None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return "⚠️ Bot is already running"

    email = request.form.get("email")
    password = request.form.get("password")
    country = request.form.get("country")

    if not email or not password or not country:
        return "❌ Missing credentials", 400

    env = os.environ.copy()
    env["BOT_EMAIL"] = email
    env["BOT_PASSWORD"] = password
    env["BOT_COUNTRY"] = country

    try:
        print("🚀 Starting bot...")
        bot_process = subprocess.Popen(
            ["python3", "-u", "final-bot.py"],
            env=env,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        return redirect(url_for("index"))
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        return f"❌ Failed to start bot: {e}", 500

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        print("🛑 Stopping bot...")
        bot_process.terminate()
        bot_process.wait()
        bot_process = None
    return redirect(url_for("index"))

if __name__ == '__main__':
    os.environ["PYTHONUNBUFFERED"] = "1"
    app.run(debug=True, host='0.0.0.0', port=5000)
