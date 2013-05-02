import requests                   #Requests Http Library
from bs4 import BeautifulSoup
import mtk
from datetime import datetime
from datetime import timedelta

from ssl import PROTOCOL_TLSv1
import ssladapter
#from ptserver import AES_Key
#from constants import AES_Key
import Globalvars





def get_program_account_info(RP_account):
    url0 = 'https://www.britishairways.com/travel/home/public/en_us'
    url1 = 'https://www.britishairways.com/travel/loginr/public/en_us'

    form_data = {
        'Directional_Login':'',
        'eId':'109001',
        'password':'password',
        'membershipNumber':'username',
        }


#    AES_Key = '0123456789abcdef'
    form_data['membershipNumber'] = RP_account['RP_username']
    form_data['password'] = mtk.decrypt(Globalvars.AES_Key,RP_account['RP_password'])
#    form_data['password'] = RP_account['RP_password']

    s = requests.Session()
    s.mount('https://', ssladapter.SSLAdapter(ssl_version = PROTOCOL_TLSv1))
    r1 = s.get(url0)                                      #BA Home Page. Grab any initial cookies and headers
    #    mtk.write_file(r1.text,'ba1.txt')

    r2 = s.post(url1, data = form_data)                    #Login in to BA
    #    mtk.write_file(r2.text,'ba1.txt')

    return r2.text






def scrape_webpage(html):
    RP_account = dict()

    soup = BeautifulSoup(html,"lxml")
#    mtk.write_file(str(s),'basoup.txt')

    RP_account_name = str(soup.find('h1', id='welcomeLabel'))                            #name

    RP_account['RP_error'] = False                                              #clear any error so we can test again
    if RP_account_name == 'None':                                                       #Bad username, password, or general error from server.
        RP_account['RP_error'] = True
        return RP_account

    RP_account_num = str(soup.find('td', class_='detailsStyle'))                     #account #
    RP_balance = str(soup.find('h2', class_ = 'lineSpace'))                          #balance
    RP_last_activity_date = str(soup.find('td', id='latestTransRow0Date'))          #Last Activity date

    RP_account_name = RP_account_name.replace('<h1 class="welcome1" id="welcomeLabel">Welcome to your Executive Club, ','')              #remove first part of tag
    RP_account_name = RP_account_name.replace('</h1>','')                                                                               #remove second part of tag to leave only name
    RP_account['RP_account_name']= RP_account_name                                                                                      # name is only left

    RP_account_num = RP_account_num.replace('<td class="detailsStyle"><strong>','')                        #remove first part of tag
    RP_account_num = RP_account_num.replace('</strong></td>','')                                            #remove second part of tag to leave only name
    RP_account['RP_account_num']= RP_account_num                                                            #account # is only left

    RP_balance = RP_balance.replace('<h2 class="lineSpace aviosPoints">','')                        #remove first part of tag
    RP_balance = RP_balance.replace('</h2>','')                                                     #remove second part of tag to leave only name
    RP_balance = RP_balance.replace(',','')
    RP_account['RP_balance']= int(RP_balance)                                                       #balance is only left

    now_date_obj = datetime.now()

    if RP_last_activity_date == 'None':                                                            #no transactions or activity
        RP_account['RP_last_activity_date']= 'N/A'
        RP_account['RP_days_remaining']= 'N/A'
        RP_account['RP_expiration_date']= 'N/A'
    else:
        RP_last_activity_date = RP_last_activity_date.split()                                   #split out the string.  date is 3rd item
        last_activity_date_obj = datetime.strptime(RP_last_activity_date[2],"%d-%b-%y")          #last activity date object
        RP_account['RP_last_activity_date']= last_activity_date_obj.strftime('%m/%d/%Y')

        exp_date = last_activity_date_obj + timedelta(days=730)                                  #add 2 years from last activity to get expiration date
        RP_account['RP_expiration_date']= exp_date.strftime('%m/%d/%Y')

        days_left = exp_date - now_date_obj                                              #still in date object format
        RP_account['RP_days_remaining']= days_left.days                               #how many days left to expiration


    RP_account['RP_datestamp'] = str(now_date_obj.month) + '/' + str(now_date_obj.day) + '/' + str(now_date_obj.year)
    RP_account['RP_timestamp'] = str(now_date_obj.hour) + ':' + str(now_date_obj.minute) + ':' + str(now_date_obj.second)

    RP_account['RP_name']='British Airways'                                          #set what program type it is
    RP_account['RP_inactive_time'] = '24 Months'                                       #BA program miles expiration rule (miles expire after 24 months of non use)
    RP_account['RP_partner']= 'One World'

    return RP_account






