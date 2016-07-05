__author__ = 'hayal808_mohmo449'


#from flask import Flask
#from flask import render_template
from flask import request
import sqlite3 as lite
from database_helper import db_helper
#from datetime import datetime, date
import json
from database_helper import StatusCodes
#from database_helper import Const
from database_helper import utility
from Twidder import app


#app = Flask(__name__)
#app.debug = True


#utility class
util = utility()



@app.route('/', methods=['POST', 'GET'])
def index():
    return app.send_static_file('client.html')


@app.route('/signin', methods=['POST'])
def login():
    try:
        dbhelper = db_helper()
        print("tt")
        email = request.get_json()['email']
        password = request.get_json()['password']
        token = dbhelper.login(email, password)

        if(token != StatusCodes.FAILURE and token != StatusCodes.DB_ERROR):
            print("gggg")
            return util.get_json_resp(True, "Successfully signed in.", token)
        else:
            return util.get_json_resp(False, "Wrong username or password.", None)
    except KeyError, e:
        print(e.args[0])
        return util.get_json_resp(False, "Wrong username or password.", None)


#adding user
@app.route('/signup', methods=['POST'])
def add_user():
    try:
        dbhelper = db_helper()
        email = request.get_json()['email']
        pwd = request.get_json()['password']
        firstname = request.get_json()['firstname']
        familyname = request.get_json()['familyname']
        gender = request.get_json()['gender']
        city = request.get_json()['city']
        country = request.get_json()['country']
        resp = dbhelper.add_user(email, pwd, firstname, familyname, gender, city, country)
        if(resp == StatusCodes.SUCCESS):
            return util.get_json_resp(True, "User added successfully..!!", None)
        elif(resp == StatusCodes.EMAIL_ALREADY_EXISTS):
            return util.get_json_resp(False, "User already exists.", None)
        elif(resp == StatusCodes.DB_ERROR):
            return util.get_json_resp(False, "Unable to add user", None)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Error adding user..!!", None)


@app.route('/sign_out', methods=['POST', 'GET'])
def sign_out():
    try:
        dbhelper = db_helper()
        token = request.get_json()['token']
        resp = dbhelper.sign_out(token)
        if(resp == StatusCodes.SUCCESS):
            return util.get_json_resp(True, "Successfully signed out.", None)
        elif(resp == StatusCodes.FAILURE):
            return util.get_json_resp(False, "You are not logged in.", None)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Error adding user..!!", None)


@app.route('/chgpwd', methods=['POST'])
def change_password():
    try:
        dbhelper = db_helper()
        #if(request.method == 'POST'):
        token = request.get_json()['token']
        o_pwd = request.get_json()['o_pwd']
        n_pwd = request.get_json()['n_pwd']
        #print(email, o_pwd, n_pwd)
        resp = dbhelper.change_password(token, o_pwd, n_pwd)
        if(resp == StatusCodes.SUCCESS):
            return util.get_json_resp(True, "Password changed successfully..!!", None)
        elif(resp == StatusCodes.FAILURE):
            return util.get_json_resp(False, "Wrong password.", None)
        elif(resp == StatusCodes.DB_ERROR):
            return util.get_json_resp(False, "Unable to add user", None)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Unable to change password. Please try Again later", None)


@app.route('/getuser_by_token/<token>', methods=['POST', 'GET'])
def get_user_data(token):
    try:
        dbhelper = db_helper();
        if(request.method == 'POST'):
            token = request.get_json()['token']

        u_data = dbhelper.get_user_data_by_token(token)
        if(u_data == StatusCodes.FAILURE):
            return util.get_json_resp(False, "No user found..!!", None)
        else:
            return util.get_json_resp(True, "User data retrieved.", u_data)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Oops, Something went wrong..!!", None)


@app.route('/getuser_by_email/<token>/<email>', methods=['POST', 'GET'])
def get_user_data2(token, email):
    try:
        dbhelper = db_helper();
        if(request.method == 'POST'):
            token = request.get_json()['token']
            email = request.get_json()['email']

        u_data = dbhelper.get_user_data_by_email(token, email)
        if(u_data == StatusCodes.FAILURE):
            return util.get_json_resp(False, "No user found..!!", None)

        if(u_data == StatusCodes.NOT_SIGNED_IN):
            return util.get_json_resp(False, "You are not signed in.", None)

        else:
            return util.get_json_resp(True, "User data retrieved.", u_data)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Oops, Something went wrong..!!", None)


@app.route('/getmsg_t/<token>', methods=['POST', 'GET'])
def get_user_messages_by_token(token):
    try:
        dbhelper = db_helper();
        if(request.method == 'POST'):
            token = request.get_json()['token']
        resp = dbhelper.get_user_messages_by_token(token)
        if(resp == StatusCodes.FAILURE):
            return util.get_json_resp(False, "No messages found for the user..!!", None)
        elif(resp == StatusCodes.DB_ERROR):
            return util.get_json_resp(False, "Unable to retrieve messages", None)
        else:
            return util.get_json_resp(True, "Messages retrieved successfully!", resp)
    except lite.Error, e:
         print("Error : %s" % e.args[0])
         return util.get_json_resp(False, "Oops, Something went wrong..!!", None)


@app.route('/getmsg/<token>/<email>', methods=['POST', 'GET'])
def get_user_messages_by_email(token, email):
    try:
        dbhelper = db_helper();
        resp = dbhelper.get_user_messages_by_email(token, email)
        if(resp == StatusCodes.FAILURE):
            return util.get_json_resp(False, "No messages found for the user..!!", None)
        elif(resp == StatusCodes.DB_ERROR):
            return util.get_json_resp(False, "Unable to retrieve messages", None)
        else:
            #print(resp)
            return util.get_json_resp(True, "Messages retrieved successfully!", resp)
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Oops, Something went wrong..!!", None)


@app.route('/postmsg/<token>/<msg>/<email>', methods=['POST', 'GET'])
def post_message(token, msg, email):
    try:
        if(request.method == 'POST'):
            token = request.get_json()['token']
            msg = request.get_json()['message']
            email = request.get_json()['email']
        #token = request.form['token']
        #msg = request.form['msg']
        #email = request.form['email']
        dbhelper = db_helper();
        resp = dbhelper.post_message(token, msg, email)
        if(resp == StatusCodes.FAILURE):
            return util.get_json_resp(False, "Unable to post message..!!", None)
        elif(resp == StatusCodes.DB_ERROR):
            return util.get_json_resp(False, "Unable to post message. Try later.!!", None)
        else:
            print("TEST")
            return util.get_json_resp(True, "Message posted successfully", None)
            print("TEST222")
    except lite.Error, e:
        print("Error : %s" % e.args[0])
        return util.get_json_resp(False, "Oops, Something went wrong..!!", None)

# #WEBSOCKET
@app.route('/check_token/<token>', methods=['POST', 'GET'])
def check_token(token):
    try:
        dbhelper = db_helper();
        if request.environ.get("wsgi.websocket"):
            ws = request.environ["wsgi.websocket"]
            while True:
                message = ws.receive()
                message = json.loads(message)
                #print(message['token'])
                resp = dbhelper.check_token_exist(message['token'])
                print (resp)
            #ws.send(json.dumps(False))
                ws.send(json.dumps(resp))

        return

    except lite.Error, e:
         print("Error : %s" % e.args[0])
         return util.get_json_resp(False, "Oops, Something went wrong..!!", None)


# #WEBSOCKET
# @app.route('/getmsg_t_ws/<token>', methods=['POST', 'GET'])
# def get_user_messages_by_token2(token):
#     try:
#         dbhelper = db_helper();
#
#         if request.environ.get("wsgi.websocket"):
#             ws = request.environ["wsgi.websocket"]
#             while True:
#                 message = ws.receive()
#                 message = json.loads(message)
#                 print(message['token'])
#                 print("HEEEEEEEEEEEEEERE")
#                 resp = dbhelper.get_user_messages_by_token(message['token'])
#                 ws.send(json.dumps(resp))
#                 print (resp)
#         return
#
#     except lite.Error, e:
#          print("Error : %s" % e.args[0])
#          return util.get_json_resp(False, StatusCodes.FAILURE, "Oops, Something went wrong..!!")
