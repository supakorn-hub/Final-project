import json

team_data = open("ranking.json","r")
data = team_data.read()
load_data = json.loads(data)

def read():
    return load_data

def update(iname,data):
    a_file = open("ranking.json","w")
    for count,i in enumerate(load_data):
        if i["name"].upper()==iname:
            for update_item in list(data.keys()):
                if update_item not in list(i.keys()):
                    return 400
                
            load_data[count].update(data)
            json.dump(load_data,a_file)
            return 200

def delete(iname):
    a_file = open("ranking.json","w")
    for i in load_data:
        if i["name"].upper()==iname.upper():
            load_data.remove(i)
            json.dump(load_data, a_file)
            return 200
    return 400 

def add(data):
    a_file = open("ranking.json","w")    
    load_data.append(data)
    json.dump(load_data, a_file)
    return 200        