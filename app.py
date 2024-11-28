import streamlit as st
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

# Define namespaces
MOVIE_ONTOLOGY = Namespace("http://www.movieontology.org/2009/10/01/movieontology.owl#")
DBPEDIA_ONTOLOGY = Namespace("http://dbpedia.org/ontology/")

# Load the graph
g = Graph()
g.parse("populated_ontology.ttl", format="turtle")

# Function to display all movies
def display_movies():
    st.subheader("All Movies")
    query = """
    PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
    SELECT ?movie ?title
    WHERE {
        ?movie a movie:Movie .
        ?movie movie:title ?title .
    }
    """
    results = g.query(query)
    for row in results:
        st.write(f"Movie: {row.movie.split('#')[-1]}, Title: {row.title}")

# Function to add a new movie
def add_movie(title, release_date, genre, actor):
    movie_uri = URIRef(MOVIE_ONTOLOGY[title.replace(" ", "_")])
    g.add((movie_uri, RDF.type, MOVIE_ONTOLOGY.Movie))
    g.add((movie_uri, MOVIE_ONTOLOGY.title, Literal(title, datatype=XSD.string)))
    g.add((movie_uri, MOVIE_ONTOLOGY.releasedate, Literal(release_date, datatype=XSD.date)))
    g.add((movie_uri, MOVIE_ONTOLOGY.belongsToGenre, MOVIE_ONTOLOGY[genre.replace(" ", "_")]))
    g.add((movie_uri, MOVIE_ONTOLOGY.hasActor, URIRef(MOVIE_ONTOLOGY[actor.replace(" ", "_")])))
    g.serialize("populated_ontology.ttl", format="turtle")

# Function to remove a movie
def remove_movie(title):
    movie_uri = URIRef(MOVIE_ONTOLOGY[title.replace(" ", "_")])
    g.remove((movie_uri, None, None))  # Remove all triples related to this movie
    g.serialize("populated_ontology.ttl", format="turtle")

# Function to search for movies
def search_movies(search_term, search_by):
    st.subheader(f"Search Results for '{search_term}' by {search_by}")
    if search_by == "Title":
        query = f"""
        PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
        SELECT ?movie ?title
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:title ?title .
            FILTER(CONTAINS(LCASE(?title), LCASE("{search_term}")))
        }}
        """
    elif search_by == "Genre":
        query = f"""
        PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
        SELECT ?movie ?title
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:belongsToGenre movie:{search_term.replace(" ", "_")} .
            ?movie movie:title ?title .
        }}
        """
    elif search_by == "Actor":
        query = f"""
        PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
        SELECT ?movie ?title
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:hasActor movie:{search_term.replace(" ", "_")} .
            ?movie movie:title ?title .
        }}
        """
    elif search_by == "Release Date":
        query = f"""
        PREFIX movie: <http://www.movieontology.org/2009/10/01/movieontology.owl#>
        SELECT ?movie ?title
        WHERE {{
            ?movie a movie:Movie .
            ?movie movie:releasedate ?releaseDate .
            FILTER(?releaseDate = "{search_term}")
            ?movie movie:title ?title .
        }}
        """

    results = g.query(query)
    for row in results:
        st.write(f"Movie: {row.movie.split('#')[-1]}, Title: {row.title}")

# Streamlit UI
st.title("Movie Ontology Management")

# Add Movie Section
st.header("Add a New Movie")
with st.form(key='add_movie_form'):
    title = st.text_input("Title")
    release_date = st.date_input("Release Date")
    genre = st.text_input("Genre")
    actor = st.text_input("Actor")
    submit_button = st.form_submit_button("Add Movie")
    if submit_button:
        add_movie(title, release_date, genre, actor)
        st.success(f"Movie '{title}' added successfully!")

# Remove Movie Section
st.header("Remove a Movie")
remove_title = st.text_input("Title of Movie to Remove")
if st.button("Remove Movie"):
    remove_movie(remove_title)
    st.success(f"Movie '{remove_title}' removed successfully!")

# Search Movies Section
st.header("Search for Movies")
search_term = st.text_input("Search Term")
search_by = st.selectbox("Search By", ["Title", "Genre", "Actor", "Release Date"])
if st.button("Search"):
    search_movies(search_term, search_by)

# Display all movies
display_movies()