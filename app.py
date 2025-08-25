from flask import Flask, request, Response
import datetime
import requests

app = Flask(__name__)

PASSWORD = "2345"

@app.route('/')
def home():
    ip = request.remote_addr

    # نحاول نجيب الموقع الجغرافي
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = geo.get("country", "Unknown")
        city = geo.get("city", "Unknown")
    except:
        country, city = "Unknown", "Unknown"

    user_agent = request.headers.get('User-Agent')
    lang = request.headers.get('Accept-Language')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = f"""
Time: {time}
IP Address: {ip}
Country: {country}
City: {city}
Device Info: {user_agent}
Language: {lang}
----------------------------
"""

    # يطبع في Logs
    print(data)

    # يخزن في ملف
    with open("visits.txt", "a", encoding="utf-8") as f:
        f.write(data)

    return "<h1>Welcome to APks.F</h1><p>Your visit has been recorded.</p>"

@app.route('/visits')
def show_visits():
    password = request.args.get("password", "")
    if password != PASSWORD:
        return Response("Access Denied: Wrong Password", status=403)

    try:
        with open("visits.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "No visits recorded yet."

    return f"<pre>{content}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
