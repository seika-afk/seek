from es import es, index_name
import json



with open("pages.json") as f :
    pages=json.load(f)
#pages will be array of dict , containing two components->>>>>> url and content , 
for i, page in enumerate(pages):
    es.index(index=index_name, id=i, document=page)
    print(f"successful{i}")
