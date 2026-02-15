from elasticsearch import Elasticsearch
from es import es


query =input("> ")
results = es.search(index="search_engine", query={"match": {"content": query}})


for hit in results['hits']['hits']:
    print("LINK > ",hit['_source']['url'], "| score:", hit['_score'])
