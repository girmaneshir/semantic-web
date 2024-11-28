from rdflib import Graph

# Load the populated graph
g = Graph()
g.parse("populated_ontology.ttl", format="turtle")

# Function to get a more readable URI
def get_readable_uri(uri):
    return uri.split('#')[-1]

# Query 1: Find all movies and their titles
query1 = """
PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
SELECT ?movie ?title
WHERE {
    ?movie a movie:Movie .
    ?movie movie:title ?title .
}
"""

# Query 2: Find all actors and the movies they acted in
query2 = """
PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
PREFIX dbpedia: <http://dbpedia.org/ontology/>
SELECT ?actor ?movie ?title
WHERE {
    ?actor a dbpedia:Actor .
    ?movie movie:hasActor ?actor .
    ?movie movie:title ?title .
}
"""

# Query 3: Find movies released after a specific date
query3 = """
PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
SELECT ?movie ?title
WHERE {
    ?movie a movie:Movie .
    ?movie movie:title ?title .
    ?movie movie:releasedate ?releaseDate .
    FILTER(?releaseDate > "2010-01-01"^^xsd:date)
}
"""

# Execute and print results for each query
print("Query 1: All Movies and Titles")
results1 = g.query(query1)
for row in results1:
    print(f"Movie: {get_readable_uri(row.movie)}, Title: {row.title}")

print("\nQuery 2: All Actors and Their Movies")
results2 = g.query(query2)
for row in results2:
    print(f"Actor: {get_readable_uri(row.actor)}, Movie: {get_readable_uri(row.movie)}, Title: {row.title}")

print("\nQuery 3: Movies Released After 2010-01-01")
results3 = g.query(query3)
for row in results3:
    print(f"Movie: {get_readable_uri(row.movie)}, Title: {row.title}")