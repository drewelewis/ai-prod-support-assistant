import os
import requests
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv(override=True)

# ServiceNow Configuration
SERVICENOW_INSTANCE = os.getenv('SERVICENOW_INSTANCE')  # e.g., 'dev12345.service-now.com'
SERVICENOW_USERNAME = os.getenv('SERVICENOW_USERNAME')
SERVICENOW_PASSWORD = os.getenv('SERVICENOW_PASSWORD')
SERVICENOW_API_TOKEN = os.getenv('SERVICENOW_API_TOKEN')  # Optional: OAuth token

if not SERVICENOW_INSTANCE:
    raise ValueError("ServiceNow instance URL is not set in environment variables.")

if not (SERVICENOW_USERNAME and SERVICENOW_PASSWORD) and not SERVICENOW_API_TOKEN:
    raise ValueError("ServiceNow credentials (username/password or API token) are not set in environment variables.")


class ServiceNowOperations:
    """
    Operations class for ServiceNow Case API interactions.
    Supports creating, reading, updating, and querying cases in ServiceNow.
    
    API Reference: https://developer.servicenow.com/dev.do#!/reference/api/zurich/rest/case-api
    """
    
    def __init__(self, table_name: str = "incident"):
        """
        Initialize ServiceNow operations with authentication.
        
        Args:
            table_name: The ServiceNow table to use. Options:
                - "incident" (default) - Standard incident table, available in all instances
                - "sn_customerservice_case" - Customer Service case table (CSM plugin required)
        """
        self.base_url = f"https://{SERVICENOW_INSTANCE}/api/now"
        self.case_table = table_name
        
        # Set up authentication
        if SERVICENOW_API_TOKEN:
            self.headers = {
                "Authorization": f"Bearer {SERVICENOW_API_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            self.auth = None
        else:
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            self.auth = (SERVICENOW_USERNAME, SERVICENOW_PASSWORD)
    
    def create_case(self, 
                   short_description: str,
                   description: Optional[str] = None,
                   priority: Optional[str] = "3",
                   contact: Optional[str] = None,
                   account: Optional[str] = None,
                   category: Optional[str] = None,
                   additional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new case in ServiceNow.
        
        Args:
            short_description: Brief summary of the case
            description: Detailed description of the case
            priority: Priority level (1-5, where 1 is highest)
            contact: Contact sys_id or email
            account: Account sys_id
            category: Case category
            additional_fields: Dictionary of additional fields to set
            
        Returns:
            Dictionary containing the created case information
        """
        try:
            url = f"{self.base_url}/table/{self.case_table}"
            
            payload = {
                "short_description": short_description,
                "priority": priority
            }
            
            if description:
                payload["description"] = description
            if contact:
                payload["contact"] = contact
            if account:
                payload["account"] = account
            if category:
                payload["category"] = category
            if additional_fields:
                payload.update(additional_fields)
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json().get("result", {})
            return {
                "success": True,
                "case_number": result.get("number"),
                "sys_id": result.get("sys_id"),
                "state": result.get("state"),
                "priority": result.get("priority"),
                "short_description": result.get("short_description"),
                "url": f"https://{SERVICENOW_INSTANCE}/nav_to.do?uri={self.case_table}.do?sys_id={result.get('sys_id')}"
            }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with ServiceNowOperations.create_case: {e}")
            return {"success": False, "error": str(e)}
    
    def get_case(self, case_sys_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific case by sys_id.
        
        Args:
            case_sys_id: The sys_id of the case to retrieve
            
        Returns:
            Dictionary containing case information
        """
        try:
            url = f"{self.base_url}/table/{self.case_table}/{case_sys_id}"
            
            response = requests.get(
                url,
                headers=self.headers,
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json().get("result", {})
            return {
                "success": True,
                "case": result
            }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with ServiceNowOperations.get_case: {e}")
            return {"success": False, "error": str(e)}
    
    def get_case_by_number(self, case_number: str) -> Dict[str, Any]:
        """
        Retrieve a case by case number.
        
        Args:
            case_number: The case number (e.g., 'CS0001001')
            
        Returns:
            Dictionary containing case information
        """
        try:
            url = f"{self.base_url}/table/{self.case_table}"
            params = {
                "sysparm_query": f"number={case_number}",
                "sysparm_limit": 1
            }
            
            response = requests.get(
                url,
                headers=self.headers,
                auth=self.auth,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json().get("result", [])
            if results:
                return {
                    "success": True,
                    "case": results[0]
                }
            else:
                return {
                    "success": False,
                    "error": f"Case {case_number} not found"
                }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with ServiceNowOperations.get_case_by_number: {e}")
            return {"success": False, "error": str(e)}
    
    def update_case(self, 
                   case_sys_id: str,
                   updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing case.
        
        Args:
            case_sys_id: The sys_id of the case to update
            updates: Dictionary of fields to update
            
        Returns:
            Dictionary containing the updated case information
        """
        try:
            url = f"{self.base_url}/table/{self.case_table}/{case_sys_id}"
            
            response = requests.patch(
                url,
                json=updates,
                headers=self.headers,
                auth=self.auth,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json().get("result", {})
            return {
                "success": True,
                "case": result
            }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with ServiceNowOperations.update_case: {e}")
            return {"success": False, "error": str(e)}
    
    def query_cases(self,
                   query: Optional[str] = None,
                   limit: int = 100,
                   offset: int = 0,
                   order_by: Optional[str] = None,
                   fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Query cases with optional filters.
        
        Args:
            query: ServiceNow encoded query string (e.g., 'state=1^priority=1')
            limit: Maximum number of records to return
            offset: Starting record index
            order_by: Field to order by (prefix with ^ for descending)
            fields: List of specific fields to return
            
        Returns:
            Dictionary containing list of cases matching the query
        """
        try:
            url = f"{self.base_url}/table/{self.case_table}"
            
            params = {
                "sysparm_limit": limit,
                "sysparm_offset": offset
            }
            
            if query:
                params["sysparm_query"] = query
            if order_by:
                params["sysparm_orderby"] = order_by
            if fields:
                params["sysparm_fields"] = ",".join(fields)
            
            response = requests.get(
                url,
                headers=self.headers,
                auth=self.auth,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json().get("result", [])
            return {
                "success": True,
                "count": len(results),
                "cases": results
            }
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with ServiceNowOperations.query_cases: {e}")
            return {"success": False, "error": str(e)}
    
    def get_open_cases(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get all open cases (state not in resolved/closed states).
        
        Args:
            limit: Maximum number of cases to return
            
        Returns:
            Dictionary containing list of open cases
        """
        # ServiceNow case states: 1=Open, 2=Work in Progress, 3=Resolved, 4=Closed
        query = "state!=3^state!=4"
        return self.query_cases(query=query, limit=limit, order_by="^sys_updated_on")
    
    def get_high_priority_cases(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get high priority cases (priority 1 or 2).
        
        Args:
            limit: Maximum number of cases to return
            
        Returns:
            Dictionary containing list of high priority cases
        """
        query = "priority=1^ORpriority=2^state!=3^state!=4"
        return self.query_cases(query=query, limit=limit, order_by="priority")
    
    def add_case_comment(self, 
                        case_sys_id: str,
                        comment: str,
                        comment_type: str = "work_notes") -> Dict[str, Any]:
        """
        Add a comment or work note to a case.
        
        Args:
            case_sys_id: The sys_id of the case
            comment: The comment text to add
            comment_type: Type of comment ('work_notes' for internal, 'comments' for customer-visible)
            
        Returns:
            Dictionary containing success status
        """
        try:
            updates = {comment_type: comment}
            return self.update_case(case_sys_id, updates)
        except Exception as e:
            print(f"An error occurred with ServiceNowOperations.add_case_comment: {e}")
            return {"success": False, "error": str(e)}
    
    def close_case(self,
                  case_sys_id: str,
                  resolution_notes: Optional[str] = None,
                  close_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Close a case.
        
        Args:
            case_sys_id: The sys_id of the case to close
            resolution_notes: Notes describing the resolution
            close_code: Close code/reason
            
        Returns:
            Dictionary containing the closed case information
        """
        try:
            updates = {
                "state": "3",  # Resolved state
                "resolved_at": "javascript:gs.nowDateTime()"
            }
            
            if resolution_notes:
                updates["resolution_notes"] = resolution_notes
            if close_code:
                updates["close_code"] = close_code
            
            return self.update_case(case_sys_id, updates)
        except Exception as e:
            print(f"An error occurred with ServiceNowOperations.close_case: {e}")
            return {"success": False, "error": str(e)}
    
    def search_cases_by_text(self, 
                            search_text: str,
                            search_fields: Optional[List[str]] = None,
                            limit: int = 50) -> Dict[str, Any]:
        """
        Search cases by text across specified fields.
        
        Args:
            search_text: Text to search for
            search_fields: List of fields to search in (default: short_description, description)
            limit: Maximum number of results
            
        Returns:
            Dictionary containing matching cases
        """
        try:
            if not search_fields:
                search_fields = ["short_description", "description"]
            
            # Build query with OR conditions
            query_parts = [f"{field}LIKE{search_text}" for field in search_fields]
            query = "^OR".join(query_parts)
            
            return self.query_cases(query=query, limit=limit, order_by="^sys_updated_on")
        except Exception as e:
            print(f"An error occurred with ServiceNowOperations.search_cases_by_text: {e}")
            return {"success": False, "error": str(e)}
    
    def get_cases_by_contact(self, contact_sys_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get all cases for a specific contact.
        
        Args:
            contact_sys_id: The sys_id of the contact
            limit: Maximum number of cases to return
            
        Returns:
            Dictionary containing list of cases
        """
        query = f"contact={contact_sys_id}"
        return self.query_cases(query=query, limit=limit, order_by="^sys_created_on")
    
    def get_cases_by_account(self, account_sys_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get all cases for a specific account.
        
        Args:
            account_sys_id: The sys_id of the account
            limit: Maximum number of cases to return
            
        Returns:
            Dictionary containing list of cases
        """
        query = f"account={account_sys_id}"
        return self.query_cases(query=query, limit=limit, order_by="^sys_created_on")
    
    def assign_case(self, 
                   case_sys_id: str,
                   assigned_to: str,
                   assignment_group: Optional[str] = None) -> Dict[str, Any]:
        """
        Assign a case to a user or group.
        
        Args:
            case_sys_id: The sys_id of the case
            assigned_to: sys_id of the user to assign to
            assignment_group: Optional sys_id of the assignment group
            
        Returns:
            Dictionary containing the updated case information
        """
        try:
            updates = {"assigned_to": assigned_to}
            
            if assignment_group:
                updates["assignment_group"] = assignment_group
            
            return self.update_case(case_sys_id, updates)
        except Exception as e:
            print(f"An error occurred with ServiceNowOperations.assign_case: {e}")
            return {"success": False, "error": str(e)}
