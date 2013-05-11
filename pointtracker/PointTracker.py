#from wsgiref.simple_server import make_server
#from pyramid.mako_templating import renderer_factory as mako_factory
#from pyramid.config import Configurator

#sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
#sys.path.insert(0, 'c:/')

#sys.path.append('D:\Office Stuff\Office Data\My Dropbox\Python Projects\PointTracker\airline_scrapers')
#import os
#import sys

#Then in your code that gets the username and password, you just do:

#from pyramid.security import remember

#remember(request, <bool>)
#The bool is True to remember the password and False to not remember.
#Then to check to see if the person is logged in, you do
#if authenticated_userid(request):
#You can also decorate your route handlers by adding permission=Authenticated as a final param. We can have lunch sometime and I can show you how this all fits together. Probably can't do it for a week and a half. We are going skiing for a week so I'm slammed trying to get everything in place by Friday.



import airline_scrapers.american
import airline_scrapers.united
import airline_scrapers.britishairways
import airline_scrapers.delta
import airline_scrapers.usairways
import airline_scrapers.evaair
#from ptserver import AES_Key

import mtk              #Mike's toolkit
#import subprocess
from pymongo import Connection
import uuid
import hashlib
#import base64
import Globalvars
import os



def Init_App():
    Globalvars.AES_Key = mtk.read_file("AES_Key.dng")
    Globalvars.Saltstring = mtk.read_file("Saltstring.dng")

    global  PT_database

    if Globalvars.DEVELOPMENT:
        mongo_con = Connection('localhost', 27017)
        mongo_db = mongo_con.PT_database                                     ## is the database created? if not created it (PT_database)
    else:
        mongo_con = Connection(os.environ['OPENSHIFT_MONGODB_DB_HOST'],
                           int(os.environ['OPENSHIFT_MONGODB_DB_PORT']))

        mongo_db = mongo_con[os.environ['OPENSHIFT_APP_NAME']]
#        mongo_db.authenticate('admin','UvdYhEC48mNd')
        mongo_db.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],
                              os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'])



    PT_database = mongo_db.PT_accounts                           ## Create our collection



#    subprocess.Popen(['C:\\Dropbox\\PyProjects\\PointTracker\\pointtracker\\mongodb\\bin\\mongod', '--dbpath', 'C:\\Dropbox\\PyProjects\\PointTracker\\pointtracker\\static\\mongodb\\'])  ## Start the Mongo Database daemon

    return




def Init_PointTracker_Database():
    global  PT_database

#    subprocess.Popen(['C:\\Dropbox\\PyProjects\\PointTracker\\pointtracker\\mongodb\\bin\\mongod', '--dbpath', 'C:\\Dropbox\\PyProjects\\PointTracker\\pointtracker\\static\\mongodb\\'])  ## Start the Mongo Database daemon

    con = Connection('localhost', 27017)
    db = con.PT_database                                     ## is the database created? if not created it (PT_database)
    PT_database = db.PT_accounts                           ## Create our collection
    return


def Update_PointTracker_Database(PT_account):
#    Encrypt_PT_account_Reward_Program_Passwords(PT_account)                                 #encrypt all Reward Program Password before sending to database
    PT_database.update({'_id':PT_account['_id']} ,{'PT_account':PT_account})
    return PT_account


def Insert_PointTracker_Database(PT_account):
#    Encrypt_PT_account_Reward_Program_Passwords(PT_account)                                 #encrypt all Reward Program Password before sending to database
    PT_database.insert({'_id':PT_account['_id'],'PT_account':PT_account})
    return





def Get_PointTracker_Account(_id):
    db_obj = PT_database.find_one({'_id':_id})
    if db_obj is None:
        PT_account = None                                                   ## No such PT_account
    else:
        PT_account = db_obj['PT_account']
#        Remove_PT_account_Reward_Program_Passwords(PT_account)                             #we need to remove RP_account passwords so that they can't be seen on client side
#        Decrypt_PT_account_Reward_Program_Passwords(PT_account)                             #we need to decrypt RP_account passwords so that they can be edited on the client side
#        Encrypt_PT_account_Reward_Program_Passwords(PT_account)
    return PT_account                                               ## return the a valid authentiated PT_account





def Register_PointTracker_Account(register_info):

    PT_account = {
                    "_id" : "",
                    "PT_account_lastname" :  "Guest_lastname",
                    "PT_account_firstname" : "Guest_firstname",
#                    "PT_password" :          "Guest_password",
                    "PT_username" :          "Guest_username",
                    "PT_sub_accounts" : [{
                        "SA_id":"",
                        "SA_name" : "Guest_firstname",
                        "SA_program_accounts" : []
                      }],
                  }


    hash = hashlib.sha256()
    string = register_info['username']  + Globalvars.Saltstring + register_info['password']
    encode_string = string.encode('utf-8')

    hash.update(encode_string)

    _id = hash.hexdigest()

    PT_account['_id'] = _id
    PT_account['PT_account_firstname'] = register_info['firstname']
    PT_account['PT_account_lastname'] =  register_info['lastname']
    PT_account['PT_username'] = register_info['username']
#    PT_account['PT_password'] = register_info['password']
#    PT_account['PT_email'] = register_info['email']

    Sub_accounts = PT_account['PT_sub_accounts']
    Sub_account = Sub_accounts[0]
    Sub_account['SA_name'] = register_info['firstname']
    Sub_account['SA_id'] = str(uuid.uuid4())                       #create a new id for this sub account
    PT_database.insert({'_id':PT_account['_id'],'PT_account':PT_account})
    return



def Valid_PointTracker_Account(_id):
    db_obj = PT_database.find_one({'_id':_id})
    if db_obj is None:
        return False                                     ## No such PT_account
    else:
        return True                                     ## An account exists















def Add_Reward_Program(PT_obj):

    RP_account = {
        "RP_id":"",
        "RP_callback_tag":"",
        "RP_datestamp":"",
        "RP_password":"",
        "RP_expiration_date":"",
        "RP_account_name":"",
        "RP_days_remaining":"",
        "RP_balance_delta":"",
        "RP_username":"",
        "RP_balance":"0",
        "RP_timestamp":"",
        "RP_name":"",
        "RP_last_activity_date":"",
        "RP_inactive_time":"",
        "RP_partner": "",
        "RP_error":False,
        #no program accounts at this time
    }


#    RP_account['RP_callback_tag'] = PT_obj['RP_callback_tag']                         #call back info
    RP_account['SA_id'] = PT_obj['SA_id']                                              #store the Sub Account id
    RP_account['RP_id'] = str(uuid.uuid4())                                         #create a new id for this program account
    RP_account['RP_name']= PT_obj['RP_name']                                    ## set the new name
    RP_account['RP_username']= PT_obj['RP_username']                                 ## set the new name
    RP_account['RP_password']= encrypt_password(PT_obj['RP_password'])                 ## set the new name
#    RP_account['RP_password']= PT_obj['RP_password']                                 ## set the new name

    RP_account = Process_Reward_Program(RP_account)                                     #scrape and check for error before inserting in PT

    if not RP_account['RP_error']:                                                  #no error, so add it to the database
        _id = PT_obj['_id']
        PT_account = Get_PointTracker_Account(_id)                                  #get our PT account out of the database
        PT_sub_accounts = PT_account['PT_sub_accounts']                         #get our PT sub account list
        #now find our sub account
        for SA_account in PT_sub_accounts:
            if SA_account['SA_id'] == PT_obj['SA_id']:
                break                                                           # we now have our sub account

        SA_program_accounts = SA_account['SA_program_accounts']                #get the list of Reward Programs
        SA_program_accounts.append(RP_account)                                  ## append to list
        Update_PointTracker_Database(PT_account)                                # update the database

    return RP_account









def Delete_Reward_Program(PT_obj):

    PT_account = Get_PointTracker_Account(PT_obj['_id'])              #get our PT account out of the database
    PT_sub_accounts = PT_account['PT_sub_accounts']                   #get our PT sub account list

    #now find our sub account
    for SA_account in PT_sub_accounts:
        if SA_account['SA_id'] == PT_obj['SA_id']:
            break                                                           # we now have our sub account

    SA_program_accounts = SA_account['SA_program_accounts']

    for RP_account in list(SA_program_accounts):                     #iterate over a copy of the list so we can remove the RP accounts with out messing with the original
        if RP_account['RP_id'] == PT_obj['RP_id']:
            SA_program_accounts.remove(RP_account)                         # remove it from list
            break

    Update_PointTracker_Database(PT_account)                 # update the database

    return






def Refresh_Reward_Program(PT_obj):

    PT_account = Get_PointTracker_Account(PT_obj['_id'])                #Get the PT account
    RP_account = Get_Reward_Program_Account(PT_account,PT_obj)         # Get the Reward Program account
    refreshed_RP_account = Process_Reward_Program(RP_account)                  # Refresh it by calling the appropriate scraper
    if not refreshed_RP_account['RP_error']:                  #no error update the database otherwise display error in client
        Set_Reward_Program_Account(PT_account, refreshed_RP_account, PT_obj)
        Update_PointTracker_Database(PT_account)
    return refreshed_RP_account




def Edit_Reward_Program(PT_obj):
#    AES_Key = '0123456789abcdef'

    PT_account = Get_PointTracker_Account(PT_obj['_id'])                #Get the PT account
    RP_account = Get_Reward_Program_Account(PT_account,PT_obj)         # Get the Reward Program account that we want to modify
    RP_account['RP_username'] = PT_obj['RP_username']                  # Update with edited information from user
    RP_account['RP_password'] = mtk.encrypt(Globalvars.AES_Key,PT_obj['RP_password'])  #encrypt new password
#    RP_account['RP_password'] = PT_obj['RP_password']  #encrypt new password
    RP_account['RP_name'] = PT_obj['RP_name']
    RP_account['RP_balance'] = 0                                        #zero out balance because user could enter in a whole different account. We want don't want the account balance delta based off old account
    RP_account['RP_balance_delta'] = 0
    edited_RP_account = Process_Reward_Program(RP_account)                  # Refresh it by calling the appropriate scraper
    if not edited_RP_account['RP_error']:                                 #no error update the database otherwise display error in client
        Set_Reward_Program_Account(PT_account, edited_RP_account, PT_obj)
        Update_PointTracker_Database( PT_account)
    return edited_RP_account








def Set_Reward_Program_Account (PT_account, new_RP_account, PT_obj):

    PT_sub_accounts = PT_account['PT_sub_accounts']
    for SA_account in PT_sub_accounts:
        if SA_account['SA_id'] == PT_obj['SA_id']:                      #We now have our SA_account
            break

    SA_program_accounts = SA_account['SA_program_accounts']
    for RP_account in SA_program_accounts:
        if RP_account['RP_id'] == PT_obj['RP_id']:                      #We now have our RP_account
            break
    for key in new_RP_account:                                          #copy the new updated reward program into the RP_account in PT account
        RP_account[key] = new_RP_account[key]
    return





def Get_Reward_Program_Account (PT_account, PT_obj):

    PT_sub_accounts = PT_account['PT_sub_accounts']
    for SA_account in PT_sub_accounts:
        if SA_account['SA_id'] == PT_obj['SA_id']:                      #We now have our SA_account
            break

    SA_program_accounts = SA_account['SA_program_accounts']
    for RP_account in SA_program_accounts:
        if RP_account['RP_id'] == PT_obj['RP_id']:                      #We now have our RP_account
            break
    RP_account['RP_callback_tag'] = PT_obj['RP_callback_tag']           # embed tag for callback functions
#    RP_account['RP_password'] = ''                                      #remove password for client for security
    return RP_account





## We store all Reward Program Passwords in the database encrypted.  However, when the client pulls the PT_account we need to decrypt
## all of the Reward Program Passwords so he can edit them if he desires.

def Decrypt_PT_account_Reward_Program_Passwords(PT_account):
#    AES_Key = '0123456789abcdef'
    PT_sub_accounts = PT_account['PT_sub_accounts']

    for SA_account in PT_sub_accounts:                               #iterate over a sub accounts
        SA_program_accounts = SA_account['SA_program_accounts']        #get the Reward program accounts for this subaccount
        for RP_account in SA_program_accounts:                               #decrypt the passwords for the client side.  Our datebase is still encrypted
            RP_account['RP_password'] = mtk.decrypt(Globalvars.AES_Key,RP_account['RP_password'])
    return PT_account


## We store all Reward Program Passwords in the database encrypted.  However, when the client pulls the PT_account we need to remove
## all of the Reward Program Passwords so client can't see them for security. If client wants to edit a RP account they just have to enter new password

def Remove_PT_account_Reward_Program_Passwords(PT_account):
#    AES_Key = '0123456789abcdef'
    PT_sub_accounts = PT_account['PT_sub_accounts']

    for SA_account in PT_sub_accounts:                               #iterate over a sub accounts
        SA_program_accounts = SA_account['SA_program_accounts']        #get the Reward program accounts for this subaccount
        for RP_account in SA_program_accounts:                               #Remove the passwords for the client side.  Our datebase is still encrypted
            RP_account['RP_password'] = ""
    return PT_account



def Add_Sub_Account(PT_obj):

    new_sub_account = {
        "SA_id":"",
        "SA_name":"",
        "SA_program_accounts":[]                                        #no program accounts at this time
    }

    _id = PT_obj['_id']
    PT_account = Get_PointTracker_Account(_id)                          #get our PT account out of the database
    PT_sub_accounts = PT_account['PT_sub_accounts']                     #get our PT sub account list

    new_sub_account['SA_name']= PT_obj['SA_name']                                 ## set the new name
    new_sub_account['SA_id'] = str(uuid.uuid4())                       #create a new id for this sub account

    PT_sub_accounts.insert(0,new_sub_account)               ## insert at beginning of list

    PT_account['PT_sub_accounts'] = PT_sub_accounts         # the list has been updated so put it back

    Update_PointTracker_Database(PT_account)                 # update the database

    return





def Delete_Sub_Account(PT_obj):

    _id = PT_obj['_id']                                                    #The id of what PT_account we are working on

    SA_id = PT_obj['SA_id']                               # sub account to be removed
#    SA_id = PT_obj['Current_SA_id']                               # sub account to be removed
    PT_account = Get_PointTracker_Account(_id)                          # Get the PT account
    PT_sub_accounts = PT_account['PT_sub_accounts']                        # Get a list of all the sub accounts

    for sub_account in list(PT_sub_accounts):                               #iterate over a copy of the list
            if sub_account['SA_id'] == SA_id:
                PT_sub_accounts.remove(sub_account)                         # remove it from list
                break

#    print ('Sub Account {} has been deleted.'.format(PT_obj['SA_id']))

    Update_PointTracker_Database(PT_account)                                 #update it in database
    return





def Process_Reward_Program(RP_account):
    if RP_account['RP_name'] == 'American Airlines':
        html = airline_scrapers.american.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.american.scrape_webpage(html)

    elif RP_account['RP_name'] == 'United Airlines':
        html = airline_scrapers.united.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.united.scrape_webpage(html)

    elif RP_account['RP_name'] == 'Delta Airlines':
        html = airline_scrapers.delta.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.delta.scrape_webpage(html)

    elif RP_account['RP_name'] == 'US Airways':
        html = airline_scrapers.usairways.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.usairways.scrape_webpage(html)

    elif RP_account['RP_name'] == 'British Airways':
        html = airline_scrapers.britishairways.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.britishairways.scrape_webpage(html)

    elif RP_account['RP_name'] == 'EVA Air':
        html = airline_scrapers.evaair.get_program_account_info(RP_account)                                 #login and grab necessary web pages to scrape
        RP_updated_account = airline_scrapers.evaair.scrape_webpage(html)

    RP_updated_account['RP_callback_tag'] = RP_account['RP_callback_tag']                       #we still need this info for the call back
    RP_updated_account['RP_name'] = RP_account['RP_name']
    RP_updated_account['RP_id'] = RP_account['RP_id']
    RP_updated_account['SA_id'] = RP_account['SA_id']

    if not RP_updated_account['RP_error']:                              # No Error so finish the last steps
        RP_updated_account['RP_username'] = RP_account['RP_username']         #put username and password back in new dict
        RP_updated_account['RP_password'] = RP_account['RP_password']
        RP_updated_account['RP_balance_delta'] = int(RP_updated_account['RP_balance']) - int(RP_account['RP_balance'])

    return RP_updated_account





def encrypt_password(password):
#    AES_Key = '0123456789abcdef'

    encrypted_password = mtk.encrypt(Globalvars.AES_Key,password)
    return encrypted_password





## This is just a test function to return the Reward Program without out updating the database
##

def Return_Reward_Program(PT_obj):

    PT_account = Get_PointTracker_Account(PT_obj['_id'])                #Get the PT account
    RP_account = Get_Reward_Program_Account(PT_account,PT_obj)         # Get the Reward Program account
    RP_account['RP_error'] = False                                    #Clear error status
    return RP_account




## This is just a utility to encrypt all the passwords for the PT_account and update it in the datebase
##It is not normally used in the program
def Encrypt_PT_account_Reward_Program_Passwords(PT_account):
#    AES_Key = '0123456789abcdef'
    PT_sub_accounts = PT_account['PT_sub_accounts']

    for SA_account in PT_sub_accounts:                               #iterate over a sub accounts
        SA_program_accounts = SA_account['SA_program_accounts']        #get the Reward program accounts for this subaccount
        for RP_account in SA_program_accounts:                               #decrypt the passwords for the client side.  Our datebase is still encrypted
            RP_account['RP_password'] = mtk.encrypt(Globalvars.AES_Key,RP_account['RP_password'])


#    Update_PointTracker_Database(PT_account)                        #write it back out to the database

    return PT_account






def Manual_MongoDB_Modify(old_id, new_id):

    db_obj = PT_database.find_one({'_id':old_id})

#    db_obj._id = ObjectId(new_id)
    db_obj['_id']= new_id

    PT_database.insert(db_obj)

    PT_database.remove(old_id)
    return



def hack_mongo(request):
    _id = '434a54829180d1c606ecfa8f86e8745d8eb2e0a534e9d8f990c85e973b32f750'
#    _id = 'a7f8400519df31402eed6b052217946f04e079d8cad25a59994402f511eadf9f'            #old id
    PT_account = Get_PointTracker_Account(_id)
    username = request['username']
    password = request['password']
    hash = hashlib.sha256()
    string = request['username']  + Globalvars.Saltstring + request['password']
    encode_string = string.encode('utf-8')

    hash.update(encode_string)
    _id = hash.hexdigest()

#    _id = 'a7f8400519df31402eed6b052217946f04e079d8cad25a59994402f511eadf9f'            #new _id
    PT_account['_id'] = _id
    Encrypt_PT_account_Reward_Program_Passwords(PT_account)                                 #encrypt all Reward Program Password before sending to database
    PT_database.insert({'_id':PT_account['_id'],'PT_account':PT_account})               #insert new one
    return

