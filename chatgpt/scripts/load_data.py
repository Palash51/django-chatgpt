from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import pandas as pd

def create_index():
    mappings = {
        "properties": {
            "title": {"type": "text", "analyzer": "english"},
            "ethnicity": {"type": "text", "analyzer": "standard"},
            "director": {"type": "text", "analyzer": "standard"},
            "cast": {"type": "text", "analyzer": "standard"},
            "genre": {"type": "text", "analyzer": "standard"},
            "plot": {"type": "text", "analyzer": "english"},
            "year": {"type": "integer"},
            "wiki_page": {"type": "keyword"}
            }
        }
    es = Elasticsearch("http://localhost:9200")
    es.indices.create(index="movies", mappings=mappings)


def prepare_data():
    df = (
        pd.read_csv("/home/palash/Documents/python-learnings/django-celery/chatgpt/scripts/wiki_movie_plots_deduped.csv")
          .dropna()
          .sample(5000, random_state=42)
          .reset_index()
        )
    es = Elasticsearch("http://localhost:9200")
    
    bulk_data = []
    for i,row in df.iterrows():
        bulk_data.append(
        {
            "_index": "movies",
            "_id": i,
            "_source": {        
                "title": row["Title"],
                "ethnicity": row["Origin/Ethnicity"],
                "director": row["Director"],
                "cast": row["Cast"],
                "genre": row["Genre"],
                "plot": row["Plot"],
                "year": row["Release Year"],
                "wiki_page": row["Wiki Page"],
            }
        }
    )
    
    bulk(es, bulk_data)


def verify_data():
    """"""
    es = Elasticsearch("http://localhost:9200")
    es.indices.refresh(index="movies")
    docs = es.cat.count(index="movies", format="json")
    print(f"docs count ########{docs}")

if __name__ == "__main__":
    create_index()
    prepare_data()
    verify_data()