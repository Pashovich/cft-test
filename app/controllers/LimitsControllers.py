
from aiohttp import web
from aiohttp import web
from app.models import Limits
from functools import wraps
from app.decorators.JsonValidator import JsonValidator
from app.schemes.limit import limit_schema_post, limit_schema_put
limit_routes = web.RouteTableDef()

class LimitsController:
    def __init__(self):
        self.data = dict()
        self.db_session = None



    def register(self,app):
        app.router.add_routes([
            web.get('/limits/{client_id}', self.get_limits_handler, name="limit_get"),
            web.post('/limits', self.post_limits_handler, name="limit_post"),
            web.put('/limits/{client_id}', self.put_limits_handler, name = "limit_put"),
            web.delete('/limits/{client_id}', self.delete_limits_handler, name = "limit_delete")
        ])


    async def get_limits_handler(self, request):
        db_session = request.app.session
        client_id = request.match_info['client_id']

        try:
            item = db_session.query(Limits).filter(Limits.client_id == client_id).one()
        except Exception :
            return web.json_response(
                status=404
            )

        return web.json_response(
            data=item.get_json(),
            status=200
        )
    @JsonValidator(limit_schema_post)
    async def post_limits_handler(self, request):
        db_session = request.app.session
        data = await request.json()

        item = Limits(**data)
        db_session.add(item)
        db_session.commit()

        return web.json_response(
            data=item.get_json(),
            status=200
        )

    @JsonValidator(limit_schema_put)
    async def put_limits_handler(self, request):
        db_session = request.app.session
        data = await request.json()

        client_id = request.match_info['client_id']

        try:
            item = db_session.query(Limits).filter(Limits.client_id == client_id).one()
        except Exception :
            return web.json_response(
                status=404
            )
        item.update(**data)
        db_session.commit()
        return web.json_response(
            data=item.get_json(),
            status=200
        )

    async def delete_limits_handler(self, request):
        db_session = request.app.session

        client_id = request.match_info['client_id']

        try:
            item = db_session.query(Limits).filter(Limits.client_id == client_id).one()
        except Exception :
            return web.json_response(
                status=404
            )

        db_session.delete(item)
        db_session.commit()

        return web.json_response(
            status=200
        )
