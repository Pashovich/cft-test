from app.controllers import LimitsController, TransactionsController

def set_routes(app):
    TransactionsController().register(app)
    LimitsController().register(app)
