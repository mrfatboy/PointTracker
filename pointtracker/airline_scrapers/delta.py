import requests                   #Requests Http Library
from bs4 import BeautifulSoup
import re
from ssl import PROTOCOL_TLSv1
#import mtk
import time
import ssladapter

from datetime import datetime



def get_program_account_info(RP_account):

    url0 = 'https://www.delta.com'
    url1 = 'https://www.delta.com/custlogin/login.action'
    url2 = 'https://www.delta.com/acctactvty/manageacctactvty.action'


    form_data = {
        'loginpath':'//www1.delta.com',
        'usernameType':'skymiles',
        'passwordType':'PW',
        'homePg':'',
        'refreshURL':'http://www.delta.com/',
        'username':'',
        'password':'',
        'rememberMe':'true',
        'BAUParams':'',
        'usernm':'',
        'pwd':'',
        'Submit':'>',
        'rememberme':'on'
    }


#    key = '0123456789abcdef'
    form_data['username'] = RP_account['RP_username']
    form_data['usernm'] = RP_account['RP_username']
#    form_data['password'] = mtk.decrypt(key,RP_account['RP_password'])
#    form_data['pwd'] = mtk.decrypt(key,RP_account['RP_password'])
    form_data['password'] = RP_account['RP_password']
    form_data['pwd'] = RP_account['RP_password']

    s = requests.Session()
    s.mount('https://', ssladapter.SSLAdapter(ssl_version = PROTOCOL_TLSv1))
    r1 = s.get(url0)                                      #Delta Home Page
#    mtk.display_webpage(r1.text)

    r2 = s.post(url1, data = form_data)                    #Login in to Delta, #this page has Name, account, miles
#    mtk.write_file(r2.text,'delta2.txt')

    r3 = s.get(url2)                                       #this page has last activity
#    mtk.write_file(r3.text,'delta3.txt')

    list = [r2.text,r3.text]
    return list                                                         #return a list since we have data on multiple pages





def scrape_webpage(html_list):
    RP_account = dict()

    soup0 = BeautifulSoup(html_list[0], "lxml")                         #delta 2 page.  Name does not come in because of JS, but we can get other stuff
#    mtk.write_file(str(s),'delta2soup.txt')

    RP_account_num = str(soup0.find(text = re.compile('smNbr')))                    #get the string with account # in it

    s_index = RP_account_num.find('smNbr = "')
    RP_account_num = RP_account_num[s_index+len('smNbr = "'):]
    e_index= RP_account_num.find('"')
    RP_account_num = RP_account_num[:e_index]

    RP_account['RP_error'] = False                                      #clear any error so we can test again
    if RP_account_num == 'null':                                       #Bad username, password, or general error from server.
        RP_account['RP_error'] = True
        return RP_account

    RP_account['RP_account_num']= RP_account_num                        #account # is only left
    RP_account['RP_account_name']= RP_account_num                                # we can only use account # at this time

    soup1 = BeautifulSoup(html_list[1])                         #page with balance & last activity, last activity n um

    RP_balance = str(soup1.find('input', id='totalAvailableMiles'))                            #balance
    RP_last_activity_num = str(soup1.find('div', class_='narrowResultCount'))                  #any Activiy?
    RP_last_activity = str(soup1.find('span', class_='bottomText postedDate'))                 # activity date

    RP_balance = RP_balance.replace('<input id="totalAvailableMiles" name="totalAvailableMiles" type="hidden" value="','')                        #remove first part of tag
    RP_balance = RP_balance.replace('"/>','')                                                                                                    #remove second part of tag to leave only name
    RP_balance = RP_balance.replace(',','')
    RP_account['RP_balance'] = int(RP_balance)                                                                         #Balance

    RP_last_activity_num = RP_last_activity_num.replace('<div class="narrowResultCount" id="resultsCount">','')        #remove first part of tag
    RP_last_activity_num  = RP_last_activity_num .replace('</div>','')                                                 #remove second part of tag to leave only name
    RP_last_activity_num  = RP_last_activity_num .replace('\n','')                                                     #get rid of newlines
    RP_last_activity_num  = RP_last_activity_num .replace('\t','')                                                     #get rid of tabs
    activity_num = int(RP_last_activity_num)                                                                           #how many last activities are reported if any

    if activity_num > 0:
        RP_last_activity = RP_last_activity.replace('<span class="bottomText postedDate">','')                           #remove first part of tag
        RP_last_activity = RP_last_activity.replace('</span>','')                                                        #remove second part of tag to leave only name
        RP_last_activity = RP_last_activity.replace('\n','')                                                             #get rid of newlines
        RP_last_activity = RP_last_activity.replace('\t','')                                                             #get rid of tabs
        RP_last_activity = RP_last_activity.replace('\r','')                                                             #get rid of tabs
        date_obj = time.strptime(RP_last_activity,"%b %d %Y")
        RP_account['RP_last_activity_date'] = time.strftime('%m/%d/%Y',date_obj)                                          #last activity date (top of list, not be last)
    else:
        RP_account['RP_last_activity_date'] = 'N/A'

    now_date_obj = datetime.now()

    RP_account['RP_datestamp'] = str(now_date_obj.month) + '/' + str(now_date_obj.day) + '/' + str(now_date_obj.year)
    RP_account['RP_timestamp'] = str(now_date_obj.hour) + ':' + str(now_date_obj.minute) + ':' + str(now_date_obj.second)

    RP_account['RP_name']='Delta Airlines'                                          #set what program type it is
    RP_account['RP_expiration_date']= 'Never Expire'
    RP_account['RP_inactive_time'] = 'Never Expire'
    RP_account['RP_days_remaining'] = 'Never Expire'
    RP_account['RP_partner']= 'Sky Team'

    return RP_account


