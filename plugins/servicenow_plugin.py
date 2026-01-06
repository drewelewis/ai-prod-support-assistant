"""
ServiceNow Plugin for Semantic Kernel
Provides functions to interact with ServiceNow Incident API for internal IT support
"""

from semantic_kernel.functions import kernel_function
from operations.servicenow_operations import ServiceNowOperations
import json

# Use 'incident' table which is available in all ServiceNow instances
servicenow_operations = ServiceNowOperations(table_name="incident")


class ServiceNowPlugin:
    """
    A plugin for interacting with ServiceNow incidents.
    Provides functions to create, read, update, query, and manage ServiceNow incidents for internal IT support.
    """

    @kernel_function(
        name="list_servicenow_functions",
        description="List all available ServiceNow incident functions for debugging. Use this to see what incident functions are available."
    )
    def list_servicenow_functions(self) -> str:
        """
        List all available ServiceNow incident functions.
        
        Returns:
            A message with all available functions
        """
        functions = [
            "INCIDENT FUNCTIONS (Internal IT Support):",
            "- create_incident: Create a new IT incident",
            "- get_incident: Get incident details by number or sys_id",
            "- query_open_incidents: Get open incidents WITH PAGING (page_number, page_size)",
            "- query_high_priority_incidents: Get high priority incidents WITH PAGING",
            "- add_incident_comment: Add comment to incident", 
            "- resolve_incident: Resolve an incident",
            "- close_incident: Close an incident",
            "- assign_incident: Assign incident to technician",
            "- search_incidents: Search incidents by text",
            "",
            "PAGING DEFAULTS:",
            "- Default page size: 20",
            "- Use page_number='1' for first page, page_number='2' for second page, etc.",
            "- Use page_size='20' or specify different size"
        ]
        return "\n".join(functions)

    @kernel_function(
        name="test_servicenow_connection",
        description="Test the ServiceNow connection and return basic info for debugging."
    )
    def test_servicenow_connection(self) -> str:
        """
        Test ServiceNow connection and return basic information.
        
        Returns:
            A message with connection test results
        """
        try:
            # Test with a simple query - get just 1 incident
            result = servicenow_operations.query_incidents(limit=1)
            
            if result.get("success"):
                incidents = result.get("incidents", [])
                if incidents:
                    incident = incidents[0]
                    return (f"✅ ServiceNow Connection Test: SUCCESS\n"
                           f"Sample incident: {incident.get('number')} - {incident.get('short_description')}\n"
                           f"Found {len(incidents)} incident(s) in test query")
                else:
                    return "✅ ServiceNow Connection: SUCCESS (but no incidents found)"
            else:
                return f"❌ ServiceNow Connection Test: FAILED\nError: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"❌ ServiceNow Connection Test: ERROR\nDetails: {str(e)} | Type: {type(e).__name__}"

    # Incident management functions for internal IT support
    
    @kernel_function(
        name="create_incident",
        description="Create a new ServiceNow incident for internal IT support. Use this when internal users report IT issues or system problems."
    )
    def create_incident(
        self, 
        short_description: str,
        description: str = "",
        priority: str = "3",
        urgency: str = "3",
        impact: str = "3",
        caller_id: str = "",
        assignment_group: str = "",
        category: str = ""
    ) -> str:
        """
        Create a new ServiceNow incident for internal users.
        
        Args:
            short_description: Brief summary of the IT incident
            description: Detailed description of the incident
            priority: Priority level (1=Critical, 2=High, 3=Moderate, 4=Low, 5=Planning)
            urgency: How quickly the incident needs to be resolved (1=High, 2=Medium, 3=Low)
            impact: How many users/services are affected (1=High, 2=Medium, 3=Low)
            caller_id: The sys_id of the person reporting the incident
            assignment_group: The sys_id of the IT group to assign to
            category: Incident category (e.g., 'Hardware', 'Software', 'Network')
            
        Returns:
            A message with the created incident details
        """
        try:
            result = servicenow_operations.create_incident(
                short_description=short_description,
                description=description,
                priority=priority,
                urgency=urgency,
                impact=impact,
                caller_id=caller_id if caller_id else None,
                assignment_group=assignment_group if assignment_group else None,
                category=category if category else None
            )
            
            if result.get("success"):
                return (f"Incident created successfully!\n"
                       f"Incident Number: {result.get('incident_number')}\n"
                       f"Sys ID: {result.get('sys_id')}\n"
                       f"Priority: {result.get('priority')}\n"
                       f"Urgency: {result.get('urgency')}\n"
                       f"Impact: {result.get('impact')}\n"
                       f"URL: {result.get('url')}")
            else:
                return f"Failed to create incident: {result.get('error')}"
        except Exception as e:
            return f"Error creating incident: {str(e)}"

    @kernel_function(
        name="get_incident",
        description="Retrieve details of a specific ServiceNow incident by incident number (e.g., 'INC0001001') or sys_id."
    )
    def get_incident(self, incident_number: str = "", incident_sys_id: str = "") -> str:
        """
        Get details of a ServiceNow incident.
        
        Args:
            incident_number: The incident number (e.g., 'INC0001001')
            incident_sys_id: The incident sys_id
            
        Returns:
            A message with the incident details
        """
        try:
            if incident_sys_id:
                result = servicenow_operations.get_incident(incident_sys_id)
            elif incident_number:
                result = servicenow_operations.get_incident_by_number(incident_number)
            else:
                return "Please provide either an incident_number or incident_sys_id"
            
            if result.get("success"):
                incident = result.get("incident", {})
                return (f"Incident Details:\n"
                       f"Number: {incident.get('number')}\n"
                       f"Short Description: {incident.get('short_description')}\n"
                       f"Description: {incident.get('description')}\n"
                       f"State: {incident.get('state')}\n"
                       f"Priority: {incident.get('priority')}\n"
                       f"Urgency: {incident.get('urgency')}\n"
                       f"Impact: {incident.get('impact')}\n"
                       f"Caller: {incident.get('caller_id')}\n"
                       f"Assigned To: {incident.get('assigned_to')}\n"
                       f"Assignment Group: {incident.get('assignment_group')}\n"
                       f"Category: {incident.get('category')}\n"
                       f"Created: {incident.get('sys_created_on')}\n"
                       f"Updated: {incident.get('sys_updated_on')}")
            else:
                return f"Failed to retrieve incident: {result.get('error')}"
        except Exception as e:
            return f"Error retrieving incident: {str(e)}"

    @kernel_function(
        name="query_open_incidents",
        description="Get all open ServiceNow incidents with paging support. Use this to see what IT incidents are currently being worked on by internal teams."
    )
    def query_open_incidents(self, page_number: str = "1", page_size: str = "20") -> str:
        """
        Get all open ServiceNow incidents with paging.
        
        Args:
            page_number: Page number to retrieve (default: 1)
            page_size: Number of incidents per page (default: 20)
            
        Returns:
            A message with the list of open incidents for the specified page
        """
        try:
            page_num = int(page_number)
            page_sz = int(page_size)
            offset = (page_num - 1) * page_sz
            
            # Query open incidents (state != 6 Resolved, != 7 Closed)
            result = servicenow_operations.query_incidents(
                query="state!=6^state!=7",
                limit=page_sz,
                offset=offset,
                order_by="^sys_updated_on"
            )
            
            if result.get("success"):
                incidents = result.get("incidents", [])
                count = result.get("count", 0)
                has_more = result.get("has_more", False)
                
                if count == 0:
                    return "No open incidents found."
                
                start_record = offset + 1
                end_record = offset + count
                output = [f"Open Incidents - Page {page_num} (showing {start_record}-{end_record}):\n"]
                
                for incident in incidents:
                    output.append(
                        f"\n- Incident {incident.get('number')}: {incident.get('short_description')}\n"
                        f"  Priority: {incident.get('priority')}, Urgency: {incident.get('urgency')}, "
                        f"Impact: {incident.get('impact')}, State: {incident.get('state')}"
                    )
                
                # Show next page guidance if there are more records
                if has_more:
                    output.append(f"\n\nMore incidents available. Use query_open_incidents with page_number='{page_num + 1}' to continue.")
                
                return "".join(output)
            else:
                return f"Failed to query open incidents: {result.get('error', 'Unknown error')}"
        except ValueError as ve:
            return f"Invalid page parameters for open incidents: {str(ve)}"
        except Exception as e:
            return f"Error querying open incidents - Details: {str(e)} | Type: {type(e).__name__}"

    @kernel_function(
        name="query_high_priority_incidents",
        description="Get all high priority ServiceNow incidents (priority 1 or 2) with paging support. Use this to see urgent IT issues that need immediate attention."
    )
    def query_high_priority_incidents(self, page_number: str = "1", page_size: str = "20") -> str:
        """
        Get all high priority ServiceNow incidents with paging.
        
        Args:
            page_number: Page number to retrieve (default: 1)
            page_size: Number of incidents per page (default: 20)
            
        Returns:
            A message with the list of high priority incidents for the specified page
        """
        try:
            page_num = int(page_number)
            page_sz = int(page_size)
            offset = (page_num - 1) * page_sz
            
            result = servicenow_operations.query_incidents(
                query="priority=1^ORpriority=2",
                limit=page_sz,
                offset=offset,
                order_by="^sys_updated_on"
            )
            
            if result.get("success"):
                incidents = result.get("incidents", [])
                count = result.get("count", 0)
                has_more = result.get("has_more", False)
                
                if count == 0:
                    return "No high priority incidents found."
                
                start_record = offset + 1
                end_record = offset + count
                output = [f"High Priority Incidents - Page {page_num} (showing {start_record}-{end_record}):\n"]
                
                for incident in incidents:
                    output.append(
                        f"\n- Incident {incident.get('number')}: {incident.get('short_description')}\n"
                        f"  Priority: {incident.get('priority')}, Urgency: {incident.get('urgency')}, "
                        f"Impact: {incident.get('impact')}, State: {incident.get('state')}"
                    )
                
                # Show next page guidance if there are more records
                if has_more:
                    output.append(f"\n\nMore high priority incidents available. Use query_high_priority_incidents with page_number='{page_num + 1}' to continue.")
                
                return "".join(output)
            else:
                return f"Failed to query high priority incidents: {result.get('error', 'Unknown error')}"
        except ValueError as ve:
            return f"Invalid page parameters for high priority incidents: {str(ve)}"
        except Exception as e:
            return f"Error querying high priority incidents - Details: {str(e)} | Type: {type(e).__name__}"

    @kernel_function(
        name="add_incident_comment",
        description="Add a comment or work note to a ServiceNow incident. Use 'work_notes' for internal IT comments or 'comments' for user-visible comments."
    )
    def add_incident_comment(
        self,
        incident_sys_id: str,
        comment: str,
        comment_type: str = "work_notes"
    ) -> str:
        """
        Add a comment to a ServiceNow incident.
        
        Args:
            incident_sys_id: The sys_id of the incident
            comment: The comment text to add
            comment_type: Type of comment ('work_notes' or 'comments')
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.add_incident_comment(
                incident_sys_id=incident_sys_id,
                comment=comment,
                comment_type=comment_type
            )
            
            if result.get("success"):
                return "Comment added successfully to incident."
            else:
                return f"Failed to add comment: {result.get('error')}"
        except Exception as e:
            return f"Error adding comment: {str(e)}"

    @kernel_function(
        name="resolve_incident",
        description="Resolve a ServiceNow incident. Use this when an IT issue has been fixed but needs user confirmation before closing."
    )
    def resolve_incident(
        self,
        incident_sys_id: str,
        resolution_notes: str = "",
        resolution_code: str = ""
    ) -> str:
        """
        Resolve a ServiceNow incident.
        
        Args:
            incident_sys_id: The sys_id of the incident to resolve
            resolution_notes: Notes describing how the issue was resolved
            resolution_code: Resolution code/category
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.resolve_incident(
                incident_sys_id=incident_sys_id,
                resolution_notes=resolution_notes if resolution_notes else None,
                resolution_code=resolution_code if resolution_code else None
            )
            
            if result.get("success"):
                incident = result.get("incident", {})
                return f"Incident {incident.get('number')} resolved successfully!"
            else:
                return f"Failed to resolve incident: {result.get('error')}"
        except Exception as e:
            return f"Error resolving incident: {str(e)}"

    @kernel_function(
        name="close_incident",
        description="Close a ServiceNow incident. Use this when an IT issue has been completely resolved and confirmed by the user."
    )
    def close_incident(
        self,
        incident_sys_id: str,
        close_notes: str = "",
        close_code: str = ""
    ) -> str:
        """
        Close a ServiceNow incident.
        
        Args:
            incident_sys_id: The sys_id of the incident to close
            close_notes: Notes describing the closure
            close_code: Close code/reason
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.close_incident(
                incident_sys_id=incident_sys_id,
                close_notes=close_notes if close_notes else None,
                close_code=close_code if close_code else None
            )
            
            if result.get("success"):
                incident = result.get("incident", {})
                return f"Incident {incident.get('number')} closed successfully!"
            else:
                return f"Failed to close incident: {result.get('error')}"
        except Exception as e:
            return f"Error closing incident: {str(e)}"

    @kernel_function(
        name="assign_incident",
        description="Assign a ServiceNow incident to a specific IT technician or group."
    )
    def assign_incident(
        self,
        incident_sys_id: str,
        assigned_to: str,
        assignment_group: str = ""
    ) -> str:
        """
        Assign a ServiceNow incident to a user or group.
        
        Args:
            incident_sys_id: The sys_id of the incident
            assigned_to: sys_id of the user to assign to
            assignment_group: Optional sys_id of the assignment group
            
        Returns:
            A message indicating success or failure
        """
        try:
            result = servicenow_operations.assign_incident(
                incident_sys_id=incident_sys_id,
                assigned_to=assigned_to,
                assignment_group=assignment_group if assignment_group else None
            )
            
            if result.get("success"):
                incident = result.get("incident", {})
                return f"Incident {incident.get('number')} assigned successfully!"
            else:
                return f"Failed to assign incident: {result.get('error')}"
        except Exception as e:
            return f"Error assigning incident: {str(e)}"

    @kernel_function(
        name="search_incidents",
        description="Search ServiceNow incidents by text with paging support. Searches in short_description and description fields for IT issues."
    )
    def search_incidents(self, search_text: str, page_number: str = "1", page_size: str = "20") -> str:
        """
        Search ServiceNow incidents by text with paging.
        
        Args:
            search_text: Text to search for
            page_number: Page number to retrieve (default: 1)
            page_size: Number of incidents per page (default: 20)
            
        Returns:
            A message with the search results and paging info
        """
        try:
            page_num = int(page_number)
            page_sz = int(page_size)
            offset = (page_num - 1) * page_sz
            
            # Search in short_description and description fields
            search_query = f"short_descriptionLIKE{search_text}^ORdescriptionLIKE{search_text}"
            
            result = servicenow_operations.query_incidents(
                query=search_query,
                limit=page_sz,
                offset=offset,
                order_by="^sys_updated_on"
            )
            
            if result.get("success"):
                incidents = result.get("incidents", [])
                count = result.get("count", 0)
                has_more = result.get("has_more", False)
                
                if count == 0:
                    return f"No incidents found matching '{search_text}'."
                
                start_record = offset + 1
                end_record = offset + count
                output = [f"Search Results for '{search_text}' - Page {page_num} (showing {start_record}-{end_record}):\n"]
                
                for incident in incidents:
                    output.append(
                        f"\n- Incident {incident.get('number')}: {incident.get('short_description')}\n"
                        f"  Priority: {incident.get('priority')}, Urgency: {incident.get('urgency')}, "
                        f"Impact: {incident.get('impact')}, State: {incident.get('state')}"
                    )
                
                # Show next page guidance if there are more records
                if has_more:
                    output.append(f"\n\nMore results available. Use search_incidents with search_text='{search_text}' and page_number='{page_num + 1}' to continue.")
                
                return "".join(output)
            else:
                return f"Failed to search incidents: {result.get('error', 'Unknown error')}"
        except ValueError as ve:
            return f"Invalid page parameters for search: {str(ve)}"
        except Exception as e:
            return f"Error searching incidents: {str(e)}"
