from flask import Flask,render_template,request
from werkzeug import datastructures
from flask_cors import CORS
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api
from PIL import Image
import base64
from ml import TFModel
import os,json,requests
from flask_sqlalchemy import SQLAlchemy
from api.routes import create_route
from flask_swagger_ui import get_swaggerui_blueprint

config = {
    'JSON_SORT_KEYS': False,
    'JWT_SECRET_KEY': 'BaNPFol%Dgfgge',
    'JWT_ACCESS_TOKEN_EXPIRES': 300,
    'JWT_REFRESH_TOKEN_EXPIRES': 604800
}

#init app
app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = TFModel(model_dir='./ml-model/')
model.load()
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"
], supports_credentials=True)


app.config.update(config)

api = Api(app)
create_route(api=api)

# swagger specific
SWAGGER_URL = '/swagger'
API_URL = '/static/ranking.yaml'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Flask RESTful API"
    }
)
app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

# init JWT
jwt = JWTManager(app=app)



@app.route("/")
def home():
    data = readJson()
    return render_template("index.html",data = data)


@app.route('/scan', methods=['GET', 'POST'])
def upload_file():
    data = readJson()
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'there is no file in form!'
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        imageteam = Image.open(path)
        outputs = model.predict(imageteam)
        imagename = imageteam.filename
        ranks = []
        name = outputs['predictions'][0]['label']
        for i in data:
            if  name == i['name']:
                ranks.append(i)   
                ranks.append({
                "ranking": "ไม่มีข้อมูล",
                "name": "ไม่มีข้อมูล",
                "nickname": "ไม่มีข้อมูล",
                "manager": "ไม่มีข้อมูล",
                "point": "ไม่มีข้อมูล",
                "continental": "ไม่มีข้อมูล",
                "player": "ไม่มีข้อมูล"
        },)
                
        return render_template('prediction.html', pred_result=outputs,pic = imagename,rankings = ranks)

    return render_template('upload.html')

def readJson():
    open_json_file = open('ranking.json', 'r') 
    read_json_file = open_json_file.read()
    team_data = json.loads(read_json_file)
    return team_data

