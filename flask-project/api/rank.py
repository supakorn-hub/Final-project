from flask import request,jsonify,Response,current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
import json

class RankApi(Resource):      
    @jwt_required() 
    def put(self,teamname):#รับ PUT
        info = request.get_json()
        status = updatejson(teamname, info)
        if status == 200:
            return {
                "message": teamname +" HAS BEEN UPDATED."}, 200
        elif status == 500:
            return {"message": "FAIL TO UPDATED."}, 500

    @jwt_required() 
    def delete(self,teamname):
        status = deleteJson(teamname)
        if status == 200:
            return {"message":teamname+" has been deleted."}, 200
        elif status == 500:
            return {"message":teamname+" not found."}, 500

def readJson():
    open_json_file = open('ranking.json', 'r') 
    read_json_file = open_json_file.read()
    team_data = json.loads(read_json_file)
    return team_data

def writeJson(team_dict):
    team_list = readJson()
    for i in team_list: 
        if i['name'] == team_dict['name']:
            return 404
    team_list.append(team_dict)
    open_json_file = open('ranking.json', 'w')
    json.dump(team_list, open_json_file, indent=4) 
    return 200

def updatejson(team_name, new_info):
    team_list = readJson()
    if len(new_info) == 0:
        return 500
    for index, item in enumerate(team_list):
        if item['name'].lower() == team_name.lower():
            for update_item in list(new_info.keys()): 
                if update_item not in list(item.keys()):
                    return 500
            team_list[index].update(new_info)
            open_json_file = open('ranking.json', 'w')
            json.dump(team_list, open_json_file, indent=4)
            return 200
    return 500

def deleteJson(teamname):
    team_list = readJson()
    for item in team_list:
        if item['name'].lower() == teamname.lower():
            team_list.remove(item)
            open_json_file = open('ranking.json', 'w')
            json.dump(team_list, open_json_file, indent=4)
            return 200
    return 500