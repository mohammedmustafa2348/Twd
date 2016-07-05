__author__ = 'hayal808_mohmo449'


import sqlite3 as lite
from flask import g
from datetime import datetime, date
#from server import StatusCodes
#from server import util
import json
import random
import string

class db_helper(object):

    def __init__(self, dbn="Twidder/database.db",):
        self.db_name = dbn
        self.util = utility()



    def connect_db(self):
        return  lite.connect(self.db_name)

    def get_db(self):
        db = getattr(g, 'db', None)
        if db is None:
            db = g.db = self.connect_db()
        return db
#    def init(self):
#        con = self.get_db()

    #function to authenticate the user credentials
    def login(self, email, pwd):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("select u.firstname, u.familyname from t_user_data u, t_login_det l where u.email = ? "
                           " and u.email = l.email "
                           " and l.pwd = ?", (email, pwd))
            row = cursor.fetchone()
            if(row != None ):
                #token generation
                first_name, family_name = row[0], row[1]
                #token = self.util.get_unique_token(email, first_name, family_name)
                token = self.get_unique_token()
                #print(token, first_name, family_name)
                cursor.execute("update t_login_det set token = ? where email = ?", (token, email))
                con.commit()
                #if(con.total_changes > 0):
                    #print ("Updated the token successfully..")
                return token
            else:
                return StatusCodes.FAILURE
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()




    def sign_out(self, token):
        con = None
        try:
            #if self.check_token_exist(token):
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("update t_login_det set token = ? where token = ?", (None, token))
            ret = con.total_changes
            if(ret == 1):
                con.commit()
                return StatusCodes.SUCCESS
            return StatusCodes.FAILURE
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()


    #Adding User details when a new user is signing up
    def add_user(self, email, pwd, first_name, family_name, gender, city, country):
        con = None
        try:
            #print("Adding user details...")
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("select count(email) from t_user_data where email = ?", (email,))
            ret = cursor.fetchone()
            if(ret != None):
                count = ret[0]
                #print(count)
                if(count > 0):
                    return StatusCodes.EMAIL_ALREADY_EXISTS
                else:
                    cursor.execute("insert into t_user_data(email, firstname, familyname, gender, city, country) values (?,?,?,?,?,?)",
                                   (email, first_name, family_name, gender, city, country))
                    #initially token's value is same as email
                    cursor.execute("insert into t_login_det(email, pwd, token) values(?,?,?)", (email, pwd, email))
                    con.commit()
                    return StatusCodes.SUCCESS
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()

    #retrieve the user details for the passed token
    def get_user_data_by_token(self, token):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("select u.* from t_user_data u, t_login_det l where u.email = l.email "
                           " and l.token = ? ", (token,))
            row = cursor.fetchone()
            #print(row)
            if(row != None):
                user = self.util.get_user_json(row)
                #print(user)
                return user
            else:
                return StatusCodes.FAILURE
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()

    #retrieve the user details for the passed token
    def get_user_data_by_email(self, token, email):
        con = None
        try:
            if self.check_token_exist(token):
                con = self.get_db()
                cursor = con.cursor()
                cursor.execute("select u.* from t_user_data u where u.email = ?", (email,))
                row = cursor.fetchone()
                #print(row)
                if(row != None):
                    user = self.util.get_user_json(row)
                    #print(user)
                    return user
                else:
                    return StatusCodes.FAILURE
            else: #token not found, user is logged of
                return StatusCodes.NOT_SIGNED_IN
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()


    #change the password with new password
    def change_password(self, token, o_pwd, n_pwd):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("update t_login_det set pwd = ? where token = ? and pwd = ? " , (n_pwd, token, o_pwd))
            ret = con.total_changes
            #print(ret)
            if(ret == 1):
                con.commit()
                return StatusCodes.SUCCESS
            else:
                return StatusCodes.FAILURE
        except lite.Error, e:
            print ("DB Error: " + e.args[0])
            return StatusCodes.FAILURE
        finally:
            if con:
                con.close()


    #get user messages by token
    def get_user_messages_by_token(self, token):
        con = None
        msg_list = []
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("select m.*, d.firstname, d.familyname from t_login_det l, t_user_msg m, t_user_data d where l.token = ? and l.email = m.email and d.email = m.posted_by", (token,))
            rows = cursor.fetchall()
            if(rows != None):
                for row in rows:
                    #print(row)
                    msg_list.append(self.util.get_message_json(row))
                #print(msg_list)
                return msg_list
            else:
                return StatusCodes.FAILURE
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()

    #retrieves the messages posted for the user identified by the email
    def get_user_messages_by_email(self, token, email):
        con = None
        msg_list = []
        try:
            if self.check_token_exist(token):
                con = self.get_db()
                cursor = con.cursor()
                #print(email)
                cursor.execute("select m.*, d.firstname, d.familyname from t_user_msg m, t_user_data d where m.email = ? and d.email = m.posted_by", (email,))
                rows = cursor.fetchall()
                if(rows != None):
                    print("ggg")
                    for row in rows:
                        #print(row)
                        msg_list.append(self.util.get_message_json(row))
                    #print(msg_list)
                    return msg_list
                else:
                    print("HELLLO")
                    return StatusCodes.FAILURE
            else: #token not found, user is logged of
                return StatusCodes.NOT_SIGNED_IN
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()

    #posting message into a person's wall
    def post_message(self, token, message, email):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            #print(token)
            cursor.execute("select l.email from t_login_det l where l.token = ?", (token,))
            row = cursor.fetchone()
            #print(row)
            if(row != None):
                posted_by_email = row[0]
                print("post by : ", posted_by_email)
                cursor.execute("insert into t_user_msg(email, message, posted_by) values (?,?,?)",
                               (email, message, posted_by_email))
                if(con.total_changes):
                    print("Posted the message successfully...!!")
                    con.commit()
                    return StatusCodes.SUCCESS
                else:
                    return StatusCodes.FAILURE
            else:
                return StatusCodes.FAILURE
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return StatusCodes.DB_ERROR
        finally:
            if con != None:
                con.close()


    def add_login_det(self, email, password, token):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("insert into tr_login_det(email, password, token) values (?,?,?)", (email, password, token))
            con.commit()
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return 0
        finally:
            if con != None:
                con.close()

    def get_login_det(self, email):
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("select password, token from tr_login_det where email = ?", (email,))
            row = cursor.fetchone()
            return (row[0], row[1])
        except lite.Error, e:
            print ("Error: " + e.args[0])
            return 0
        finally:
            if con:
                con.close()

    def add_message(self, email, message):
        con = None
        try:
            con = self.get_db()
            cursor = con.cursor()
            cursor.execute("insert into t_user_msg(email, message, twt_time) values (?,?,?)", (email, message, datetime.now()))
            con.commit()
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return 0
        finally:
            if con != None:
                con.close()



    def get_unique_token(self): #, email):
        con = None
        #rand_num = 0
        try:
            con = self.get_db()
            cursor = con.cursor()
            #print("Generating random number for token..!!")
            while (True):
                #rand_num = self.util.get_random_num()
                token = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(128))
                #print(token)
                cursor.execute("select token from t_login_det where token = ?", (token,))
                ret = cursor.fetchone()
                if(ret == None):
                    #if(ret[0] == 0):
                    #break
                    print(token)
                    return token
                #print("detected duplicate!")
                #else:
                #    break
            #print(rand_num)
            #return token #rand_num
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return 0
        #finally:
            #if con != None:
             #   con.close()
            #return rand_num


    def check_token_exist(self, token):
        con = None
        rand_num = 0
        try:
            con = self.get_db()
            cursor = con.cursor()


            cursor.execute("select token from t_login_det where token = ?",(token,))
            ret = cursor.fetchone()
            if(ret != None ):
                #if(ret[0] > 0):
                return True
            return False
        except lite.Error, e:
            print("DB Error: " + e.args[0])
            return 0
        #finally:
        #    if con != None:
        #        con.close()



    def close(self):
        self.get_db.close()


class utility:

    def __init__(self):
        pass

    #generating JSON string for User from the passed User tuple
    def get_user_json(self, user):
        j_str = ""
        try:
            if(user != None):
                j_str = {Const.EMAIL:user[0], Const.FIRST_NAME:user[1],
                         Const.FAMILY_NAME:user[2], Const.GENDER:user[3],
                         Const.CITY:user[4], Const.COUNTRY:user[5]}
                return j_str
        except BaseException, be:
            print("Error while parsing user %s" %be.args[0])

    #generating JSON string for Message from the passed Message tuple


    def get_message_json(self, msg):
        j_str = ""
        try:
            if(msg != None):
                j_str = {Const.EMAIL:msg[0], Const.MESSAGE:msg[1],
                         Const.POSTED_BY:msg[2], Const.TWEET_TIME:msg[3],
                         Const.FIRST_NAME:msg[4], Const.FAMILY_NAME:msg[5]}
                return j_str
        except BaseException, be:
            print("Error while parsing message %s" %be.args[0])

    #generates JSON string for response with the passed params
    def get_json_resp(self, func_stat, message, data):
        resp = {Const.FUNC_STAT:func_stat, Const.MESSAGE:message,Const.DATA:data}
        return json.dumps(resp)



class StatusCodes:
    EMAIL_ALREADY_EXISTS = 10
    EMAIL_DOES_NOT_EXISTS = 20
    SUCCESS = 1
    FAILURE = -1
    NOT_SIGNED_IN = -2
    DB_ERROR = -3
    FAIL_STR = "failure"
    SUC_STR = "success"

class Const:
    FUNC_STAT = "success"
    STAT = "stat"
    DATA = "data"
    TYPE_EMAIL = "e"
    TYPE_TOKEN = "t"

    #message constants
    MESSAGE = "message"
    POSTED_BY = "posted_by"
    TWEET_TIME = "twt_time"

    #user constants
    EMAIL = "email"
    PWD = "pwd"
    FIRST_NAME = "firstname"
    FAMILY_NAME = "familyname"
    GENDER = "gender"
    CITY = "city"
    COUNTRY = "country"
    TOKEN = "token"