import debug
import graph_store
import statistics

graph = graph_store.Graph()

eric = graph.Node()
eric['name'] = 'Eric'
eric['age'] = 31
eric.job = 'QA'

josh = graph.Node()
josh['name'] = 'Josh'
josh['age'] = 24

al = graph.Node()
al.name = 'al'
al.age = 30
al.likes = ['orange']

alan = graph.Node()
alan.name = 'alan'
alan.new = True
alan.job = 'Tech'

graph.Relation(eric, 'Mentor', josh)
graph.Relation(eric, 'Co worker', al)
r = graph.Relation(josh, 'friend', alan)

with debug.TimerContextManager():
    graph.Search()._get_nodes().execute()

with debug.TimerContextManager():
    graph.Search()._get_nodes().execute()

graph.Search.get_by_value('name', 'Josh')

graph.Search().property('name').value('name', 'Josh').execute()

graph.Search().value('name', 'Eric').relations_to().execute()

graph.Search().relations_to().execute()

with debug.TimerContextManager():
    graph.Search.get_by_value('name', 'Josh')

with debug.TimerContextManager():
    graph.Search().value('name', 'Josh').execute()

NODES = 1000
print('create {} nodes'.format(NODES))
with debug.TimerContextManager():
    for i in range(NODES):
        graph.Node(name=i)

with debug.TimerContextManager():
    graph.Search()._get_nodes().execute()

with debug.TimerContextManager():
    graph.Search()._get_nodes().execute()

with debug.ProfileContextManager():
    graph.Search().value('name', 'Josh').execute()

'''with debug.TimerContextManager():
    graph.Search.get_by_value('name', 'Josh')

with debug.TimerContextManager():
    graph.Search.get_by_value('name', 'Josh')
'''
with debug.ProfileContextManager():
    graph.Search().value('name', 'Josh').execute()

graph.remove(josh)
graph.remove(josh)