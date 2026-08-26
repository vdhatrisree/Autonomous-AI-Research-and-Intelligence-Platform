from graph.neo4j_client import run_query

def add_document(doc):
    run_query(
        "MERGE (p:Paper {title: $title}) SET p.summary = $summary, p.url = $url",
        {"title": doc.title, "summary": doc.summary[:500], "url": doc.url}
    )
    run_query(
        "MERGE (s:Source {name: $source})",
        {"source": doc.source}
    )
    run_query(
        """
        MATCH (p:Paper {title: $title}), (s:Source {name: $source})
        MERGE (p)-[:FROM_SOURCE]->(s)
        """,
        {"title": doc.title, "source": doc.source}
    )

def add_authors(doc):
    for author_name in doc.authors:
        run_query(
            "MERGE (a:Author {name: $name})",
            {"name": author_name}
        )
        run_query(
            """
            MATCH (p:Paper {title: $title}), (a:Author {name: $name})
            MERGE (a)-[:AUTHORED]->(p)
            """,
            {"title": doc.title, "name": author_name}
        )

def add_dataset_usage(doc, dataset_names):
    for name in dataset_names:
        run_query(
            "MERGE (d:Dataset {name: $name})",
            {"name": name}
        )
        run_query(
            """
            MATCH (p:Paper {title: $title}), (d:Dataset {name: $name})
            MERGE (p)-[:USES_DATASET]->(d)
            """,
            {"title": doc.title, "name": name}
        )

def add_citations(doc, cited_arxiv_ids):
    for arxiv_id in cited_arxiv_ids:
        run_query(
            "MERGE (p2:Paper {arxiv_id: $arxiv_id})",
            {"arxiv_id": arxiv_id}
        )
        run_query(
            """
            MATCH (p1:Paper {title: $title}), (p2:Paper {arxiv_id: $arxiv_id})
            MERGE (p1)-[:CITES]->(p2)
            """,
            {"title": doc.title, "arxiv_id": arxiv_id}
        )