from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('Tarefa', type=str)

Tarefas = {1: "Dormir", 2: "Andar"}
a = 3


class Tarefa(Resource):
    def get(self):
        return jsonify(Tarefas)

    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        # tarefa = request.args.get("Tarefa")
        Tarefas[len(Tarefas)+1] = tarefa
        return jsonify({"Tarefas": Tarefas})


class Nada(Resource):
    def get(self):
        return "Hello WOrld"


class TarefaId(Resource):
    def get(self, id):
        return jsonify({"Tarefa": Tarefas[id]})

    def put(self, id):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        Tarefas[id] = tarefa
        return jsonify({"Tarefas": Tarefas})

    def delete(self, id):
        del Tarefas[id]
        return jsonify({"Tarefas": Tarefas})

class HealthCheck(Resource):
    def get(self):
        return  jsonify({"Status": 200})

api.add_resource(Tarefa, '/Tarefa/')
api.add_resource(HealthCheck, '/HealthCheck')
api.add_resource(TarefaId, '/Tarefa/<int:id>')
api.add_resource(Nada, '/')


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)

