# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17-1_EK9LqWcT5WysqsHsiTci6Z27sGIl

**Task 06: Modifying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**

"""

# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")
g.add((ns.JaneSmith, RDF.type, ns.Researcher))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**"""

from rdflib import XSD
# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")
VCARD=Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

g.add((ns.JaneSmith, VCARD.FN, Literal("Jane Smith", datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.hasEmail, Literal("JaneSmith@email.com", datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Given, Literal("Jane", datatype=XSD.string)))
g.add((ns.JaneSmith, VCARD.Family, Literal("Smith", datatype=XSD.string)))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""

# TO DO
# Visualize the results
ns = Namespace("http://somewhere#")

g.add((ns.Workplace, RDF.type, RDF.Property))
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JonhSmith, ns.Workplace, ns.UPM))
for s, p, o in g:
  print(s,p,o)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**"""

# TO DO
# Visualize the results
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
ns = Namespace("http://somewhere#")

g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))
for s, p, o in g:
  print(s,p,o)