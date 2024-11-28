# Existing imports
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

# Define namespaces
MOVIE_ONTOLOGY = Namespace("http://www.movieontology.org/2009/10/01/movieontology.owl#")
DBPEDIA_ONTOLOGY = Namespace("http://dbpedia.org/ontology/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create a Graph
g = Graph()

# Load the ontology
g.parse("movieontology.owl", format="xml")

# Add a sample movie
movie_uri_inception = MOVIE_ONTOLOGY.Inception
g.add((movie_uri_inception, RDF.type, MOVIE_ONTOLOGY.Movie))
g.add((movie_uri_inception, MOVIE_ONTOLOGY.title, Literal("Inception", datatype=XSD.string)))
g.add((movie_uri_inception, MOVIE_ONTOLOGY.releasedate, Literal("2010-07-16", datatype=XSD.date)))
g.add((movie_uri_inception, MOVIE_ONTOLOGY.imdbrating, Literal(8.8, datatype=XSD.double)))

# Add another movie
movie_uri_titanic = MOVIE_ONTOLOGY.Titanic
g.add((movie_uri_titanic, RDF.type, MOVIE_ONTOLOGY.Movie))
g.add((movie_uri_titanic, MOVIE_ONTOLOGY.title, Literal("Titanic", datatype=XSD.string)))
g.add((movie_uri_titanic, MOVIE_ONTOLOGY.releasedate, Literal("1997-12-19", datatype=XSD.date)))
g.add((movie_uri_titanic, MOVIE_ONTOLOGY.imdbrating, Literal(7.8, datatype=XSD.double)))

# Add a sample actor
actor_uri_leonardo = MOVIE_ONTOLOGY.Leonardo_DiCaprio
g.add((actor_uri_leonardo, RDF.type, DBPEDIA_ONTOLOGY.Actor))
g.add((actor_uri_leonardo, RDFS.label, Literal("Leonardo DiCaprio", datatype=XSD.string)))

# Relate the movies and the actors
g.add((movie_uri_inception, MOVIE_ONTOLOGY.hasActor, actor_uri_leonardo))
g.add((movie_uri_titanic, MOVIE_ONTOLOGY.hasActor, actor_uri_leonardo))

# Serialize the graph to a file
g.serialize("populated_ontology.ttl", format="turtle")

print("Ontology populated successfully.")