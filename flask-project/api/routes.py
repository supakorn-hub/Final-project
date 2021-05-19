from flask_restful import Api

from api.rank import RankApi
from api.authentication import TokenApi,RefreshToken
def create_route(api: Api):

    api.add_resource(TokenApi,'/authentication/token')
    api.add_resource(RefreshToken,'/authentication/token/refresh')

    api.add_resource(RankApi, '/rank')


