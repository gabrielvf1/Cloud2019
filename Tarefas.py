from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import Api, Resource, reqparse
import sys
import requests

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('Tarefa', type=str)

f= open("/tmp/dados.txt","r")
dados = f.readlines()
for i in dados:
    linha = i.split()
    if linha[0] == 'ipPublic:':
        PublicIP = linha[1]

# PublicIP = '18.188.94.107'
class Tarefa(Resource):
    def get(self):
        tarefas = requests.get('http://' + PublicIP + ':8080' + '/Tarefa/')
        return tarefas.json()

    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        resposta = requests.post('http://' + PublicIP + ':8080' + '/Tarefa/', json={'Tarefa': tarefa})
        return resposta.json()


class Nada(Resource):
    def get(self):
        tarefas = requests.get('http://' + PublicIP + ':8080' + '/')
        return tarefas.json()


class TarefaId(Resource):
    def get(self, id):
        tarefas = requests.get('http://' + PublicIP + ':8080' + '/Tarefa/' + str(id))
        return tarefas.json()

    def put(self, id):
        request.get_json(force=True)
        args = parser.parse_args()
        tarefa =  str(args['Tarefa'])
        print('http://' + PublicIP + ':8080' + '/Tarefa/' + str(id))
        a = requests.put('http://' + PublicIP + ':8080' + '/Tarefa/' + str(id), json={'Tarefa': tarefa})
        return a.json()

    def delete(self, id):
        del Tarefas[id]
        resposta = requests.delete('http://' + PublicIP + ':8080' + '/Tarefa/' + str(id))
        return resposta.json()

class HealthCheck(Resource):
    def get(self):
        tarefas = requests.get('http://' + PublicIP + ':8080' + '/HealthCheck')
        return  tarefas.json()

api.add_resource(Tarefa, '/Tarefa/')
api.add_resource(HealthCheck, '/HealthCheck')
api.add_resource(TarefaId, '/Tarefa/<int:id>')
api.add_resource(Nada, '/')


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=8080)
