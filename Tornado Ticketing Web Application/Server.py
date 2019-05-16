# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:48:02 2019

@author: Mah
"""

import os.path
#import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options
import sqlite3
from sqlite3 import Error


define("port", default=1138, help="run on the given port", type=int)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def sql_execute(conn, exe_sql):
    try:
        c = conn.cursor()
        c.execute(exe_sql)
        conn.commit()
    except Error as e:
        print(e)
        
def sql_query(conn, q):
    try:
        c = conn.cursor()
        c.execute(q)
        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)
        return False


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/signup/([^/]+)/([^/]+)", signup),
#            # POST METHOD :
            (r"/signup", signup),
            (r"/sendticket", sendticket),  # Balance Using API Format : /apibalance/API
            (r"/readticketuser", readticket_user),# Balance Using Authentication Format : /authbalance/Username/Password
            (r"/readticketadmin", readticket_admin),  # deposit Using API Format : /apideposit/API/Amount
            (r"/changeuser", change_user), # deposit Using Authentication Format : /authdeposit/Username/Password/Amount
            (r"/changeadmin", change_admin),# Withdeaw Using API Format : /apiwithdraw/API/amount
            (r"/response", response),
            (r"/login", login),
            (r"/logout", logout), # Withdeaw using  AuthenticationFormat : /apiwithdraw/username/password/amount
            (r".*", defaulthandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)

r = create_connection("E:\\sa.sqlite3")
class BaseHandler(tornado.web.RequestHandler):
    @property
    def check_user(user):
        print(user)
        

    def check_api(self,api):
        resuser = sql_query(r, 'SELECT * from users where api = {}'.format(api))
        if resuser:
            return True
        else:
            return False
    def check_auth(self,username,password):
        resuser = sql_query('SELECT * from users where username = {} and password = {}', username,password)
        if resuser:
            return True
        else:
            return False

class defaulthandler(BaseHandler):
    def get(self):
        output = {'a':'b'}
        self.write(output)

    def post(self, *args, **kwargs):
        output = {"status":"Wrong Command"}
        self.write(output)


class signup(BaseHandler):
    def get(self, *args):
        #self.write("Hello World~")
        output = {self.get_argument('username') : self.get_argument('password')}
        self.write(output)
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        resuser = sql_query(r, 'SELECT * from users where username = {}'.format(username))
        print('*********************************')
        print(resuser)
        if not resuser:
            api = str(hexlify(os.urandom(16)))
            sql_execute(r, 'insert into users values({},{},{},"Normal")'.format(username, password, api))
            r.commit()
            output = {'message':'User successfully added!', 'code':'200', 'api':api}
            self.write(output)
        else:
            output = {'message':'User exits!', 'code':'201'}
            self.write(output)
class sendticket(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        date = self.get_argument('date')
        if self.check_auth(username, password) or self.check_api(api):
            sql_execute(r, 'insert into tickets values({}, {}, {}, {}, {}, {}, NULL)'.format(
                    str(hexlify(os.urandom(16))), username, 'Open', subject, body, date))
            output = {'message':'Ticket successfully sent!', 'id':'Open', 'code':'200'}
            self.write(output)
        else:
            output = {'message': 'Unsuccessful', 'code': '201'}
            self.write(output)

class readticket_user(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        token = self.get_argument('token')
        if self.check_auth(username, password) or self.check_api(api):
            w = sql_query(r, 'select * from tickets where token = {}'.format(token))
            if w[1] ==username or w[1] == sql_query(r, 'select * from users where api = {}'.format(api))[0]:
                output = {'tickets' : 'there are -1- Ticket', 'code' : '200', 'block 0' : '"subject": {} \n"body": {} \n "status":{} \n "id":NULL \n "date":{}'.format(w[3], w[4], w[2], w[5])}
                self.write(output)
            else:
                output = {'message':'Not allowed!'}
                self.write(output)

            
class readticket_admin(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        token = self.get_argument('token')
        if self.check_auth(username, password) or self.check_api(api):
            if sql_query(r, 'select * from users where api = {}'.format(api))[3] =='Admin' or sql_query(r, 'select * from users where username = {}'.format(username))[3] =='Admin':
                w = sql_query(r, 'select * from tickets where token = {}'.format(token))
                output = {'tickets' : 'there are -1- Ticket', 'code' : '200', 'block 0' : '"subject": {} \n"body": {} \n "status":{} \n "id":NULL \n "date":{}'.format(w[3], w[4], w[2], w[5])}
                self.write(output)
            else:
                output = {'message':'Not allowed!'}
                self.write(output)
class change_user(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        token = self.get_argument('token')
        idd = self.get_argument('id')
        if self.check_auth(username, password) or self.check_api(api):
            w = sql_query(r, 'select * from tickets where token = {}'.format(token))
            if w[1] ==username or w[1] == sql_query(r, 'select * from users where api = {}'.format(api))[0]:
                sql_execute(r, 'update tickets set id = {} where token = {}'.format(idd, token))
                output = {'message' : 'Changed Successfully!', 'code' : '200'}
                self.write(output)
            else:
                output = {'message':'Not allowed!'}
                self.write(output)
                
class check(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        qq = sql_query(r, 'select * from users where username = {} or api={}'.format(username, api))
        if qq[3] == 'Admin':
            output = {'tag' : '1'}
            self.write(output)
        else:
            output = {'tag' : '0'}
            self.write(output)

class change_admin(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        token = self.get_argument('token')
        idd = self.get_argument('id')
        if self.check_auth(username, password) or self.check_api(api):
            if sql_query(r, 'select * from users where api = {}'.format(api))[3] =='Admin' or sql_query(r, 'select * from users where username = {}'.format(username))[3] =='Admin':
                sql_execute(r, 'update tickets set id = {} where token = {}'.format(idd, token))
                output = {'message' : 'Changed Successfully!', 'code' : '200'}
                self.write(output)
            else:
                output = {'message':'Not allowed!'}
                self.write(output)                

class response(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        token = self.get_argument('token')
        response = self.get_argument('response')
        if self.check_auth(username, password) or self.check_api(api):
            if sql_query(r, 'select * from users where api = {}'.format(api))[3] =='Admin' or sql_query(r, 'select * from users where username = {}'.format(username))[3] =='Admin':
                sql_execute(r, 'update tickets set response = {} where token = {}'.format(response, token))
                output = {'message' : 'Response made Successfully!', 'code' : '200'}
                self.write(output)
            else:
                output = {'message':'Not allowed!'}
                self.write(output)

class login(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        if self.check_auth(username, password):
            ss = str(hexlify(os.urandom(16)))
            sql_execute(r, 'update users set api = {} where username = {}'.format(api, username))
            output = {'message' : 'Logged in Successfully', 'code' : '200', 'token' : ss}
            self.write(output)
        elif self.check_api(api):
            output = {'message' : 'Logged in Successfully', 'code' : '201'}
            self.write(output)

class logout(BaseHandler):
    def get(self):
        pass
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        api = self.get_argument('api')
        sql_execute(r, 'update users set api = {} where username = {} or api={}'.format('', username,api))
        output = {'message' : 'Logged out Successfully', 'code' : '200'}
        self.write(output)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    

if __name__ == "__main__":
    main()