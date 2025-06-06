import os
from typing import List, Optional
from pydantic import BaseModel, Field
import json

from elasticsearch import Elasticsearch
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

isconnected=False
elasticsearch_url=os.getenv('ELASTICSEARCH_URL')
elasticsearch_index=os.getenv('ELASTICSEARCH_INDEX')


class ElasticSearchOperations():
    def search(self, query: str) -> list[any]| None:
        results = []
        try:
            query = json.loads(query) #<--important
            client = Elasticsearch(elasticsearch_url)
            
            resp = client.search(index=elasticsearch_index, query=query)
            # print("Got {} hits:".format(resp["hits"]["total"]["value"]))
            for hit in resp["hits"]["hits"]:
                results.append(hit)
            return results
        except Exception as e:
            print(f"An error running query {query} Error {e}")
            return results
        finally:
            client.close() 

