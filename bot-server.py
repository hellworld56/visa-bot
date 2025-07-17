from flask import Flask
import subprocess
import os

app = Flask(__name__)
bot_process = None  # Global process handle

@app.route('/')
def home():
    return '🤖 Bot Control Server is running!'

@app.route('/start-bot')
def start_bot():
    global bot_process
    if bot_process is None or bot_process.poll() is not None:
        bot_process = subprocess.Popen(["python3", "final-bot.py"])
        return "✅ Bot started"
    return "⚠️ Bot is already running"

@app.route('/stop-bot')
def stop_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        bot_process.terminate()
        return "🛑 Bot stopped"
    return "ℹ️ No bot is running"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render provides this PORT variable
    app.run(debug=True, host='0.0.0.0', port=port)
