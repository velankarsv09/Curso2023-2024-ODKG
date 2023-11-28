# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nX4QUViU3sz6M-4JLws1Nb-ZgWas6Cdl

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

#Veamos primero los datos de los dos grafos:
print("--------------------------------------------g1--------------------------------------------")
for s,p,o in g1:
    print(s,p,o)
print("--------------------------------------------g2--------------------------------------------")
for s,p,o in g2:
    print(s,p,o)

from rdflib.namespace import OWL, RDF
from rdflib.plugins.sparql import prepareQuery

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
data1 = Namespace("http://data.three.org#")
data2 = Namespace("http://data.four.org#")
owl = Namespace("http://www.w3.org/2002/07/owl#")

q1 = prepareQuery('''
SELECT ?person ?given ?family WHERE {
    ?person rdf:type data1:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
}
''',
    initNs = {"rdf":rdf, "data1":data1, "vcard":vcard}
)
q2 = prepareQuery('''
SELECT ?person ?given ?family WHERE {
    ?person rdf:type data2:Person.
    ?person vcard:Given ?given.
    ?person vcard:Family ?family.
}
''',
    initNs = {"rdf":rdf, "data2":data2, "vcard":vcard}
)

indiv1 = g1.query(q1)
indiv2 = g2.query(q2)


for r1 in indiv1:
    for r2 in indiv2:
        if r1.given == r2.given and r1.family == r2.family:
            g3.add((r1.person, OWL.sameAs, r2.person))

#Mostrar resultados del grafo g3
for s,p,o in g3:
    print(s,p,o)