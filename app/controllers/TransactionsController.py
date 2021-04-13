
from datetime import datetime
from sqlalchemy import extract
from aiohttp import web
from app.models import Limits, Transactions
# from sqlalchemy.exc import NoResultFound
from app.decorators.JsonValidator import JsonValidator
from app.schemes.transaction import transaction_schema_post
import time

transaction_routes = web.RouteTableDef()


class TransactionsController:
    def __init__(self):
        pass
    

    def register(self,app):
        app.router.add_routes([
            web.post('/transactions', self.post_transactions_handler, name = 'transaction_post')
        ])

    @JsonValidator(transaction_schema_post)
    async def post_transactions_handler(self,request):
        db_session = request.app.session
        data = await request.json()

        try:
            limit = db_session.query(Limits).filter(Limits.client_id == data['client_id'], 
                                                    Limits.cur == data['cur'],
                                                    Limits.country == data['country']
                                                    ).one()
        except Exception :
            return web.json_response(
                {"error_msg" : "Not found limit for this params"},
                status=404
            )
        data['date'] = datetime.fromtimestamp(data.get('date', int(time.time())))
        transactions = db_session.query(Transactions).filter(
            Transactions.client_id == data['client_id'],
            Transactions.cur == data['cur'],
            Transactions.country == data['country'],
            extract('year', Transactions.date) == data['date'].year,
            extract('month', Transactions.date) == data['date'].month
        ).all()
        amount = 0

        if transactions != None:
            amount = sum([transaction.amount for transaction in transactions])
        if amount + data['amount'] > limit.limit:
            return web.json_response(
                {"error_msg" : "Limit exeeded"},
                status=400
            )

        transaction = Transactions(**data)
        db_session.add(transaction)
        db_session.commit()
        return web.json_response(
            status=200,
            data= transaction.get_json()
        )
