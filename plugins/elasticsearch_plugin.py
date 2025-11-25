"""
Elasticsearch Plugin for Semantic Kernel
Provides functions to search and query application logs stored in Elasticsearch
"""

from semantic_kernel.functions import kernel_function
from operations.elastic_search_operations import ElasticSearchOperations
import json

elasticsearch_operations = ElasticSearchOperations()


class ElasticsearchPlugin:
    """
    A plugin for querying Elasticsearch logs.
    Provides functions to search application logs using KQL (Kibana Query Language).
    """

    @kernel_function(
        name="search_logs",
        description="""Search for logs in Elasticsearch using KQL (Kibana Query Language).
        
        The Elasticsearch index contains Python application logs with the following fields:
        - levelname: Log level (ERROR, INFO, WARNING, DEBUG, etc.)
        - message: The log message content
        - host: Server hostname where the log originated
        - host_ip: Server IP address
        - timestamp: When the log was created
        - filename: Source file that generated the log
        - funcName: Function name where log originated
        - lineno: Line number in source code
        - module: Python module name
        - pathname: Full file path
        - process: Process ID
        - processName: Process name
        - exc_info: Exception information
        - exc_text: Exception text details
        
        The query should be a JSON string in Elasticsearch query format.
        
        Examples:
        - To find all ERROR logs: {"match": {"levelname": "ERROR"}}
        - To find logs with specific message: {"match": {"message": "database timeout"}}
        - To find logs from specific host: {"match": {"host": "server-01"}}
        - To find logs with multiple conditions: {"bool": {"must": [{"match": {"levelname": "ERROR"}}, {"match": {"host": "server-01"}}]}}
        """
    )
    def search_logs(self, query: str) -> str:
        """
        Search Elasticsearch logs using a query.
        
        Args:
            query: The Elasticsearch query in JSON format
            
        Returns:
            A string representation of the search results
        """
        try:
            # Validate that query is valid JSON
            try:
                json.loads(query)
            except json.JSONDecodeError:
                return f"Invalid JSON query format. Please provide a valid JSON query string."
            
            results = elasticsearch_operations.search(query)
            
            if not results:
                return "No logs found matching the query."
            
            # Format results for display
            output = [f"Found {len(results)} log entries:\n"]
            
            for idx, hit in enumerate(results[:10], 1):  # Limit to first 10 for readability
                source = hit.get("_source", {})
                output.append(f"\n--- Log Entry {idx} ---")
                output.append(f"Timestamp: {source.get('timestamp', 'N/A')}")
                output.append(f"Level: {source.get('levelname', 'N/A')}")
                output.append(f"Message: {source.get('message', 'N/A')}")
                output.append(f"Host: {source.get('host', 'N/A')}")
                output.append(f"Module: {source.get('module', 'N/A')}")
                output.append(f"Function: {source.get('funcName', 'N/A')}")
                
                if source.get('exc_text'):
                    output.append(f"Exception: {source.get('exc_text', 'N/A')}")
            
            if len(results) > 10:
                output.append(f"\n... and {len(results) - 10} more entries")
            
            return "\n".join(output)
            
        except Exception as e:
            return f"Error searching Elasticsearch: {str(e)}"
