from flask import Flask
from flask_mongoengine import MongoEngine


db = MongoEngine()


def create_app(**config_overrides):

    app = Flask(__name__)

    # config the app using the settings file
    app.config.from_pyfile("settings.py")

    # override the app used for testings purposes
    app.config.update(config_overrides)

    # register the application to the database
    db.init_app(app)

    # import the blueprints from the views
    from user.register.views import registration_app
    from user.login.views import login_app
    from user.password.views import password_app
    from home.views import home_app
    from user.profile.views import profile_app
    from user.edit.views import edit_app
    from relationship.views import relationship_app
    from feeds.views import feed_app
    from user.logout.logout import logout_app


    # register the blueprint

    app.register_blueprint(registration_app)
    app.register_blueprint(login_app)
    app.register_blueprint(password_app)
    app.register_blueprint(home_app)
    app.register_blueprint(profile_app)
    app.register_blueprint(edit_app)
    app.register_blueprint(relationship_app)
    app.register_blueprint(feed_app)
    app.register_blueprint(logout_app)

    return app