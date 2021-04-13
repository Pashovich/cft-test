from .routes import set_routes
from .db import get_session


def app_config(app):
    app.session = get_session()
    set_routes(app)
    return app

