import graph_store

graph = graph_store.Graph()

eric = graph.Node()
eric['name'] = 'Eric'
eric['age'] = 31
eric.job = 'QA'

josh = graph.Node()
josh['name'] = 'Josh'
josh['age'] = 24

r = graph.Relation(eric, josh)
r['related'] = 'Mentor'