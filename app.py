from flask import Flask, request
import smtplib
import os

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    lang = request.headers.get('Accept-Language')

    subject = "New Visitor"
    body = f"""
    New visitor detected:

    IP Address: {ip}
    Device Info: {user_agent}
    Language: {lang}
    """
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, message)
    except Exception as e:
        print("Error:", e)

    return "<h1>Welcome</h1><p>Your visit has been recorded.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
