from flask import Flask
import subprocess
import os
import sys

app = Flask(__name__)
bot_process = None  # Global process handle

@app.route('/')
def home():
    return '🤖 Bot Control Server is running!'

@app.route('/start-bot')
def start_bot():
    global bot_process
    if bot_process is None or bot_process.poll() is not None:
        try:
            print("🚀 Starting bot...")
            sys.stdout.flush()
            # Start final-bot.py with unbuffered output (-u)
            bot_process = subprocess.Popen(
                ["python3", "-u", "final-bot.py"],  # -u = unbuffered stdout/stderr
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            return "✅ Bot started"
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            sys.stdout.flush()
            return f"❌ Failed to start bot: {e}", 500
    return "⚠️ Bot is already running"

@app.route('/stop-bot')
def stop_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        print("🛑 Stopping bot...")
        sys.stdout.flush()
        bot_process.terminate()
        return "🛑 Bot stopped"
    return "ℹ️ No bot is running"

if __name__ == '__main__':
    # Set PYTHONUNBUFFERED so Flask's own prints are also unbuffered
    os.environ["PYTHONUNBUFFERED"] = "1"
    port = int(os.environ.get('PORT', 5000))
    print(f"🔧 Starting Flask server on port {port}")
    sys.stdout.flush()
    app.run(debug=True, host='0.0.0.0', port=port)
