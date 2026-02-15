from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es=Elasticsearch(
        
        os.getenv("LINK"),
        api_key=os.getenv("API")
    

        )

index_name = "search_engine"

es.indices.create(
    index=index_name,
    ignore=400, 
    body={
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "content": {"type": "text"}
            }
        }
    }
)


