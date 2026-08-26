from graph.neo4j_client import run_query

def get_papers_by_source(source_name):
    return run_query(
        """
        MATCH (p:Paper)-[:FROM_SOURCE]->(s:Source {name: $source})
        RETURN p.title AS title
        """,
        {"source": source_name}
    )

def get_authors_of_paper(title):
    return run_query(
        """
        MATCH (a:Author)-[:AUTHORED]->(p:Paper {title: $title})
        RETURN a.name AS author
        """,
        {"title": title}
    )

