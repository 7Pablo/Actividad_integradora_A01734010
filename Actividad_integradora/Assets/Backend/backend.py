import flask
from flask.json import jsonify
import uuid
from paquetes import WareHouse

games = {}

app = flask.Flask(__name__)

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = WareHouse()
    return "ok", 201, {'Location': f"/games/{id}"}


@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()

    robot1 = model.schedule.agents[25]
    robot2 = model.schedule.agents[26]
    robot3 = model.schedule.agents[27]
    robot4 = model.schedule.agents[28]
    robot5 = model.schedule.agents[29]

    box1 = model.schedule.agents[0]
    box2 = model.schedule.agents[1]
    box3 = model.schedule.agents[2]
    box4 = model.schedule.agents[3]
    box5 = model.schedule.agents[4]
    box6 = model.schedule.agents[5]
    box7 = model.schedule.agents[6]
    box8 = model.schedule.agents[7]
    box9 = model.schedule.agents[8]
    box10 = model.schedule.agents[9]
    box11 = model.schedule.agents[10]
    box12 = model.schedule.agents[11]
    box13 = model.schedule.agents[12]
    box14 = model.schedule.agents[13]
    box15 = model.schedule.agents[14]
    box16 = model.schedule.agents[15]
    box17 = model.schedule.agents[16]
    box18 = model.schedule.agents[17]
    box19 = model.schedule.agents[18]
    box20 = model.schedule.agents[19]
    box21 = model.schedule.agents[20]
    box22 = model.schedule.agents[21]
    box23 = model.schedule.agents[22]
    box24 = model.schedule.agents[23]
    box25 = model.schedule.agents[24]

    pile1 = model.schedule.agents[30]
    pile2 = model.schedule.agents[31]
    pile3 = model.schedule.agents[32]
    pile4 = model.schedule.agents[33]
    pile5 = model.schedule.agents[34]

    return jsonify({ "Items": [
        {"x": robot1.pos[0], "y": robot1.pos[1]}, 
        {"x": robot2.pos[0], "y": robot2.pos[1]}, 
        {"x": robot3.pos[0], "y": robot3.pos[1]}, 
        {"x": robot4.pos[0], "y": robot4.pos[1]}, 
        {"x": robot5.pos[0], "y": robot5.pos[1]},
        {"x": box1.pos[0], "y": box1.pos[1]},
        {"x": box2.pos[0], "y": box2.pos[1]},
        {"x": box3.pos[0], "y": box3.pos[1]},
        {"x": box4.pos[0], "y": box4.pos[1]},
        {"x": box5.pos[0], "y": box5.pos[1]},
        {"x": box6.pos[0], "y": box6.pos[1]},
        {"x": box7.pos[0], "y": box7.pos[1]},
        {"x": box8.pos[0], "y": box8.pos[1]},
        {"x": box9.pos[0], "y": box9.pos[1]},
        {"x": box10.pos[0], "y": box10.pos[1]},
        {"x": box11.pos[0], "y": box11.pos[1]},
        {"x": box12.pos[0], "y": box12.pos[1]},
        {"x": box13.pos[0], "y": box13.pos[1]},
        {"x": box14.pos[0], "y": box14.pos[1]},
        {"x": box15.pos[0], "y": box15.pos[1]},
        {"x": box16.pos[0], "y": box16.pos[1]},
        {"x": box17.pos[0], "y": box17.pos[1]},
        {"x": box18.pos[0], "y": box18.pos[1]},
        {"x": box19.pos[0], "y": box19.pos[1]},
        {"x": box20.pos[0], "y": box20.pos[1]},
        {"x": box21.pos[0], "y": box21.pos[1]},
        {"x": box22.pos[0], "y": box22.pos[1]},
        {"x": box23.pos[0], "y": box23.pos[1]},
        {"x": box24.pos[0], "y": box24.pos[1]},
        {"x": box25.pos[0], "y": box25.pos[1]},
        {"x": pile1.pos[0], "y": pile1.pos[1]},
        {"x": pile2.pos[0], "y": pile2.pos[1]},
        {"x": pile3.pos[0], "y": pile3.pos[1]},
        {"x": pile4.pos[0], "y": pile4.pos[1]},
        {"x": pile5.pos[0], "y": pile5.pos[1]}
        ]})

app.run()
