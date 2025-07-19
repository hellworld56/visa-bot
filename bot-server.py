from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import os
import threading

app = Flask(__name__)
bot_process = None
bot_status = {
    "running": False,
    "message": "Bot not started",
    "logs": []
}


def monitor_bot():
    global bot_process, bot_status
    if not bot_process:
        return

    # Read live output
    for line in iter(bot_process.stdout.readline, b''):
        decoded = line.decode().strip()
        print(decoded)
        bot_status["logs"].append(decoded)

    bot_process.wait()
    exit_code = bot_process.returncode

    if exit_code == 0:
        bot_status["message"] = "Bot completed successfully"
    else:
        bot_status["message"] = f"Bot failed with exit code {exit_code}"
    bot_status["running"] = False
    bot_process = None


@app.route('/')
def index():
    return render_template("index.html", bot_status=bot_status)


@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_process, bot_status

    if bot_process and bot_process.poll() is None:
        bot_status["message"] = "Bot is already running"
        return redirect(url_for("index"))

    email = request.form.get("email")
    password = request.form.get("password")
    country = request.form.get("country")

    if not email or not password or not country:
        bot_status["message"] = "Missing credentials"
        return redirect(url_for("index"))

    env = os.environ.copy()
    env["BOT_EMAIL"] = email
    env["BOT_PASSWORD"] = password
    env["BOT_COUNTRY"] = country

    try:
        print("Starting bot...")
        bot_status["running"] = True
        bot_status["message"] = "Bot is running..."
        bot_status["logs"] = []

        bot_process = subprocess.Popen(
            ["python3", "-u", "final-bot.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        threading.Thread(target=monitor_bot, daemon=True).start()
        return redirect(url_for("index"))

    except Exception as e:
        print(f"Failed to start bot: {e}")
        bot_status["running"] = False
        bot_status["message"] = f"Failed to start bot: {e}"
        return redirect(url_for("index"))


@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_process, bot_status
    if bot_process and bot_process.poll() is None:
        print("Stopping bot...")
        bot_process.terminate()
        bot_process.wait()
        bot_process = None
        bot_status["message"] = "Bot was manually stopped"
    else:
        bot_status["message"] = "⚠️ No bot process to stop"
    bot_status["running"] = False
    return redirect(url_for("index"))


@app.route('/status')
def status():
    return jsonify({
        "running": bot_status["running"],
        "message": bot_status["message"]
    })


@app.route('/logs')
def logs():
    return jsonify({
        "logs": bot_status["logs"][-100:]  # last 100 lines
    })


if __name__ == '__main__':
    os.environ["PYTHONUNBUFFERED"] = "1"
    app.run(debug=True, host='0.0.0.0', port=5000)
