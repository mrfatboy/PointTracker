__author__ = 'Office'


def display_program_info (account):
    #Displays info for an individual account
    print ('{:<30}{:<25}{:<15}{:>10,d}\t\t{:<25}{:<20}{:<15}{:<15}'.format(
        account['PA_name'],account['PA_reward_program_name'],account['PA_account_num'],account['PA_balance'],account['PA_last_activity_date'],account['PA_expiration_date'],account['PA_inactive_time'],account['PA_days_remaining']))
    return





def Encrypt_PA_account_passwords(PT_account):

    print ('Encrypting all Program Accounts in all Sub Account')
    for sub_account in PT_account['PT_sub_accounts']:                                        #PointTracker accounts are made up of sub accounts of other people's accounts
        print ('Account :',sub_account['SA_name'])                                                 #sub_account name

        for program_account in sub_account['SA_program_accounts']:                                                       #go thru list of program accounts for each sub account

            key = '0123456789abcdef'

            password = program_account['PA_password']                   #get unencrypted password
            encrypted_password = mtk.encrypt(key,password)              #encrypt it
            program_account['PA_password'] = encrypted_password         #save it encrypte
            print('\t {} encrypted',format(program_account['PA_reward_program_name']))

    print ('Completed')
    return











def update_and_display_PointTracker_account(PT_account):

    print ('\n\n')
    print ('==================================================================================================================================================================')
    print ('=                                                                PointTracker                                                                                    =')
    print ('==================================================================================================================================================================')
    print ('\n')

    grand_total_points = 0

    for sub_account in PT_account['PT_sub_accounts']:                                        #PointTracker accounts are made up of sub accounts of other people's accounts
        print ('Account :',sub_account['SA_name'])                                                 #sub_account name
        print ('{:<30}{:<25}{:<15}{:>10}\t\t{:<25}{:<20}{:<15}{:<15}'.format('Name','Program','Account','Balance','Last Activity Date','Expiration Date','Program Time','Days Remaining'))
        print ('------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        sub_total_points =0
        for program_account in sub_account['SA_program_accounts']:                                                       #go thru list of program accounts for each sub account
            scraped_program_account = process_program(program_account)                               #Login & Scrape current program info
            display_program_info(scraped_program_account)                                                #print it out on one line
            sub_total_points = sub_total_points + scraped_program_account['PA_balance']

        print ('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print ('                                                         Sub Total    {:>10,d}'.format(sub_total_points))
        print ('\n')
        grand_total_points = grand_total_points + sub_total_points

    print ('                                            All Sub Accounts Total    {:>10,d}'.format(grand_total_points))
    return










def display_PointTracker_account(PTaccount):

    print ('\n\n')
    print ('==================================================================================================================================================================')
    print ('=                                                                PointTracker                                                                                    =')
    print ('==================================================================================================================================================================')
    print ('\n')

    grand_total_points = 0

    for sub_account in PTaccount['PT_sub_accounts']:                                        #PointTracker accounts are made up of sub accounts of other people's accounts
        print ('Account :',sub_account['SA_name'])                                                 #sub_account name
        print ('{:<30}{:<25}{:<15}{:>10}\t\t{:<25}{:<20}{:<15}{:<15}'.format('Name','Program','Account','Balance','Last Activity Date','Expiration Date','Program Time','Days Remaining'))
        print ('------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        sub_total_points =0
        for program_account in sub_account['SA_program_accounts']:                                                       #go thru list of program accounts for each sub account
            display_program_info(program_account)                                                #print it out on one line
            sub_total_points = sub_total_points + program_account['PA_balance']

        print ('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print ('                                                         Sub Total    {:>10,d}'.format(sub_total_points))
        print ('\n')
        grand_total_points = grand_total_points + sub_total_points

    print ('                                            All Sub Accounts Total    {:>10,d}'.format(grand_total_points))
    return









def write_unencrypted_PointTracker_account(PTaccount, filename):
    print('writing file')
    unencrypted_file = json.dumps(PTaccount)

    mtk.write_file(unencrypted_file,filename)
    print('writing file done')

    return







def read_PointTracker_account():
    key = '0123456789abcdef'

    encrypted_file = mtk.read_file('PointTracker_data_encrypt.json')
    decrypted_file = mtk.decrypt(key,encrypted_file)
    PointTracker_Account = json.loads(decrypted_file)

    return (PointTracker_Account)


def write_PointTracker_account(PTaccount):
    key = '0123456789abcdef'

    unencrypted_file = json.dumps(PTaccount)

    #    mtk.write_file(unencrypted_file,'PointTracker2_decrypted2.ini')

    encrypted_file = mtk.encrypt(key,unencrypted_file)
    mtk.write_file(encrypted_file,'PointTracker_data2_dummy_encrypt.json')
    return



def load_PointTracker_account():
    file = mtk.read_file('PT_account1_encrypt.json')
    PT_account = json.loads(file)
    return (PT_account)


def Load_PTaccount():
    file = mtk.read_file('PT_account1_encrypt.json')
    PT_account = json.loads(file)
    return (PT_account)


def dump_PointTracker_account(PT_account):
    write_PointTracker_account(PT_account)
    return


#this scrapes entire Pointracker account with subs and returns a new PointTracker account
def update_PointTracker_account(PT_account):
    new_pt_account = list()

    for sub_account in PT_account:                                        #PointTracker accounts are made up of sub accounts of other people's accounts
        new_sub_account = list()

        sub_account_programs = list()

        for program_account in sub_account[1]:                                                       #go thru list of program accounts for each sub account
            scraped_program_account = process_program(program_account)                               #Login & Scrape current program info
            sub_account_programs.append(scraped_program_account)                                            #get each program info and add it to the list

        new_sub_account.append(sub_account[0])                                      #add the sub account name
        new_sub_account.append(sub_account_programs)                                #add the program accounts for that sub account
        new_pt_account.append(new_sub_account)                                      #add the sub account to main account

    return (new_pt_account)


def load_dummy_PointTracker_account():
    file = mtk.read_file('PT_account1_encrypt.json')
    PT_account = json.loads(file)
    return (PT_account)


def Python_Test_Method(text):
    mtk.write_file(text,'Python_Test.txt')
    return



