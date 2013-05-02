import requests                   #Requests Http Library
from bs4 import BeautifulSoup
from datetime import datetime
import mtk
from pytz import timezone
#from ptserver import AES_Key
#from constants import AES_Key
import Globalvars



def get_program_account_info(RP_account):
    url0 = 'http://www.evaair.com/en-us/index.html'
    url2 = 'https://eservice.evaair.com/EVAWEB/EVA/FFP/frm_login.aspx?p_url=http://www.evaair.com/en-us/index.html'                 #embeded login modal with _viewstate and _eventvalidations
    url3 = 'https://eservice.evaair.com/EVAWEB/EVA/FFP/frm_login.aspx?p_url=http%3a%2f%2fwww.evaair.com%2fen-us%2findex.html'       #post to this
    url6 = 'https://eservice.evaair.com/evaweb/eva/ffp/mileage-summary.aspx?lang=en-us'
    url7 = 'https://eservice.evaair.com/Evaweb/EVA/FFP/personal-data.aspx'                                                          #has membership number, name

    form_data = {
        '__EVENTARGUMENT':'',
        '__EVENTTARGET':	'wuc_login$btn_Login_Server',
        '__EVENTVALIDATION':'',                                             #fill this in below
        '__VIEWSTATE':'',                                                   #fill this in below
        '__VIEWSTATEENCRYPTED':'',
        'wuc_login$Chk_RmbrMbrID':'on',
        'wuc_login$hid_DateTime':'',                                        #fill this in below
        'wuc_login$hid_url':'http://www.evaair.com/en-global/index.html',
        'wuc_login$txt_Member':'',                                              #fill this in below
        'wuc_login$txt_Password':''                                             #fill this in below
    }

#    AES_Key = '0123456789abcdef'

    form_data['wuc_login$txt_Member'] = RP_account['RP_username']
    form_data['wuc_login$txt_Password'] = mtk.decrypt(Globalvars.AES_Key,RP_account['RP_password'])
#    form_data['wuc_login$txt_Password'] = RP_account['RP_password']

    s = requests.session()

    r_obj0 = s.get(url0)                                        #Eva air.com, grab any cookies and headers in session

    r_obj2 = s.get(url2)                                        #Load in login form.  it has embeded info we need. _VIEWSTATE & _EVENTVALIDATION that we need to scrap before we submit
    soup = BeautifulSoup(r_obj2.text, "lxml")

    __VIEWSTATE = str(soup.find('input', id='__VIEWSTATE'))
    s_index = __VIEWSTATE.find('value="')
    __VIEWSTATE = __VIEWSTATE[s_index+len('value="'):-3]                 #take off 'value="' and ending html tag

    __EVENTVALIDATION = str(soup.find('input', id='__EVENTVALIDATION'))
    s_index = __EVENTVALIDATION.find('value="')                           #take off 'value="' and ending html tag
    __EVENTVALIDATION = __EVENTVALIDATION[s_index+len('value="'):-3]


    form_data['__VIEWSTATE'] = __VIEWSTATE                               #setup form data
    form_data['__EVENTVALIDATION'] = __EVENTVALIDATION

    pacific = timezone('US/Pacific')                        #get local timezone
    loc_dt = pacific.localize(datetime.now())               #local time
    Taipei = timezone('Asia/Taipei')                        #convert to Taipai time
    Taipei_dt = loc_dt.astimezone(Taipei)                   #get Taipei time

    form_data['wuc_login$hid_DateTime'] = Taipei_dt.strftime('%Y/%m/%d %H:%M:%S')                            #setup form data for Taipei Time

    r_obj3 = s.post(url3, data = form_data)                       #First page after login - it doesn't have any scrapable info on it, doing it for cookies

    r_obj6 = s.get(url6)                                        #page where all the milage data is

    r_obj7 = s.get(url7)                                        #name and account number

    list = [ r_obj6.text, r_obj7.text]
    return list







def scrape_webpage(html_list):
    RP_account = dict()

    soup0 = BeautifulSoup(html_list[0],"lxml")                          # mileage data info
    soup1 = BeautifulSoup(html_list[1],"lxml")                          #  page with name and account number
#    mtk.write_file(str(soup0),"evasoup1.txt")
#    mtk.write_file(str(soup1),"evasoup2.txt")

    RP_account_name = str(soup1.find('span', id="ContentPlaceHolder1_lbl_FName"))                            #First and middle name

    RP_account['RP_error'] = False                                      #clear any error so we can test again
    if RP_account_name == 'None':                                                      #Bad username, password, or general error from server.
        RP_account['RP_error'] = True
        return RP_account

    RP_lastname = str(soup1.find('span', id="ContentPlaceHolder1_lbl_LName"))                              #Last name
    RP_account_num = str(soup1.find('span', id="ContentPlaceHolder1_lbl_Member"))                           #Account num

    expiration_list = (soup0.find_all('strong', class_='green_text'))                                       #expiration info
    RP_expiration_date = str(expiration_list[3])                                                            #expiration date
    RP_balance = str(expiration_list[6])                                                                    #account balance

    RP_account_name = RP_account_name.replace('<span id="ContentPlaceHolder1_lbl_FName" style="color: #333; font-weight:normal;">','')                        #remove first part of tag
    RP_account_name = RP_account_name.replace('</span>','')                                                                                               #remove second part of tag to leave only name

    RP_lastname = RP_lastname.replace('<span id="ContentPlaceHolder1_lbl_LName" style="color: #333; font-weight:normal;">','')                        #remove first part of tag
    RP_lastname = RP_lastname.replace('</span>','')                                                                                                     #remove last part of tag

    RP_account_name = RP_account_name + ' ' + RP_lastname                                                                                      #add first and last name together
    RP_account_name= RP_account_name.lower()
    RP_account_name = RP_account_name.title()
    RP_account['RP_account_name']= RP_account_name

    RP_account_num = RP_account_num.replace('<span id="ContentPlaceHolder1_lbl_Member" style="color: #333; font-weight:normal;">','')                        #remove first part of tag
    RP_account_num = RP_account_num.replace('</span>','')                                                                                            #remove first part of tag
    RP_account['RP_account_num']= RP_account_num                                                                                #account # is only left

    RP_balance = RP_balance.replace('<strong class="green_text">','')                                                                   #remove first part of tag
    RP_balance = RP_balance.replace('</strong>','')                                                                                            #remove last part of tag
    RP_account['RP_balance']= int(RP_balance)                                                                                 #balance is only left

    RP_expiration_date = RP_expiration_date.replace('<strong class="green_text">','')                        #remove first part of tag  for expiration date
    RP_expiration_date = RP_expiration_date.replace('</strong>','')                                          #remove last part of tag for expiration date
                                                                            # The expiration date now looks like '2014/12' for example. we need to change it to 12-31-14'
    s_index = RP_expiration_date.find('/')
    month = RP_expiration_date[s_index+1:]                                                     #get month
    year = RP_expiration_date[:4]                                                              #year

    RP_account['RP_expiration_date'] = month+'/'+'31'+ '/' + year

    now_date_obj = datetime.now()
    last_activity_date_obj = datetime.strptime(RP_account['RP_expiration_date'],'%m/%d/%Y')
    days_left = last_activity_date_obj - now_date_obj

    RP_account['RP_days_remaining'] =  days_left.days

    RP_account['RP_datestamp'] = str(now_date_obj.month) + '/' + str(now_date_obj.day) + '/' + str(now_date_obj.year)
    RP_account['RP_timestamp'] = str(now_date_obj.hour) + ':' + str(now_date_obj.minute) + ':' + str(now_date_obj.second)

    RP_account['RP_last_activity_date']= 'N/A'                                                            #united does not provide easy Last Activity date
    RP_account['RP_inactive_time'] = '36 Months'
    RP_account['RP_partner']= 'Star Alliance'
    RP_account['RP_name']='EVA Air'                                          #set what program type it is

    return RP_account





