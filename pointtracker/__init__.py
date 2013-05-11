from wsgiref.simple_server import make_server
from pyramid.mako_templating import renderer_factory as mako_factory
from pyramid.config import Configurator
from PTrequest import PTRequest
from auth import authentication_policy, authorization_policy
#from auth import Root
from PointTracker import Init_App
import Globalvars
import os



def main(global_config, **settings):
    Init_App()

    config = Configurator(authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          settings=settings)


    config.add_renderer('.html', mako_factory)                          #Make it so .html files are recognized and goes thru the MAKO factory

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')                                       #sign in page
    config.add_route('Sign_Out', '/sign_out')                           #sign out (this gets redirected back to 'home' or '/'
    config.add_route('pointtracker', '/pointtracker')                   #main info page with account data
    config.set_request_factory(PTRequest)                               #Hook in our custom Request Object

    config.scan('pointtracker.views')                                   #scan our pointtracker project directory for any Views  (all of ours are in views.py)

    app = config.make_wsgi_app()
    return app



if __name__ == '__main__':

    app = main(global_config=None)
    if Globalvars.DEVELOPMENT:
        server = make_server('0.0.0.0', 6543, app)                      #Serve from our local server
    else:
        server = make_server(os.environ['OPENSHIFT_INTERNAL_IP'], 8080, app)    #Serve from the Openshift website
#        server = make_server('127.11.64.1', 8080, app)
    server.serve_forever()