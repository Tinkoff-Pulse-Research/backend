from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def app_root():
    return jsonify(
        {"status": "ok", "message": "pong"}
    ), 200

if __name__ == '__main__':
    app.run()