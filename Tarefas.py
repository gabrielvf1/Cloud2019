from flask import Flask, json, request
dictTarefas = {}
result = list(range(100))

dictTarefas[result[0]] = "Acordar"
dictTarefas[result[1]] = "Dormir"


class Tarefas:
    def __init__(self, atributo1, atributo2):
        self.atributo1 = atributo1
        self.atributo2 = atributo1


def acha_key(id):
    for i in dictTarefas:
        if id == i:
            return True
    return False


app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    return "200"


@app.route('/Tarefa', methods=['GET', 'POST'])
def tarefa():
    if request.method == 'GET':
        data = dictTarefas
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    if request.method == 'POST':
        nomeTarefa = request.args.get("Tarefa")
        dictTarefas[len(dictTarefas)] = nomeTarefa
        data = dictTarefas
        response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
         )
        return response


@app.route('/Tarefa/<id_tarefa>', methods=['GET', 'PUT', 'DELETE'])
def tarefa_id(id_tarefa):
    if request.method == 'GET':
        existe = acha_key(int(id_tarefa))
        if (not(existe)):
            return 404
        data = dictTarefas[int(id_tarefa)]
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    if request.method == 'PUT':
        existe = acha_key(int(id_tarefa))
        if (not(existe)):
            return "Tarefa_Inexistente"
        nomeTarefa = request.args.get("Tarefa")
        dictTarefas[int(id_tarefa)] = nomeTarefa
        response = app.response_class(
            response=json.dumps(str(id_tarefa) + ": " + dictTarefas[int(id_tarefa)]),
            status=200,
            mimetype='application/json'
        )
        return response

    if request.method == 'DELETE':
        existe = acha_key(int(id_tarefa))
        if (not(existe)):
            return "Tarefa_Inexistente"
        del dictTarefas[int(id_tarefa)]
        response = app.response_class(
            response=json.dumps(str(id_tarefa) + ": " + dictTarefas[int(id_tarefa)]),
            status=200,
            mimetype='application/json'
        )
        return dictTarefas

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
