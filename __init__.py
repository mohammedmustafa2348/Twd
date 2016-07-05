__author__ = 'hayal808_mohmo449'


from flask import Flask, request
app = Flask(__name__, static_url_path='')
import Twidder.server

if __name__ == '__main__':
        app.run()