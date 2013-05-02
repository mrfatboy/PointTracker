import requests                   #Requests Http Library
from bs4 import BeautifulSoup
import mtk
import time
from datetime import datetime
#from ptserver import AES_Key
#from constants import AES_Key
import Globalvars

def get_program_account_info(RP_account):
    url_loginSubmit = 'https://www.aa.com/login/loginSubmit.do'
    url_myAccountAccess = 'https://www.aa.com/myAccount/myAccountAccess.do'

    form_data = dict()

#    AES_key = '0123456789abcdef'

    form_data['loginId'] = RP_account['RP_username']
    form_data['password'] = mtk.decrypt(Globalvars.AES_Key,RP_account['RP_password'])
#    form_data['password'] = RP_account['RP_password']

    s = requests.session()

    r_obj1 = s.post(url_loginSubmit, data= form_data)           #login

    r_obj2 = s.get(url_myAccountAccess)                         #Get Account Info page

    return r_obj2.text                                        #return webpage with account info to scrape








def scrape_webpage(html):
    RP_account = dict()

    soup0 = BeautifulSoup(html,"lxml")
#    mtk.write_file(str(s),'americansoup.txt')
    RP_account_name = str(soup0.find('li', class_='aa-personalInfo-name'))                  #Name

    RP_account['RP_error'] = False                                                  #clear any error so we can test again
    if RP_account_name == 'None':                                                           #Bad username, password, or general error from server.
        RP_account['RP_error'] = True
        return RP_account

    RP_account_num_list = soup0.find_all('strong')                                  #Account is first in list
    RP_balance = str(soup0.find('td', class_='pbnTableTotal hright'))               #balance
    RP_expiration_date = str(soup0.find('div', id='summaryData'))                   #Expiration
    RP_last_activity_date = str(soup0.find('div', class_='pbnMember floatLeft'))    #Last Activity

    RP_account_name = RP_account_name.replace('\n','')                                                    #clean up by removing new lines
    RP_account_name = RP_account_name.replace('<li class="aa-personalInfo-name"><span>','')
    RP_account_name = RP_account_name.replace('</span></li>','')
    RP_account_name = RP_account_name.lstrip(' ')                                                     #get rid of any leading spaces, it can be different in AA scrapes
    RP_account_name = RP_account_name.lower()                                                         #make all lowercase
    RP_account_name = RP_account_name.title()                                                       #name and capitalize first, middle, last
    RP_account['RP_account_name'] = RP_account_name

    RP_account_num = str(RP_account_num_list[0])                              #account num is first item in list
    RP_account_num = RP_account_num.replace('<strong>','')                                     #remove first tag
    RP_account_num = RP_account_num.replace('</strong>','')                                      #remove end tag
    RP_account['RP_account_num'] = RP_account_num                                 #account num

    RP_balance = RP_balance.replace('<td class="pbnTableTotal hright">','')                  #remove first part of tag
    RP_balance = RP_balance.replace('</td>','')                                              #remove second part of tag to leave only name
    RP_balance = RP_balance.replace(',','')                                                  #just want number without commas
    RP_account['RP_balance'] = int(RP_balance)                                     #balance

    now_date_obj = datetime.now()
    RP_expiration_date = RP_expiration_date.replace('\n','')                                         #remove newlines
    RP_expiration_date = RP_expiration_date.replace('\t','')                                         #remove tabs
    s_index = RP_expiration_date.find('Expiration Deferred Through')
    if s_index == -1:                                                                               # There is no expiration data
        RP_account['RP_expiration_date']= 'N/A'
        RP_account['RP_days_remaining'] = 'N/A'
        RP_account['RP_last_activity_date'] = 'N/A'                                                     #last Activity Date
    else:
        e_index = RP_expiration_date.find('/td',s_index)                                                   #get index of ending tag. date is before
        RP_expiration_date = RP_expiration_date[s_index+len('Expiration Deferred Through')+6:e_index-1]
        RP_expiration_date = RP_expiration_date.replace('00:00:00 CDT ','')                                                   #date is now in 'Nov 20 2012' format
        date_obj = time.strptime(RP_expiration_date,"%b %d %Y")
        RP_expiration_date = time.strftime('%m/%d/%Y',date_obj)                               #Expiration is now in 'm/d/Y' format
        RP_account['RP_expiration_date'] =  RP_expiration_date

        last_activity_date_obj = datetime.strptime(RP_expiration_date,'%m/%d/%Y')
        days_left = last_activity_date_obj - now_date_obj
        RP_account['RP_days_remaining'] =  days_left.days


        RP_last_activity_date = RP_last_activity_date.replace('\n','')                              #remove tabs and newlines
        RP_last_activity_date = RP_last_activity_date.replace('\t','')
        s_index = RP_last_activity_date.find('Last Activity Date:')                                 #get index of tag
        e_index = RP_last_activity_date.find('</strong',s_index)                                    #get the end of tag index, date is before
        RP_last_activity_date = RP_last_activity_date[s_index:e_index]                              #get a tag that looks something like this "Last Activity Date:</label><strong>Sunday, March 24, 2013"

        s_index = RP_last_activity_date.find(',')                                                   #find the index after day of week (ex. Sunday)
        RP_last_activity_date = RP_last_activity_date[s_index+2:]                                    #Get March 24, 2013

        date_obj = time.strptime(RP_last_activity_date,"%B %d, %Y")                         #note how the date format is with the comma
        RP_last_activity_date = time.strftime('%m/%d/%Y',date_obj)                           #last Activity Date
        RP_account['RP_last_activity_date'] = RP_last_activity_date


    RP_account['RP_datestamp'] = str(now_date_obj.month) + '/' + str(now_date_obj.day) + '/' + str(now_date_obj.year)
    RP_account['RP_timestamp'] = str(now_date_obj.hour) + ':' + str(now_date_obj.minute) + ':' + str(now_date_obj.second)

    RP_account['RP_name']='American Airlines'                               #set what program type it is
    RP_account['RP_inactive_time'] = '18 Months'
    RP_account['RP_partner']= 'One World'

    return RP_account








