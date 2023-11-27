# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16Xa60txu_zUOAi-gKyrvwe2uYqKodJIH

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

from rdflib.plugins.sparql import prepareQuery
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
ns = Namespace("http://data.org#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Listar todos los elementos de la clase persona
q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject rdf:type ns:Person.
  }
  ''',
  initNs = { "ns": ns,"rdf":rdf}
)


for r in g1.query(q1):
  print(r.Subject)

# Anadir elementos del segundo grafo al primero
for s,p,o in g1.triples((None, rdf.type, ns.Person)):
  if not (s,vcard.Family, None) in g1:
    g1.add((s, vcard.Family,  g2.value(s, vcard.Family)))
  if not (s, vcard.Given, None) in g1:
    g1.add((s, vcard.Given, g2.value(s, vcard.Given)))
  if not (s,vcard.email, None) in g1:
    g1.add((s, vcard.EMAIL,  g2.value(s, vcard.EMAIL)))

# Ver todos los datos de las personas
q3 = prepareQuery('''
  SELECT ?person ?given ?family ?email
  WHERE {
    ?person rdf:type ns:Person .
    ?person vcard:Given ?given .
    ?person vcard:Family ?family .
    ?person vcard:EMAIL ?email .
  }
  ''',
  initNs={"rdf": rdf, "vcard": vcard,"ns":ns}
)
results = g1.query(q3)
for r in results:
  print(r.person,r.given,r.family,r.email)