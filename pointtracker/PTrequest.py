from pyramid.decorator import reify
from pyramid.request import Request as BaseRequest
from pyramid.security import authenticated_userid
from pyramid.security import unauthenticated_userid
from pyramid.security import effective_principals
from pyramid.security import remember
from pyramid.security import forget


class PTRequest(BaseRequest):
#    @reify
    def hasPTaccount(self):
        answer = unauthenticated_userid(self)
        return answer

    @reify
    def username(self):
        if unauthenticated_userid(self):
            return self.username
        return

    def remember_me(self):
        remember(self,True)
        return

    def forget(self):
        forget(self)
        return



