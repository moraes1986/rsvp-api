from flask import Flask, Blueprint
from flask_restx import Api

from .controllers.routes.user import user, user_ns
from .controllers.routes.guest import guests, guests_ns
from .model.extensions import database
from .model.extensions.jwt import configure_jwt, setup_jwt
from .model.commands.userCommands import userCommands
from .model.commands.guestCommands import guestCommands
from .web.views.main_view import main
from .web.views.account_view import account
from .web.views.guest_view import guest as guest_view

#from app.model.config import get_config

api_bp = Blueprint( 'api', __name__, url_prefix='/api/v1' )
 
api = Api(
    api_bp,
    catch_all_404s=True,
    version='1.0',
    title='RSVP API - List Confirmation',
    description='Welcome to RSVP API with Swagger UI documentation',
    doc='/docs',
    authorizations=setup_jwt(),
)

api.add_namespace( user_ns, path='/user')
api.add_namespace( guests_ns, path='/guest' )
#api.add_namespace( parents_ns, path='/parent' )

def create_app(config_object="app.settings"):
    app = Flask(__name__,
                static_url_path='',
                static_folder='web/static',
                template_folder='web/templates')
    
    app.config.from_object(config_object)
    configure_jwt(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(user)
    app.register_blueprint(guests)
    app.register_blueprint(main)
    app.register_blueprint(account)
    app.register_blueprint(guest_view)
    app.register_blueprint(userCommands)
    app.register_blueprint(guestCommands)
    database.init_app(app)

    return app



