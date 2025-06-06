import os
from elasticsearch import Elasticsearch

doc_type = "python_log"
# index = "contosobank-logs-2025.05.21"
elasticsearch_url=os.getenv('ELASTICSEARCH_URL')
elasticsearch_index=os.getenv('ELASTICSEARCH_INDEX')


def main():
    results = []
    query={
            "match": {
                "levelname": "Error"
            }
        }
        
    try:
        client = Elasticsearch(elasticsearch_url)
        
        resp=client.search(index=elasticsearch_index, query=query)
        for hit in resp["hits"]["hits"]:
            results.append(hit)
        return results
    except Exception as e:
        print(f"An error running query {query} Error {e}")
        return results
    finally:
        client.close() 

if __name__ == "__main__":
    results = main()
    for result in results:
        print(result)

# https://stackoverflow.com/questions/65785913/how-to-automate-the-creation-of-elasticsearch-index-patterns-for-all-days