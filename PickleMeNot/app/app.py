from flask import Flask, request, render_template
import base64, pickle
from pydantic import BaseModel

class UserInput(BaseModel):
    command: str

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("form.html")

@app.route('/validate')
def index_js():
    return render_template("formJSvalidate.html")

@app.route('/submit', methods=["POST"])
def submit():
    payload = request.form.get("payload", "")
    try:
        decoded = base64.b64decode(payload)
        obj = pickle.loads(decoded)
        user = UserInput(**obj) # <---RCE happens here
        return f"Command to run: {user.command}" #<-- Pydantic check happens here
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

