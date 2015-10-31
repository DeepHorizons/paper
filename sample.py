
import graph_store

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
graph.Relation(josh, 'friend', alan)
