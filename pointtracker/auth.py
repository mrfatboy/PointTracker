from base64 import urlsafe_b64encode
from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Authenticated, Everyone
import hashlib
from PointTracker import Valid_PointTracker_Account


#class Root(object):
#    __acl__ = [
#        (Allow, Viewer, Viewer),
#        (Allow, CanUploadApp, CanUploadApp),
#        (Allow, CanApproveApp, CanUploadApp),
#        (Allow, CanApproveApp, CanApproveApp),
#        (Allow, CanUploadLegal, CanUploadLegal),
#        (Allow, CanApproveLegal, CanUploadLegal),
#        (Allow, CanApproveLegal, CanApproveLegal),
#        (Allow, CanUploadWelcome, CanUploadWelcome),
#        (Allow, CanApproveWelcome, CanUploadWelcome),
#        (Allow, CanApproveWelcome, CanApproveWelcome),
#        (Allow, CanUploadCert, CanUploadCert),
#        (Allow, CanCreateAccounts, CanCreateAccounts),
#        (Allow, Admin, Admin),
#        (Allow, Admin, ALL_PERMISSIONS),
#    ]

#    def __init__(self, request):
#        self.request = request
#
#
#
#    def effective_principals(self, request):
#        effective_principals = [Everyone]
#        if request.access_levels:
#            effective_principals.append(Authenticated)
#            effective_principals.extend(list(request.access_levels))
#            effective_principals.append('user.' + request.username)
#
#        return effective_principals






__all__ = ['authentication_policy', 'authorization_policy']


@implementer(IAuthenticationPolicy)
class MyAuthenticationPolicy(object):
    """ An object representing My Pyramid authentication policy. """

    cookie_version = '1'

    def __init__(self, secret, cookie_name):
        self.secret = secret
        self.cookie_name = cookie_name


    def authenticated_userid(self, request):
        if self.unauthenticated_userid(request):
            return request.username



    def unauthenticated_userid(self, request):
        username = request.POST['username']
        password = request.POST['password']

        hash = hashlib.sha256()
        string = username  + "saltstring" + password
        encode_string = string.encode('utf-8')

        hash.update(encode_string)

        _id = hash.hexdigest()

        if Valid_PointTracker_Account(_id):
            return True                                         #he has a valid pointtracker account
        else:
            return False



    def effective_principals(self, request):
        effective_principals = [Everyone]
        if self.unauthenticated_userid(request):
            effective_principals.append(Authenticated)
            effective_principals.append('user')
            effective_principals.append(request.username)

        return effective_principals



    def remember(self, request, principal, **kw):
        username = request.POST['username']
        password = request.POST['password']
#        email = request.POST['email']
        remember_me = request.POST['remember_me']

        hash = hashlib.sha256()
        string = username  + "saltstring" + password
        encode_string = string.encode('utf-8')

        hash.update(encode_string)

        _id = hash.hexdigest()                                  #get unique hash for the database and cookie

        response = request.response
#Make sure _id is URL safe for future use.  We know it's a string now and safe
        if remember_me == 'true':
            max_age=315360000                                       #Don't log me out for a year
        else:
            max_age=600                                             #Log me out in 10 minutes
        response.set_cookie(self.cookie_name, _id, max_age if principal else None, secure=False, path='/')
        return


    def forget(self, request):
        response = request.response
        response.delete_cookie(self.cookie_name)
        return



authentication_policy = MyAuthenticationPolicy(
    secret = 'makeup32randomcharactersforthis!',
    cookie_name = 'PointTracker_Login'
)

authorization_policy = ACLAuthorizationPolicy()
