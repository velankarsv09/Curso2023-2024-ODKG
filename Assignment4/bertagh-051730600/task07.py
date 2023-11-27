# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qINb5ZO4-kFEXhxYiHiO2zxldjlk8BOp

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

for s, p, o in g:
  print(s,p,o)

ns = Namespace("http://somewhere#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
from rdflib import XSD

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# SPARQL
print("SPARQL")
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject RDFS:subClassOf/RDFS:subClassOf* ns:LivingThing.
  }
  ''',
  initNs = { "RDFS": RDFS, "ns":ns }
)
#Visualize the results

for r in g.query(q1):
  print(r.Subject)


#RDFLib
print('RDFLib')
subclasses = []
def find_subclasses(class_x):
    for s, p, o in g.triples((None, RDFS.subClassOf, class_x)):
        subclasses.append(s)
        find_subclasses(s)

find_subclasses(ns.LivingThing)
# Visualize the results
for s in subclasses:
  print(s)


"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# SPARQL
print("SPARQL")

q2 = prepareQuery('''
   SELECT ?Individual  WHERE {
    ?Subject RDFS:subClassOf* ns:Person.
  ?Individual RDF:type ?Subject.
  }
  ''',
  initNs = { "RDFS": RDFS,
            "RDF": RDF,
             "ns":ns}
)
#Visualize the results

for r in g.query(q2):
  print(r.Individual)

#RDFLib
print('RDFLib')
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
   for s1,p1,o1 in g.triples((None,RDF.type, s)):
     print(s1)

for s2,p2,o2 in g.triples((None, RDF.type, ns.Person)):
  print(s2)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# SPARQL
print("SPARQL")

q3 = prepareQuery('''
   SELECT  ?Individual ?property WHERE {
    ?Individual ?property ?value
    {
    ?Subject RDFS:subClassOf ns:Person.
  ?Individual RDF:type ?Subject.
  }  UNION{
    ?Subject RDFS:subClassOf* ns:Animal.
  ?Individual RDF:type ?Subject.
  }}
  ''',
  initNs = { "RDFS": RDFS,
            "RDF": RDF,
             "ns":ns}
)
#Visualize the results

for r in g.query(q3):
  print((r.Individual),(r.property))

#RDFLib
print('RDFLib')
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  for s1,p1,o1 in g.triples((s, None, None)):
   print(s1 + p1)
for s,p,o in g.triples((None, RDF.type, ns.Animal)):
  for s1,p1,o1 in g.triples((s, None, None)):
   print(s1 + p1)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# SPARQL
print("SPARQL")

q4 = prepareQuery('''
  SELECT  ?Given WHERE {
    ?Subject foaf:knows ?RockySmith;
             vcard:Given ?Given.
  ?RockySmith vcard:FN ?RockySmithFullName.
  }
  ''',
  initNs = { "foaf": FOAF, "vcard": VCARD, "xsd":XSD}
)

for r in g.query(q4, initBindings = {'?RockySmithFullName' : Literal('Rocky Smith', datatype=XSD.string)}):
  print(r.Given)


#RDFLib
print('RDFLib')
for s,p,o in g.triples((None, FOAF.knows, ns.RockySmith)):
  for s1,p1,o1 in g.triples((s, VCARD.Given , None)):
    print(o1)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# SPARQL
print("SPARQL")

q5 = prepareQuery('''
 SELECT DISTINCT ?entity WHERE {
        ?entity foaf:knows ?other1 .
        ?entity foaf:knows ?other2 .
        FILTER(?other1 != ?other2)
    }''',
  initNs = { "foaf": FOAF}
)

# Visualize the results

for r in g.query(q5):
  print(r.Entity)


#RDFLib
print('RDFLib')

known_entities = {}

for s, p, o in g.triples((None, FOAF.knows, None)):
    if s in known_entities:
        if o not in known_entities[s]:
            known_entities[s].append(o)
    else:
        known_entities[s] = [o]

# Print entities that know at least two different entities
for s, known_list in known_entities.items():
    if len(known_list) >= 2:
        print(s)
