from graph.neo4j_client import run_query

def create_constraints():
    run_query("CREATE CONSTRAINT paper_title IF NOT EXISTS FOR (p:Paper) REQUIRE p.title IS UNIQUE")
    run_query("CREATE CONSTRAINT author_name IF NOT EXISTS FOR (a:Author) REQUIRE a.name IS UNIQUE")
    run_query("CREATE CONSTRAINT source_name IF NOT EXISTS FOR (s:Source) REQUIRE s.name IS UNIQUE")