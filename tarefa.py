#!/usr/bin/python
import sys
import requests

try:
    palavra1 = sys.argv[1].lower()
except :
    palavra1 = 0
    pass

try:
    palavra2 = sys.argv[2]
except :
    palavra2 = 0
    pass

try:
    palavra3 = sys.argv[3]
except :
    palavra3 = 0
    pass


if (palavra1 == 'listar'):
    tarefas = requests.get('http://127.0.0.1:5000/Tarefa')
    print(tarefas.json())

if (palavra1 == 'adicionar' and palavra2 != 0):
    a = requests.post('http://127.0.0.1:5000/Tarefa/', json={'Tarefa': palavra2})
    tarefas = requests.get('http://127.0.0.1:5000/Tarefa/')
    print(tarefas.json())

if (palavra1 == 'buscar' and palavra2 != 0):
    tarefas = requests.get('http://127.0.0.1:5000/Tarefa/' + palavra2)
    print(tarefas.json())

if (palavra1 == 'apagar' and palavra2 != 0):
    tarefas = requests.delete('http://127.0.0.1:5000/Tarefa/' + palavra2)
    print(tarefas.json())

if (palavra1 == 'atualizar' and palavra2 != 0 and palavra3 != 0):
    requests.delete('http://127.0.0.1:5000/Tarefa/' + palavra2)
    tarefa = requests.put('http://127.0.0.1:5000/Tarefa/' + palavra2, json={'Tarefa': palavra3} )
    tarefas = requests.get('http://127.0.0.1:5000/Tarefa')
    print(tarefas.json())

else:
    print('===================================== '+ 'HELP' + ' =======================================' + "\n")
    print('tarefa '+ 'listar' + ' --LISTA AS TAREFAS DO DICIONARIO' + "\n")
    print('tarefa '+ 'adicionar' + " [tarefa_a_ser_adicionada]" + ' --ADICIONA UMA TAREFA' + "\n")
    print('tarefa '+ 'buscar' + " [id_tarefa_buscada]"  + ' --BUSCA UMA TAREFA' + "\n")
    print('tarefa '+ 'apagar' + " [id_tarefa_apagada]"  + ' --APAGA UMA TAREFA' + "\n")
    print('tarefa '+ 'atualizar' + " [id_tarefa_a_ser_atualizada]" + " [nome_tarefa]"  + ' --ATUALIZA UMA TAREFA DO DICIONARIO' + "\n")