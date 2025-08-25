from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    lang = request.headers.get('Accept-Language')

    data = f"""
    New visitor detected:

    IP Address: {ip}
    Device Info: {user_agent}
    Language: {lang}
    -----------------------------
    """

    try:
        with open("visits.txt", "a", encoding="utf-8") as f:
            f.write(data + "\n")
    except Exception as e:
        print("Error saving visitor:", e)

    return "<h1>Welcome</h1><p>Your visit has been recorded.</p>"

# صفحة خاصة تعرض البيانات
@app.route('/data')
def show_data():
    if os.path.exists("visits.txt"):
        with open("visits.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    else:
        return "<h1>No visits recorded yet.</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
