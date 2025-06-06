import os
from typing import List, Optional, Type
from langchain_core.callbacks import  CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, field_validator

from github import Github
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

from operations.elastic_search_operations import ElasticSearchOperations

elasticsearch_Operations=ElasticSearchOperations()

class ElasticsearchTools():
    class ElasticsearchSearchTool(BaseTool):
        name: str = "ElasticsearchSearchTool"
        description: str = """useful for when you need get items from an elasticsearch index.
        When querying ElasticSearch, you should use KQL (Kibana Query Language) to search for the data.
        Convert the input query to KQL format.
        The KQL query should be a JSON object that matches the Elasticsearch mapping.
        If you are not sure about the query, you can return an empty list
        Here is the elasticsearch mapping:
        {
        "mappings": {
            "python_log": {
            "properties": {
                "exc_info": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "exc_text": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "filename": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "funcName": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "host": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "host_ip": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "levelname": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "lineno": {
                "type": "long"
                },
                "message": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "module": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "msg": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "name": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "pathname": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "process": {
                "type": "long"
                },
                "processName": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "stack_info": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "taskName": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "thread": {
                "type": "long"
                },
                "threadName": {
                "type": "text",
                "fields": {
                    "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                    }
                }
                },
                "timestamp": {
                "type": "date"
                }
            }
            }
        }
        }
        
    The query string should be in the format of a JSON object.
    Here are some examples: 
    # Example 1:  Get all log entries with levelname 'Error'
    {'match': {'levelname': 'Error'}}
    """
        return_direct: bool = True
        
        class ElasticsearchSearchToolInputModel(BaseModel):
            query: str = Field(description="query")

             # Validation method to check parameter input from agent
            @field_validator("query")
            def validate_query_param(query):
                if not query:
                    raise ValueError("ElasticsearchSearchTool tool error: query parameter is empty")
                else:
                    return query
            
        args_schema: Optional[ArgsSchema] = ElasticsearchSearchToolInputModel

        
                
        def _run(self,query) -> str:
            logs=elasticsearch_Operations.search(query)
            return str(logs)


    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.ElasticsearchSearchTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools