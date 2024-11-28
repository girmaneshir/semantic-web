# Movie Ontology Project

This project demonstrates the concepts of taxonomy, ontology, and knowledge graphs using a movie ontology.

## File Structure

- `local_ontology.owl`: Predefined ontology file for movies.
- `populate.py`: Populates the ontology with instances (movies, actors, directors).
- `query.py`: Queries the ontology to retrieve information.

## How to Run

1. Install required libraries:
   pip install owlready2 rdflib

2. If you don't have local_ontology.owl, create it by running the ontology creation script:
    python ontology.py

3. Populate the ontology with instances by running:
    python populate.py

4. Query the populated ontology:
   python query.py

## Output Example
Movies:
Movie: Titanic
Actors in Titanic:
Actor: Leonardo DiCaprio
Actor: Kate Winslet
Director of Titanic:
Director: James Cameron