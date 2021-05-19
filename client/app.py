from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import json
import json_read
from flask_basicauth import BasicAuth 

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'Admin'
app.config['BASIC_AUTH_PASSWORD'] = 'Admin'
app.wsgi_app = ProxyFix(app.wsgi_app)
basic_auth = BasicAuth(app)

api = Api(app, version='1.0', title='International Team',
          description='According to FIFA.com',
          )

ns = api.namespace('InternationalTeam', description='FIFA.com')
data = json_read.read()

@ns.route('/<string:iname>') 
class Teamget(Resource):
    @ns.doc('list_tasks') 
    def get(self,iname):
        for t in data:
            if t['name'].upper()==iname.upper():
                return t
        return ("sorry, we don't have this team")

    @basic_auth.required 
    def put(self,iname): 
        data = api.payload
        check=json_read.update(iname.upper(),data)
        if check == 200:
                result = [{"Message":"Update Complete"}]
        else :
                result = [{"Message":"Not Complete"}]
        return result


@ns.route('/')
@ns.response(404, 'Not found')
class delete(Resource):
    @basic_auth.required 
    @ns.doc('delete_task')
    @ns.response(204, 'Task deleted') 
    def delete(self):
        name = api.payload['Name']
        check = json_read.delete(name.upper())
        if check == 200:
            result = [{"Message":"Delete Complete"}]
        else :
            result = [{"Message":"Not Complete"}]
        return result

    @basic_auth.required 
    @ns.response(204, 'Task add')
    def post(self):
        check = json_read.add(api.payload)
        if check == 200:
            result = [{"Message":"ADD Complete"}]
        else :
            result = [{"Message":"Not Complete"}]
        return result
    

