import requests                   #Requests Http Library
from bs4 import BeautifulSoup
import time
from datetime import datetime
import mtk
#from ptserver import AES_Key
#from constants import AES_Key
import Globalvars




def get_program_account_info(RP_account):
    url_loginSubmit = 'https://www.united.com/web/en-US/apps/account/signin.aspx'
    url3 = 'https://www.united.com/web/en-US/apps/mileageplus/statement/statement.aspx?MP=1&SD=12/31/2011'


    form_data = {
        'hdnServer':'.111'
        ,'hdnSID':'F0BEF75DD058494BB7C9A7916FF514D0'
        ,'hdnLangCode':'en-US'
        ,'hdnPOS':'US'
        ,'hdnClient':'76.212.215.196'
        ,'hdnInactive':'false'
        ,'hdnAccountNumber':''
        ,'hdnAccountNumberE':''
        ,'hdnAccountStatus':''
        ,'__EVENTTARGET':''
        ,'__EVENTARGUMENT':''
        ,'hdnTiming':'0.1874592 seconds'
        ,'__VIEWSTATE':'/wEPDwUKMTQzNjgzNDA3NA9kFgJmD2QWAgIDDxYCHghvbnVubG9hZAUSUHVyY2hhc2VBYmFuZG9uKCk7FgICAQ8WAh4GYWN0aW9uBTlodHRwczovL3d3dy51bml0ZWQuY29tL3dlYi9lbi1VUy9hcHBzL2FjY291bnQvc2lnbmluLmFzcHgWBAIFD2QWAgIJD2QWBAIJD2QWAgIBDw8WAh4LTmF2aWdhdGVVcmwFOWh0dHBzOi8vd3d3LnVuaXRlZC5jb20vd2ViL2VuLVVTL2FwcHMvYWNjb3VudC9lbnJvbGwuYXNweGRkAg0PZBYCAgEPZBYIAgEPZBYEAgIPDxYEHgxFcnJvck1lc3NhZ2UFRiEgUGxlYXNlIGVudGVyIGEgTWlsZWFnZVBsdXMgTnVtYmVyIG9yIFVzZXJuYW1lLjwhLS1FcnJDb2RlOlYxLS0+PGJyLz4eD1ZhbGlkYXRpb25Hcm91cAUKU2lnbkluRm9ybWRkAgQPDxYEHwMFTSEgUGxlYXNlIGVudGVyIGEgdmFsaWQgTWlsZWFnZVBsdXMgTnVtYmVyIG9yIFVzZXJuYW1lLjwhLS1FcnJDb2RlOlYxNS0tPjxici8+HwQFClNpZ25JbkZvcm1kZAIDD2QWAmYPDxYCHwIFX34vZW4tVVMvYXBwcy9hY2NvdW50L3NldHRpbmdzL2FjY291bnROdW1iZXJSZXNvbHV0aW9uLmFzcHg/U0lEPUYwQkVGNzVERDA1ODQ5NEJCN0M5QTc5MTZGRjUxNEQwZGQCBQ9kFgRmDw8WAh8EBQpTaWduSW5Gb3JtZGQCAg8PFgIfBAUKU2lnbkluRm9ybWRkAgkPZBYCZg9kFgICAg8QDxYCHwQFClNpZ25JbkZvcm1kZGRkAgsPDxYCHgdWaXNpYmxlaGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYFBRhjdGwwMCRDdXN0b21lckhlYWRlciRyZDEFGGN0bDAwJEN1c3RvbWVySGVhZGVyJHJkMgUYY3RsMDAkQ3VzdG9tZXJIZWFkZXIkcmQzBRxjdGwwMCRDdXN0b21lckhlYWRlciRjaGtTYXZlBSxjdGwwMCRDb250ZW50SW5mbyRTaWduSW4kcmVtZW1iZXJtZSRjaGtSZW1NZaKBrzhMWTTBSXshMEJJqfJ6rL4V'
        ,'ctl00$CustomerHeader$ddlCountries':'US'
        ,'ctl00$CustomerHeader$rdlang':'en-us'
        ,'ctl00$CustomerHeader$chkSave':'on'
        ,'ctl00$CustomerHeader$countryText':''
        ,'ctl00$CustomerHeader$langText':''
        ,'ctl00$ContentInfo$hdnReturnPage':'/web/en-US/apps/account/account.aspx'
        ,'ctl00$ContentInfo$SignIn$onepass$txtField':'username'                                                 #filled in below
        ,'ctl00$ContentInfo$SignIn$password$txtPassword':'password'                                             #filled in below
        ,'ctl00$ContentInfo$SignIn$rememberme$chkRemMe':'on'
        ,'ctl00$ContentInfo$SignInSecure':'Sign In (Secure)'
    }




    form_data2 = {

        'hdnServer':'.182',
        'hdnSID':'84F9AA85289241C9AFF9621B7256C529',
        'hdnLangCode':'en-US',
        'hdnPOS':'US',
        'hdnClient':'76.212.212.84',                                                             #generic ip
        'hdnInactive':'false',
        'hdnAccountNumber':'',                                                                 #we need to fill in
        'hdnAccountNumberE':'Vprv7mYxhdVWIrmvlcsLKQ%3d%3d',
        'hdnAccountStatus':'0',
        '__EVENTARGUMENT':'',
        '__EVENTTARGET':'',
        'hdnTiming':'0.7029225 seconds',
        '__VIEWSTATE':'/wEPDwUKMTg4NTU1MDQ0Ng9kFgJmD2QWAgIDDxYCHghvbnVubG9hZAUSUHVyY2hhc2VBYmFuZG9uKCk7FgICAQ9kFgQCBQ9kFgICCQ9kFgICAQ9kFgwCAQ9kFgYCAQ9kFgRmDw8WBB4LTmF2aWdhdGVVcmwFP34vZW4tVVMvYXBwcy9taWxlYWdlcGx1cy9zdGF0ZW1lbnQvc3RhdGVtZW50LmFzcHg/TVA9MSZBQz1QcmludB4EVGV4dAUQUHJpbnRlciBGcmllbmRseWRkAgIPZBYCAgEPDxYEHwEFXX4vZW4tVVMvYXBwcy9wZGYvbWFpbi5hc3B4P0xpbms9fi9lbi1VUy9hcHBzL21pbGVhZ2VwbHVzL3N0YXRlbWVudC9zdGF0ZW1lbnQuYXNweD9NUD0xJkFDPVBERh8CBQtTYXZlIGFzIFBERmRkAgMPDxYCHwIFKVZpZXcgT3RoZXIgTWlsZWFnZVBsdXMgSGlzdG9yeSBTdGF0ZW1lbnRzZGQCBQ8QDxYGHg1EYXRhVGV4dEZpZWxkBRBEaXNwbGF5RGF0ZVJhbmdlHg5EYXRhVmFsdWVGaWVsZAUDS2V5HgtfIURhdGFCb3VuZGdkEBUDFzAzLzAxLzIwMTIgLSAwMy8wNC8yMDEyFzAxLzAxLzIwMTEgLSAxMi8zMS8yMDExFzAxLzAxLzIwMTAgLSAxMi8zMS8yMDEwFQMUMy80LzIwMTIgMTI6MDA6MDAgQU0WMTIvMzEvMjAxMSAxMjowMDowMCBBTRYxMi8zMS8yMDEwIDEyOjAwOjAwIEFNFCsDA2dnZ2RkAgMPZBYQAgEPDxYCHwIFGk1yLiBNaWNoYWVsIFdpbmZpZWxkIEFiYm90ZGQCBQ8PFgIfAgUIREZMNzM2NDNkZAIHDw8WAh8CBRcwMS8wMS8yMDEwIC0gMTIvMzEvMjAxMGRkAgkPDxYEHwIFEk1pbGVhZ2VQbHVzIFN0YXR1cx4HVmlzaWJsZWhkZAILDw8WBB8CBQ5PbmVQYXNzIG1lbWJlch8GaGRkAg0PFgIfBmhkAg8PFgIfBmhkAhEPFgIfBmgWBAIBDw8WBB8CBSBBY3Rpdml0eSBTaW5jZSBNeSBMYXN0IFN0YXRlbWVudB8GZ2RkAgMPDxYEHwIFE1ZpZXcgTGFzdCBTdGF0ZW1lbnQfBmhkZAIFDw8WAh8CBRpIaXN0b3JpY2FsIEFjY291bnQgU3VtbWFyeWRkAgcPFgIeCWlubmVyaHRtbAWPBTxzY3JpcHQgbGFuZ3VhZ2U9IkphdmFTY3JpcHQiIHNyYz0iaHR0cHM6Ly9hZC5kb3VibGVjbGljay5uZXQvYWRqL2NvbnQuZW4ub3BzdGF0ZS87Y2FiaW49O2hvbWFwPVNBTjtmbHRzcmNoZGVwYT07Zmx0c3JjaGRlc3Q9O29wdHlwZT0wO3RpbGU9MTtzej0zMDB4MTAwO29yZD03NDVjMjA3Yi1lYjYyLTQ0OTAtYjg4YS1hYTExZjIyN2VhOGY/IiB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPjwvc2NyaXB0Pg0KPG5vc2NyaXB0PjxhIGhyZWY9Imh0dHBzOi8vYWQuZG91YmxlY2xpY2submV0L2p1bXAvY29udC5lbi5vcHN0YXRlLztjYWJpbj07aG9tYXA9U0FOO2ZsdHNyY2hkZXBhPTtmbHRzcmNoZGVzdD07b3B0eXBlPTA7dGlsZT0xO3N6PTMwMHgxMDA7b3JkPTc0NWMyMDdiLWViNjItNDQ5MC1iODhhLWFhMTFmMjI3ZWE4Zj8iIHRhcmdldD0iX2JsYW5rIj48aW1nIHNyYz0iaHR0cHM6Ly9hZC5kb3VibGVjbGljay5uZXQvYWQvY29udC5lbi5vcHN0YXRlLztjYWJpbj07aG9tYXA9U0FOO2ZsdHNyY2hkZXBhPTtmbHRzcmNoZGVzdD07b3B0eXBlPTA7dGlsZT0xO3N6PTMwMHgxMDA7b3JkPTc0NWMyMDdiLWViNjItNDQ5MC1iODhhLWFhMTFmMjI3ZWE4Zj8iIHdpZHRoPSIzMDAiIGhlaWdodD0iMTAwIiBib3JkZXI9IjAiIGFsdD0iIj48L2E+PC9ub3NjcmlwdD5kAgkPZBYGZg8WAh8GaGQCAg9kFgQCBA9kFghmD2QWAgIBDw8WAh8CBR9FbmRpbmcgQmFsYW5jZSBhcyBvZiAxMi8zMS8yMDEwZGQCAQ9kFgICAQ8PFgIfAgUIMTQ5LDE0NiBkZAIDD2QWAgIBDw8WAh8CBQMwICpkZAIED2QWAgIBDw8WAh8CBQMwICpkZAIHD2QWAmYPZBYCZg8PFgIfAgV/KlByZW1pZXIgcXVhbGlmeWluZyBtaWxlcyBhbmQgc2VnbWVudHMgbWF5IGRpZmZlciBmcm9tIHRoZSBzdW1tYXJ5IGRldGFpbCBib3ggZHVlIHRvIGRlbGF5ZWQgY3JlZGl0aW5nIG9mIHByb21vdGlvbmFsIGFjdGl2aXR5LmRkAgQPFgIfBmhkAgsPZBYEAgIPFgIfBmhkAgQPFgIfBmdkAgsPDxYCHwZoZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFGGN0bDAwJEN1c3RvbWVySGVhZGVyJHJkMQUYY3RsMDAkQ3VzdG9tZXJIZWFkZXIkcmQyBRhjdGwwMCRDdXN0b21lckhlYWRlciRyZDMFHGN0bDAwJEN1c3RvbWVySGVhZGVyJGNoa1NhdmUF1qz4fSiFhPtmNqDA9Do3hcozvw==',
        'ctl00$CustomerHeader$ddlCountries':'US',
        'ctl00$CustomerHeader$rdlang':'en-us',
        'ctl00$CustomerHeader$chkSave':'on',
        'ctl00$CustomerHeader$countryText':'',
        'ctl00$CustomerHeader$langText':'',

        'ctl00$ContentInfo$drpStatementDates':'12/31/2013 12:00:00 AM',                        # need to fill in
        'ctl00$ContentInfo$imgbnGo':'Go',
        '__LASTFOCUS':''
    }



#    AES_Key = '0123456789abcdef'

    form_data['ctl00$ContentInfo$SignIn$onepass$txtField'] = RP_account['RP_username']
    form_data['ctl00$ContentInfo$SignIn$password$txtPassword'] =  mtk.decrypt(Globalvars.AES_Key,RP_account['RP_password'])
#    form_data['ctl00$ContentInfo$SignIn$password$txtPassword'] = RP_account['RP_password']


    s = requests.session()
    r_obj1 = s.post(url_loginSubmit, data = form_data)
#    mtk.write_file(r_obj1.text,'united_login.txt')
#    mtk.display_webpage(r_obj1.text)


###########################################################
#    This below code is a bit of a hack but it allows the user to input his Username or Account number as creditials
#    The actual Frequent flyer account number must be used to get the 3 activity statements.
#    The only way around it would be to force users to be able to use their FF # as login id only.

    soup = BeautifulSoup(r_obj1.text,"lxml")                                                   #main login page with most info
    RP_account_num = str(soup.find('span', id='ctl00_ContentInfo_AccountSummary_lblOPNumber'))               #account #
    RP_account_num = RP_account_num.replace('<span id="ctl00_ContentInfo_AccountSummary_lblOPNumber">','')                        #remove first part of tag
    RP_account_num = RP_account_num.replace('</span>','')                                                                  #remove second part of tag to leave only name
    form_data2['hdnAccountNumber'] = RP_account_num                                                     #we need to fill in

###########################################################


    statement_date = '12/31/XXXX 12:00:00 AM'                                        #base string
    date = datetime.now()
    statement_date1 = statement_date.replace('XXXX',str(date.year))
    statement_date2 = statement_date.replace('XXXX',str(date.year-1))
    statement_date3 = statement_date.replace('XXXX',str(date.year-2))
                                                                                            #we need to go back 3 year just to make sure we get 18 months worth of activity.
                                                                                            #United organized their data differently
    form_data2['ctl00$ContentInfo$drpStatementDates']= statement_date1                    #Get current year's activity
    r_obj3 = s.post(url3, data = form_data2)
#    mtk.write_file(r_obj3.text,'united_activity_get1.txt')
#    mtk.display_webpage(r_obj3.text)

    form_data2['ctl00$ContentInfo$drpStatementDates']= statement_date2                   #Get year before's activity
    r_obj4 = s.post(url3, data = form_data2)
#    mtk.write_file(r_obj4.text,'united_activity_get2.txt')
#    mtk.display_webpage(r_obj4.text)

    form_data2['ctl00$ContentInfo$drpStatementDates']= statement_date3                    #Get year before that activity
    r_obj5 = s.post(url3, data = form_data2)
#    mtk.write_file(r_obj5.text,'united_activity_get3.txt')
#    mtk.display_webpage(r_obj5.text)

    html_list = [r_obj1.text,r_obj3.text,r_obj4.text,r_obj5.text]
    return html_list







def scrape_webpage(html_list):
    RP_account = dict()

    soup = BeautifulSoup(html_list[0],"lxml")                                                       #main login page with most info
#    mtk.write_file(str(s),"unitedsoup.txt")
#    mtk.display_webpage(str(s))

    RP_account_name = str(soup.find('span', id='ctl00_CustomerHeader_spanCustName'))                            #name

    RP_account['RP_error'] = False                                                  #clear any error so we can test again
    if RP_account_name == 'None':                                                                               #Bad username, password, or general error from server.
        RP_account['RP_error'] = True
        return RP_account

    RP_account_num = str(soup.find('span', id='ctl00_ContentInfo_AccountSummary_lblOPNumber'))               #account #
    RP_balance = str(soup.find('span', id='ctl00_ContentInfo_AccountSummary_lblMileageBalance'))         #balance
    RP_expiration_date = str(soup.find('span', id='ctl00_ContentInfo_AccountSummary_lblMileageExpireDate'))      #Expiration Date#

    RP_account_name = RP_account_name.replace('<span id="ctl00_CustomerHeader_spanCustName">Welcome ','')                        #remove first part of tag
    RP_account_name = RP_account_name.replace(' | </span>','')                                                                  #remove second part of tag to leave only name
    RP_account['RP_account_name']= RP_account_name                                                                                 #name is only left

    RP_account_num = RP_account_num.replace('<span id="ctl00_ContentInfo_AccountSummary_lblOPNumber">','')                        #remove first part of tag
    RP_account_num = RP_account_num.replace('</span>','')                                                                  #remove second part of tag to leave only name
    RP_account['RP_account_num'] = RP_account_num                                                                                #account # is only left

    RP_balance = RP_balance.replace('<span id="ctl00_ContentInfo_AccountSummary_lblMileageBalance">','')                        #remove first part of tag
    RP_balance = RP_balance.replace(' </span>','')                                                                  #remove second part of tag to leave only name
    RP_balance = RP_balance.replace('</span>','')                                                                  #remove this way also just in case.
    RP_balance = RP_balance.replace(',','')
    RP_account['RP_balance']= int(RP_balance)                                                                                 #balance is only left

    now_date_obj = datetime.now()

    RP_account['RP_datestamp'] = str(now_date_obj.month) + '/' + str(now_date_obj.day) + '/' + str(now_date_obj.year)
    RP_account['RP_timestamp'] = str(now_date_obj.hour) + ':' + str(now_date_obj.minute) + ':' + str(now_date_obj.second)
    RP_account['RP_name']='United Airlines'                                          #set what program type it is
    RP_account['RP_inactive_time'] = '18 Months'
    RP_account['RP_partner']= 'Star Alliance'


    if RP_expiration_date == 'None':                                                                                #no expiration date on page ( maybe new account or no miles)
        RP_account['RP_expiration_date'] = 'N/A'
        RP_account['RP_days_remaining'] =  'N/A'
        RP_account['RP_last_activity_date'] = 'N/A'
    else:
        RP_expiration_date = RP_expiration_date.replace('<span id="ctl00_ContentInfo_AccountSummary_lblMileageExpireDate">','')                        #remove first part of tag
        RP_expiration_date = RP_expiration_date.replace('</span>','')                                                                  #remove second part of tag to leave only name

        date_obj = time.strptime(RP_expiration_date,"%m/%d/%Y")                                     #format date to '00/00/00'
        RP_expiration_date = time.strftime('%m/%d/%Y',date_obj)                                     #last Activity Date
        RP_account['RP_expiration_date'] = RP_expiration_date

        last_activity_date_obj = datetime.strptime(RP_expiration_date,'%m/%d/%Y')
        days_left = last_activity_date_obj - now_date_obj
        RP_account['RP_days_remaining'] =  days_left.days
    #    s4 = s.find_all(lambda tag: tag.name=='span' and tag.has_key('id') and tag.has_key('class'))      #find the table with Most recent activity

    # there are 2 main places to find the most recent activity
    #first we will try to find it listed on the main page.  It may or may not be there. It's time dependent and I'm not sure when it comes off and they just put it in the main statements
        activity_table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="activity")      #find the table with Most recent activity
        if activity_table != None :                                                                                     # we have recent activity here
            activity_data = activity_table.findAll(lambda tag: tag.name=='tr')                                          #get all the table data
            RP_last_activity_date = str(activity_data[1])                                                                                  #the most recent is the #2 obj in the Beautiful soup object
            RP_account['RP_last_activity_date'] = RP_last_activity_date[9:19]                                           #slice the date out of the string
        else:
    #it was not on main page. now we have to go back 3 years of statements to make sure we cover 18 months
    #Now we have to search the 3 different html pages of activity
            activity_list = []                                              #need to make a list of all the activity dates on the remaining 3 html pages

            soup = BeautifulSoup(html_list[1],"lxml")                      #Current year statement page
            activity_soup = soup.find_all('span', class_='Notes')          #zero in activity dates on this html page
            if activity_soup != None:
                add_activity_date_list(activity_soup,activity_list)        #add all actvity to our activity_list

            soup = BeautifulSoup(html_list[2],"lxml")                      #Go back another year and check for activity
            activity_soup = soup.find_all('span', class_='Notes')          #zero in activity dates on this html page
            if activity_soup != None:
                add_activity_date_list(activity_soup,activity_list)         #add all actvity to our activity_list

            soup = BeautifulSoup(html_list[3],"lxml")                      #Go back another year and check for activity  (we need to cover 3 years to make sure we get 18 months worth. United only does statements by year)
            activity_soup = soup.find_all('span', class_='Notes')          #zero in activity dates on this html page
            if activity_soup != None:
                add_activity_date_list(activity_soup,activity_list)         #add all actvity to our activity_list

            if activity_list is not None:
                activity_list.sort(reverse=True)                             #We have some activity. get the newest date first

                date_obj = datetime.strptime(activity_list[0],'%Y/%m/%d')      #We now have to put back into our original date format (first one in list is what we want)
                RP_last_activity_date = datetime.strftime(date_obj,'%m/%d/%Y')
                RP_account['RP_last_activity_date'] = RP_last_activity_date
            else:
                RP_account['RP_last_activity_date'] = 'N/A'                     #There was nothing in the list. So no activity

    return RP_account






def add_activity_date_list(soup_list,activity_list):

    for index in range(0,len(soup_list),10):                                    #activity date's are in groups of 10 tags so skip every 10 to get a new one that is pertinent
        activity_date = str(soup_list[index])                                     #get tag with date embedded in it
        description_str = str(soup_list[index+1])                                    #get the description.  We don't want anything activity that starts with "TRANSFER".  it's not valid
        if description_str.find('TRANSFER') == -1:                              #it's not here so we are assuming it's valid activity. -1 means it could not find it so it must be valid so process it
            activity_date = activity_date.replace('</span>','')                        #remove end tag
            s_index = activity_date.find('">')                                      #find the end of the beginnning tag
            activity_date = activity_date[s_index+2:]                           #skip over the '">' and get the date.  The date is in '12/15/2011' format we need "YYYY/MM/DD" format :(
            date_obj = datetime.strptime(activity_date,'%m/%d/%Y')              #switch up the format in the next two lines
            activity_date = datetime.strftime(date_obj,'%Y/%m/%d')
            activity_list.append(activity_date)                                     #a list of airline and non airline activity for this page   UNSORTED!!!!!!
    return