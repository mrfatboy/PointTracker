from pyramid.view import view_config
#from pyramid.renderers import render
#from pyramid.response import Response
#from pyramid.renderers import render_to_response
#from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound

from PointTracker import Get_PointTracker_Account
from PointTracker import Register_PointTracker_Account
from PointTracker import Add_Sub_Account
from PointTracker import Delete_Sub_Account
from PointTracker import Add_Reward_Program
from PointTracker import Refresh_Reward_Program
from PointTracker import Edit_Reward_Program
from PointTracker import Delete_Reward_Program
from PointTracker import Return_Reward_Program
from PointTracker import Remove_PT_account_Reward_Program_Passwords

#from PointTracker import hack_mongo






@view_config(route_name='home', renderer='pointtracker:templates/index.html')               #pull up our index.html
def server_view0(request):
    if 'PointTracker_Login' in request.cookies:                                             #is the cookie set?
        url = request.route_url('pointtracker')                                             #cookie was set so redirect
        return HTTPFound(location=url)
    return {}



@view_config(renderer="json", name="Sign_In_View")
def server_view1(request):
    hasAccount = request.hasPTaccount()
    if hasAccount:                                                          #true?
        request.remember_me()                                               #remember me will determine cookie time limit
    return hasAccount



@view_config(renderer="json", name="Register_View")
def server_view2(request):
#    hack_mongo(request.POST)
    hasAccount = request.hasPTaccount()                                     #the account already exists so don't create a new one and warn user
    if not hasAccount:
        Register_PointTracker_Account(request.POST)                         #Register the account in the database
        request.remember_me()                                               #remember me will determine cookie time limit
    return hasAccount



@view_config(route_name='Sign_Out', renderer='pointtracker:templates/index.html')               #pull up our index.html
def server_view3(request):
    request.forget()                                                                            #delete cookie
    return {}



@view_config(route_name='pointtracker', renderer='pointtracker:templates/pointtracker.html')               #pull up our index.html
def server_view4(request):
    if 'PointTracker_Login' not in request.cookies:                             #is the cookie set?
        url = request.route_url('home')                                     #cookie is not set so redirect home sign in page
        return HTTPFound(location=url)
    return {}                                                               #No return dict at this time.  All of our info comes from Get_PointTracker_account ajax calls



@view_config(renderer="json", name="Get_PointTracker_Account_View")        #Get our PT_account of of the database
def server_view5(request):
    _id = request.cookies['PointTracker_Login']                            # cookie is in here and contains the _id
    PT_account = Get_PointTracker_Account(_id)                             # Pull the PT_account out of the database
    Remove_PT_account_Reward_Program_Passwords(PT_account)                 # we need to remove RP_account passwords so that they can't be seen on client side
    return PT_account



@view_config(renderer="json", name="Update_PointTracker_Account_View")
def server_view6(request):
    RP_account = Refresh_Reward_Program(request.GET)                       #Get the new updated Reward Program
    return RP_account



@view_config(renderer="json", name="Add_Sub_Account_View")
def server_view7(request):
    Add_Sub_Account(request.GET)                                            #Add a new sub account to the database
    return



@view_config(renderer="json", name="Delete_Sub_Account_View")
def server_view8(request):
    Delete_Sub_Account(request.GET)                                         #Delete a sub account out of the database
    return



@view_config(renderer="json", name="Add_Reward_Program_View")
def server_view9(request):
    RP_account = Add_Reward_Program(request.GET)                            #Add a Reward Program to the database
    return RP_account                                                       #Check later if needed for callbacks



@view_config(renderer="json", name="Delete_Reward_Program_View")
def server_view10(request):
    Delete_Reward_Program(request.GET)                                      #Delete a Reward Program from the database
    return



@view_config(renderer="json", name="Refresh_Reward_Program_View")
def server_view11(request):
    RP_account = Refresh_Reward_Program(request.GET)                        #Refreshes by scraping and updating the database
    return RP_account                                                       #Return for callback info inside



@view_config(renderer="json", name="Edit_Reward_Program_View")
def server_view12(request):
    RP_account = Edit_Reward_Program(request.GET)                           #Edit/Modify a Reward Program in the database
    return RP_account                                                       #Check later if needed for callbacks



@view_config(renderer="json", name="Get_Reward_Program_View")
def server_view13(request):
    RP_account = Return_Reward_Program(request.GET)                         #Returns Reward Program from database  (used for testing purposes without scraping and updating database
    RP_account['RP_password'] = ''                                          #Remove password for client side for security reasons. no reason for the client to have it.
    return RP_account


@view_config(route_name='FAQ', renderer='pointtracker:templates/FAQ.html')               #pull up our FAQ.html
def server_view14(request):
    return {}


@view_config(route_name='test_page', renderer='pointtracker:templates/test_page.html')               #pull up our FAQ.html
def server_view15(request):
    return {}






