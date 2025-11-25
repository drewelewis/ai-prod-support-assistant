"""
ServiceNow Plugin for Semantic Kernel
Provides functions to interact with ServiceNow Case API
"""

from semantic_kernel.functions import kernel_function
from operations.servicenow_operations import ServiceNowOperations
import json

# Use 'incident' table which is available in all ServiceNow instances
# Change to 'sn_customerservice_case' if you have Customer Service Management plugin
servicenow_operations = ServiceNowOperations(table_name="incident")


class ServiceNowPlugin:
    """
    A plugin for interacting with ServiceNow cases.
    Provides functions to create, read, update, query, and manage ServiceNow cases.
    """

    @kernel_function(
        name="create_case",
        description="Create a new ServiceNow case. Use this when a user wants to log a new support case or issue."
    )
    def create_case(
        self, 
        short_description: str,
        description: str = "",
        priority: str = "3"
    ) -> str:
        """
        Create a new ServiceNow case.
        
        Args:
            short_description: Brief summary of the issue
            description: Detailed description of the case
            priority: Priority level (1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning)
            
        Returns:
            A message with the created case details
        """
        try:
            result = servicenow_operations.create_case(
                short_description=short_description,
                description=description,
                priority=priority
            )
            
            if result.get("success"):
                return (f"Case created successfully!\n"
                       f"Case Number: {result.get('case_number')}\n"
                       f"Sys ID: {result.get('sys_id')}\n"
                       f"Priority: {result.get('priority')}\n"
                       f"URL: {result.get('url')}")
            else:
                return f"Failed to create case: {result.get('error')}"
        except Exception as e:
            return f"Error creating case: {str(e)}"

    @kernel_function(
        name="get_case",
        description="Retrieve details of a specific ServiceNow case by case number (e.g., 'CS0001001') or sys_id."
    )
    def get_case(self, case_number: str = "", case_sys_id: str = "") -> str:
        """
        Get details of a ServiceNow case.
        
        Args:
            case_number: The case number (e.g., 'CS0001001')
            case_sys_id: The case sys_id
            
        Returns:
            A message with the case details
        """
        try:
            if case_sys_id:
                result = servicenow_operations.get_case(case_sys_id)
            elif case_number:
                result = servicenow_operations.get_case_by_number(case_number)
            else:
                return "Please provide either a case_number or case_sys_id"
            
            if result.get("success"):
                case = result.get("case", {})
                return (f"Case Details:\n"
                       f"Number: {case.get('number')}\n"
                       f"Short Description: {case.get('short_description')}\n"
                       f"Description: {case.get('description')}\n"
                       f"State: {case.get('state')}\n"
                       f"Priority: {case.get('priority')}\n"
                       f"Created: {case.get('sys_created_on')}\n"
                       f"Updated: {case.get('sys_updated_on')}")
            else:
                return f"Failed to retrieve case: {result.get('error')}"
        except Exception as e:
            return f"Error retrieving case: {str(e)}"

    @kernel_function(
        name="query_open_cases",
        description="Get all open ServiceNow cases. Use this to see what cases are currently being worked on."
    )
    def query_open_cases(self, limit: str = "50") -> str:
        """
        Get all open ServiceNow cases.
        
        Args:
            limit: Maximum number of cases to return (default: 50)
            
        Returns:
            A message with the list of open cases
        """
        try:
            result = servicenow_operations.get_open_cases(limit=int(limit))
            
            if result.get("success"):
                cases = result.get("cases", [])
                count = result.get("count", 0)
                
                if count == 0:
                    return "No open cases found."
                
                output = [f"Found {count} open case(s):\n"]
                for case in cases[:10]:  # Limit display to 10
                    output.append(
                        f"\n- Case {case.get('number')}: {case.get('short_description')}\n"
                        f"  Priority: {case.get('priority')}, State: {case.get('state')}"
                    )
                
                if count > 10:
                    output.append(f"\n... and {count - 10} more cases")
                
                return "".join(output)
            else:
                return f"Failed to query cases: {result.get('error')}"
        except Exception as e:
            return f"Error querying cases: {str(e)}"

    @kernel_function(
        name="query_high_priority_cases",
        description="Get all high priority ServiceNow cases (priority 1 or 2). Use this to see urgent issues that need attention."
    )
    def query_high_priority_cases(self, limit: str = "50") -> str:
        """
        Get all high priority ServiceNow cases.
        
        Args:
            limit: Maximum number of cases to return (default: 50)
            
        Returns:
            A message with the list of high priority cases
        """
        try:
            result = servicenow_operations.get_high_priority_cases(limit=int(limit))
            
            if result.get("success"):
                cases = result.get("cases", [])
                count = result.get("count", 0)
                
                if count == 0:
                    return "No high priority cases found."
                
                output = [f"Found {count} high priority case(s):\n"]
                for case in cases[:10]:  # Limit display to 10
                    output.append(
                        f"\n- Case {case.get('number')}: {case.get('short_description')}\n"
                        f"  Priority: {case.get('priority')}, State: {case.get('state')}"
                    )
                
                if count > 10:
                    output.append(f"\n... and {count - 10} more cases")
                
                return "".join(output)
            else:
                return f"Failed to query cases: {result.get('error')}"
        except Exception as e:
            return f"Error querying cases: {str(e)}"

    @kernel_function(
        name="add_case_comment",
        description="Add a comment or work note to a ServiceNow case. Use 'work_notes' for internal comments or 'comments' for customer-visible comments."
    )
    def add_case_comment(
        self,
        case_sys_id: str,
        comment: str,
        comment_type: str = "work_notes"
    ) -> str:
        """
        Add a comment to a ServiceNow case.
        
        Args:
            case_sys_id: The sys_id of the case
            comment: The comment text to add
            comment_type: Type of comment ('work_notes' or 'comments')
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.add_case_comment(
                case_sys_id=case_sys_id,
                comment=comment,
                comment_type=comment_type
            )
            
            if result.get("success"):
                return "Comment added successfully to case."
            else:
                return f"Failed to add comment: {result.get('error')}"
        except Exception as e:
            return f"Error adding comment: {str(e)}"

    @kernel_function(
        name="close_case",
        description="Close a ServiceNow case. Use this when an issue has been resolved."
    )
    def close_case(
        self,
        case_sys_id: str,
        resolution_notes: str = ""
    ) -> str:
        """
        Close a ServiceNow case.
        
        Args:
            case_sys_id: The sys_id of the case to close
            resolution_notes: Notes describing the resolution
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.close_case(
                case_sys_id=case_sys_id,
                resolution_notes=resolution_notes
            )
            
            if result.get("success"):
                case = result.get("case", {})
                return f"Case {case.get('number')} closed successfully!"
            else:
                return f"Failed to close case: {result.get('error')}"
        except Exception as e:
            return f"Error closing case: {str(e)}"

    @kernel_function(
        name="search_cases",
        description="Search ServiceNow cases by text. Searches in short_description and description fields."
    )
    def search_cases(self, search_text: str, limit: str = "50") -> str:
        """
        Search ServiceNow cases by text.
        
        Args:
            search_text: Text to search for
            limit: Maximum number of results (default: 50)
            
        Returns:
            A message with the search results
        """
        try:
            result = servicenow_operations.search_cases_by_text(
                search_text=search_text,
                limit=int(limit)
            )
            
            if result.get("success"):
                cases = result.get("cases", [])
                count = result.get("count", 0)
                
                if count == 0:
                    return f"No cases found matching '{search_text}'."
                
                output = [f"Found {count} case(s) matching '{search_text}':\n"]
                for case in cases[:10]:  # Limit display to 10
                    output.append(
                        f"\n- Case {case.get('number')}: {case.get('short_description')}\n"
                        f"  Priority: {case.get('priority')}, State: {case.get('state')}"
                    )
                
                if count > 10:
                    output.append(f"\n... and {count - 10} more cases")
                
                return "".join(output)
            else:
                return f"Failed to search cases: {result.get('error')}"
        except Exception as e:
            return f"Error searching cases: {str(e)}"
