from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    request_token = request.args.get('request_token')
    return f"Request Token: {request_token}"

if __name__ == '__main__':
    app.run(port=5000)
