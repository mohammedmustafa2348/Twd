from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return app.send_static_file('/static/client.html')

if __name__ == "__main__":
    app.run()