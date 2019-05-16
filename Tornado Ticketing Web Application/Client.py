# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:03:48 2019

@author: Mah
"""

import requests
import os
import time
import platform
import sys
from binascii import hexlify
from os import system
PARAMS = CMD = USERNAME = PASSWORD = API = " "
HOST = "127.0.0.1"
PORT = "1138"
def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"

def clear():
    _ = system('cls')
while 1:
    clear()
    print('Wellcome to the ticketing system \n please choose between options below \n 1.signin \n 2.signup \n 3.exit \n')
    status = sys.stdin.readline()
    if status[:-1] == '1':
        clear()
        print("What kind of login do you prefer?\n 1.API \n 2.Username/Password")
        login_type = sys.stdin.readline()
        if login_type[:-1] == '1':
            clear()
            while 1:
                print('API: ')
                API = sys.stdin.readline()
                CMD = 'login'
                PARAMS = {'api' : API, 'username':'', 'password':''}
                re = requests.post(__postcr__(), PARAMS).json()
                print('{}\n {}'.format(re['message'], re['code']))
                if re['code'] == '200':
                    time.sleep(2)
                    break
                else:
                    clear()
                    print('Something is wrong!')
                    time.sleep(2)
            while 1:
                clear()
                if sql_query(r, 'select type from users where username = {}'.format(username))[0] == 'Normal':
                    print('Choose between the options below: \n 1.send a ticket \n 2.edit a ticket \n 3.read a ticket \n 4.exit \n')
                    op = sys.stdin.readline()
                    if op[:-1]=='1':
                        clear()
                        print ("subject: \n")
                        subject = sys.stdin.readline()
                        print("body: \n")
                        body = sys.stdin.readline()
                        clear()
                        PARAMS = {'username': '', 'password' : '', 'api' : API,'subject':subject, 'body':body, 'date': '', 'token': str(hexlify(os.urandom(16))), 'id': 'Open'}
                        CMD = 'sendticket'
                        
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {} \n code: {} \n id: {}'.format(re['message'], re['code']))
                    elif op[:-1]=='2':
                        clear()
                        print('token: \n')
                        token = sys.stdin.readline()
                        print('id: \n')
                        idd = sys.stdin.readline()
                        clear()
                        PARAMS = {'username': '', 'password' : '', 'api' : API}
                        CMD = 'check'
                        re = requests.post(__postcr__(), PARAMS).json()
                        if re['tag'] == '1':
                            PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token, 'id':idd}
                            CMD = 'changeadmin'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('message: {} \n code: {}'.format(re['message'], re['code']))
                        else:
                            PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token, 'id':idd}
                            CMD = 'changeuser'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('message: {}'.format(re['message']))
                    elif op[:-1] == '3':
                        clear()
                        print('token: \n')
                        token = sys.stdin.readline()
                        clear()
                        PARAMS = {'username': '', 'password' : '', 'api' : API}
                        CMD = 'check'
                        re = requests.post(__postcr__(), PARAMS).json()
                        if re['tag'] == '1':
                            PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token}
                            CMD = 'readticketadmin'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                        else:
                            PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token}
                            CMD = 'readticketuser'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                            
                    elif op[:-1] == '4':
                        clear()
                        CMD = 'logout'
                        PARAMS = {'api' : API, 'username':username, 'password':password}
                        re = requests.post(__postcr__(), PARAMS).json()
                        print (re['message'])
            elif login_type[:-1] == '2':
                clear()
                while 1:
                    print('username: ')
                    username = sys.stdin.readline()
                    print('password: ')
                    password = sys.stdin.readline()
                    CMD = 'login'
                    PARAMS = {'api' : '', 'username':username, 'password':password}
                    re = requests.post(__postcr__(), PARAMS).json()
                    print('{}\n {} n api: {}'.format(re['message'], re['code'], re['token']))
                    if re['code'] == '200':
                        time.sleep(2)
                        break
                    else:
                        clear()
                        print('Something is wrong!')
                        time.sleep(2)
                while 1:
                    clear()
                    print('Choose between the options below: \n 1.send a ticket \n 2.edit a ticket \n 3.read a ticket \n 4.exit \n')
                    op = sys.stdin.readline()
                    if op[:-1]=='1':
                        clear()
                        print ("subject: \n")
                        subject = sys.stdin.readline()
                        print("body: \n")
                        body = sys.stdin.readline()
                        clear()
                        PARAMS = {'api' : '', 'username':username, 'password':password,'subject':subject, 'body':body, 'date': '', 'token': str(hexlify(os.urandom(16))), 'id': 'Open'}
                        CMD = 'sendticket'
                        
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {} \n code: {} \n id: {}'.format(re['message'], re['code']))
                    elif op[:-1]=='2':
                        clear()
                        print('token: \n')
                        token = sys.stdin.readline()
                        print('id: \n')
                        idd = sys.stdin.readline()
                        clear()
                        PARAMS = {'api' : '', 'username':username, 'password':password}
                        CMD = 'check'
                        re = requests.post(__postcr__(), PARAMS).json()
                        if re['tag'] == '1':
                            PARAMS = {'api' : '', 'username':username, 'password':password,'token':token, 'id':idd}
                            CMD = 'changeadmin'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('message: {} \n code: {}'.format(re['message'], re['code']))
                        else:
                            PARAMS = {'api' : '', 'username':username, 'password':password,'token':token, 'id':idd}
                            CMD = 'changeuser'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('message: {}'.format(re['message']))
                    elif op[:-1] == '3':
                        clear()
                        print('token: \n')
                        token = sys.stdin.readline()
                        clear()
                        PARAMS = {'api' : '', 'username':username, 'password':password}
                        CMD = 'check'
                        re = requests.post(__postcr__(), PARAMS).json()
                        if re['tag'] == '1':
                            PARAMS = {'api' : '', 'username':username, 'password':password,'token':token}
                            CMD = 'readticketadmin'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                        else:
                            PARAMS = {'api' : '', 'username':username, 'password':password,'token':token}
                            CMD = 'readticketuser'
                            re = requests.post(__postcr__(), PARAMS).json()
                            print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                    
                    elif op[:-1] == '4':
                        clear()
                        CMD = 'logout'
                        PARAMS = {'api' : API, 'username':username, 'password':password}
                        re = requests.post(__postcr__(), PARAMS).json()
                        print (re['message'])
        else:
            print('Choose between the options below: \n 1.send a ticket \n 2.edit a ticket \n 3.read a ticket \n 4.respond \n 5.exit \n')
             op = sys.stdin.readline()
             if op[:-1]=='1':
                 clear()
                 print ("subject: \n")
                 subject = sys.stdin.readline()
                 print("body: \n")
                    body = sys.stdin.readline()
                    clear()
                    PARAMS = {'username': '', 'password' : '', 'api' : API,'subject':subject, 'body':body, 'date': '', 'token': str(hexlify(os.urandom(16))), 'id': 'Open'}
                    CMD = 'sendticket'
                        
                    re = requests.post(__postcr__(), PARAMS).json()
                    print('message: {} \n code: {} \n id: {}'.format(re['message'], re['code']))
                elif op[:-1]=='2':
                    clear()
                    print('token: \n')
                    token = sys.stdin.readline()
                    print('id: \n')
                    idd = sys.stdin.readline()
                    clear()
                    PARAMS = {'username': '', 'password' : '', 'api' : API}
                    CMD = 'check'
                    re = requests.post(__postcr__(), PARAMS).json()
                    if re['tag'] == '1':
                        PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token, 'id':idd}
                        CMD = 'changeadmin'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {} \n code: {}'.format(re['message'], re['code']))
                    else:
                        PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token, 'id':idd}
                        CMD = 'changeuser'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {}'.format(re['message']))
                elif op[:-1] == '3':
                    clear()
                    print('token: \n')
                    token = sys.stdin.readline()
                    clear()
                    PARAMS = {'username': '', 'password' : '', 'api' : API}
                    CMD = 'check'
                    re = requests.post(__postcr__(), PARAMS).json()
                    if re['tag'] == '1':
                        PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token}
                        CMD = 'readticketadmin'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                    else:
                        PARAMS = {'username': '', 'password' : '', 'api' : API,'token':token}
                        CMD = 'readticketuser'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                        
                elif op[:-1] == '4':
                    clear()
                    CMD = 'logout'
                    PARAMS = {'api' : API, 'username':username, 'password':password}
                    re = requests.post(__postcr__(), PARAMS).json()
                    print (re['message'])
        elif login_type[:-1] == '2':
            clear()
            while 1:
                print('username: ')
                username = sys.stdin.readline()
                print('password: ')
                password = sys.stdin.readline()
                CMD = 'login'
                PARAMS = {'api' : '', 'username':username, 'password':password}
                re = requests.post(__postcr__(), PARAMS).json()
                print('{}\n {} n api: {}'.format(re['message'], re['code'], re['token']))
                if re['code'] == '200':
                    time.sleep(2)
                    break
                else:
                    clear()
                    print('Something is wrong!')
                    time.sleep(2)
            while 1:
                clear()
                print('Choose between the options below: \n 1.send a ticket \n 2.edit a ticket \n 3.read a ticket \n 4.exit \n')
                op = sys.stdin.readline()
                if op[:-1]=='1':
                    clear()
                    print ("subject: \n")
                    subject = sys.stdin.readline()
                    print("body: \n")
                    body = sys.stdin.readline()
                    clear()
                    PARAMS = {'api' : '', 'username':username, 'password':password,'subject':subject, 'body':body, 'date': '', 'token': str(hexlify(os.urandom(16))), 'id': 'Open'}
                    CMD = 'sendticket'
                    
                    re = requests.post(__postcr__(), PARAMS).json()
                    print('message: {} \n code: {} \n id: {}'.format(re['message'], re['code']))
                elif op[:-1]=='2':
                    clear()
                    print('token: \n')
                    token = sys.stdin.readline()
                    print('id: \n')
                    idd = sys.stdin.readline()
                    clear()
                    PARAMS = {'api' : '', 'username':username, 'password':password}
                    CMD = 'check'
                    re = requests.post(__postcr__(), PARAMS).json()
                    if re['tag'] == '1':
                        PARAMS = {'api' : '', 'username':username, 'password':password,'token':token, 'id':idd}
                        CMD = 'changeadmin'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {} \n code: {}'.format(re['message'], re['code']))
                    else:
                        PARAMS = {'api' : '', 'username':username, 'password':password,'token':token, 'id':idd}
                        CMD = 'changeuser'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('message: {}'.format(re['message']))
                elif op[:-1] == '3':
                    clear()
                    print('token: \n')
                    token = sys.stdin.readline()
                    clear()
                    PARAMS = {'api' : '', 'username':username, 'password':password}
                    CMD = 'check'
                    re = requests.post(__postcr__(), PARAMS).json()
                    if re['tag'] == '1':
                        PARAMS = {'api' : '', 'username':username, 'password':password,'token':token}
                        CMD = 'readticketadmin'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                    else:
                        PARAMS = {'api' : '', 'username':username, 'password':password,'token':token}
                        CMD = 'readticketuser'
                        re = requests.post(__postcr__(), PARAMS).json()
                        print('{} \n {} \n {}'.format(re['tickets'], re['code'], re['block 0']))
                
                elif op[:-1] == '4':
                    clear()
                    CMD = 'response'
                    if sql_query(r, 'select type from users where username = {} or api = {}'.format(username, api))[0]=='Admin':
                        print('token:')
                        token = sys.stdin.readline()
                        print('body:')
                        body = sys.stdin.readline()
                        PARAMS = {'api' : API, 'username':username, 'password':password, 'response' :body, 'token':token}
                        re = requests.post(__postcr__(), PARAMS).json()
                        print (re['message'])
                    
                elif op[:-1] == '5':
                    clear()
                    CMD = 'logout'
                    PARAMS = {'api' : API, 'username':username, 'password':password}
                    re = requests.post(__postcr__(), PARAMS).json()
                    print (re['message'])
                    ########################################################################
        ############################################################################copy
        #################################################################################################
############################################################################################
        
    elif status[:-1] == '2':
        clear()
        print('username:')
        username = sys.stdin.readline()
        print('password:')
        password = sys.stdin.readline()
        print('type:')
        typee = sys.stdin.readline()
        clear()
        PARAMS = {'type' : typee, 'username':username, 'password':password}
        CMD = 'signup'
        re = requests.post(__postcr__(), params=PARAMS).json()
        if str(re['code']) =='200':
            print('message: {} \n code: {} \n api: {} \n'.format(re['message'], re['code']))
        else:
            print('message: {} \n code: {} \n api: {} \n'.format(re['message'], re['code']))
        
        time.sleep(5)
#    elif status[:-1] == '3':
