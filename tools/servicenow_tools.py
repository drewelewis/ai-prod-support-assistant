from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from operations.servicenow_operations import ServiceNowOperations


class CreateCaseInput(BaseModel):
    """Input schema for creating a ServiceNow case."""
    short_description: str = Field(..., description="Brief summary of the case issue")
    description: Optional[str] = Field(None, description="Detailed description of the case")
    priority: Optional[str] = Field("3", description="Priority level: 1 (Critical), 2 (High), 3 (Moderate), 4 (Low), 5 (Planning)")
    contact: Optional[str] = Field(None, description="Contact sys_id or email address")
    account: Optional[str] = Field(None, description="Account sys_id")
    category: Optional[str] = Field(None, description="Case category")


class GetCaseInput(BaseModel):
    """Input schema for retrieving a ServiceNow case."""
    case_sys_id: Optional[str] = Field(None, description="The sys_id of the case to retrieve")
    case_number: Optional[str] = Field(None, description="The case number (e.g., 'CS0001001')")


class UpdateCaseInput(BaseModel):
    """Input schema for updating a ServiceNow case."""
    case_sys_id: str = Field(..., description="The sys_id of the case to update")
    state: Optional[str] = Field(None, description="Case state: 1 (Open), 2 (Work in Progress), 3 (Resolved), 4 (Closed)")
    priority: Optional[str] = Field(None, description="Priority level: 1-5")
    short_description: Optional[str] = Field(None, description="Updated short description")
    description: Optional[str] = Field(None, description="Updated description")
    assigned_to: Optional[str] = Field(None, description="sys_id of user to assign case to")


class QueryCasesInput(BaseModel):
    """Input schema for querying ServiceNow cases."""
    query_type: str = Field(..., description="Type of query: 'open', 'high_priority', 'custom', 'search', 'by_contact', 'by_account'")
    query: Optional[str] = Field(None, description="Custom ServiceNow encoded query string (e.g., 'state=1^priority=1')")
    search_text: Optional[str] = Field(None, description="Text to search for when query_type is 'search'")
    contact_sys_id: Optional[str] = Field(None, description="Contact sys_id when query_type is 'by_contact'")
    account_sys_id: Optional[str] = Field(None, description="Account sys_id when query_type is 'by_account'")
    limit: Optional[int] = Field(50, description="Maximum number of cases to return")


class AddCommentInput(BaseModel):
    """Input schema for adding a comment to a ServiceNow case."""
    case_sys_id: str = Field(..., description="The sys_id of the case")
    comment: str = Field(..., description="The comment text to add")
    comment_type: Optional[str] = Field("work_notes", description="Comment type: 'work_notes' (internal) or 'comments' (customer-visible)")


class CloseCaseInput(BaseModel):
    """Input schema for closing a ServiceNow case."""
    case_sys_id: str = Field(..., description="The sys_id of the case to close")
    resolution_notes: Optional[str] = Field(None, description="Notes describing the resolution")
    close_code: Optional[str] = Field(None, description="Close code/reason")


class AssignCaseInput(BaseModel):
    """Input schema for assigning a ServiceNow case."""
    case_sys_id: str = Field(..., description="The sys_id of the case")
    assigned_to: str = Field(..., description="sys_id of the user to assign case to")
    assignment_group: Optional[str] = Field(None, description="Optional sys_id of the assignment group")


class ServiceNowCreateCaseTool(BaseTool):
    """Tool for creating a new ServiceNow case."""
    name: str = "servicenow_create_case"
    description: str = """
    Create a new case in ServiceNow. Use this when a user wants to create or log a new support case.
    Required: short_description (brief summary)
    Optional: description, priority (1-5), contact, account, category
    """
    args_schema: type[BaseModel] = CreateCaseInput

    def _run(self, 
             short_description: str,
             description: Optional[str] = None,
             priority: Optional[str] = "3",
             contact: Optional[str] = None,
             account: Optional[str] = None,
             category: Optional[str] = None) -> str:
        """Create a new ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            result = operations.create_case(
                short_description=short_description,
                description=description,
                priority=priority,
                contact=contact,
                account=account,
                category=category
            )
            
            if result.get("success"):
                return (f"Case created successfully!\n"
                       f"Case Number: {result.get('case_number')}\n"
                       f"Sys ID: {result.get('sys_id')}\n"
                       f"Priority: {result.get('priority')}\n"
                       f"State: {result.get('state')}\n"
                       f"URL: {result.get('url')}")
            else:
                return f"Failed to create case: {result.get('error')}"
        except Exception as e:
            return f"Error creating case: {str(e)}"


class ServiceNowGetCaseTool(BaseTool):
    """Tool for retrieving a ServiceNow case."""
    name: str = "servicenow_get_case"
    description: str = """
    Retrieve a specific ServiceNow case by sys_id or case number.
    Provide either case_sys_id or case_number to retrieve the case details.
    """
    args_schema: type[BaseModel] = GetCaseInput

    def _run(self, 
             case_sys_id: Optional[str] = None,
             case_number: Optional[str] = None) -> str:
        """Retrieve a ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            
            if case_sys_id:
                result = operations.get_case(case_sys_id)
            elif case_number:
                result = operations.get_case_by_number(case_number)
            else:
                return "Error: Must provide either case_sys_id or case_number"
            
            if result.get("success"):
                case = result.get("case", {})
                return (f"Case Details:\n"
                       f"Number: {case.get('number')}\n"
                       f"Short Description: {case.get('short_description')}\n"
                       f"Description: {case.get('description')}\n"
                       f"State: {case.get('state')}\n"
                       f"Priority: {case.get('priority')}\n"
                       f"Contact: {case.get('contact')}\n"
                       f"Account: {case.get('account')}\n"
                       f"Assigned To: {case.get('assigned_to')}\n"
                       f"Created: {case.get('sys_created_on')}\n"
                       f"Updated: {case.get('sys_updated_on')}")
            else:
                return f"Failed to retrieve case: {result.get('error')}"
        except Exception as e:
            return f"Error retrieving case: {str(e)}"


class ServiceNowUpdateCaseTool(BaseTool):
    """Tool for updating a ServiceNow case."""
    name: str = "servicenow_update_case"
    description: str = """
    Update an existing ServiceNow case. Provide the case_sys_id and the fields you want to update.
    Available fields: state, priority, short_description, description, assigned_to
    """
    args_schema: type[BaseModel] = UpdateCaseInput

    def _run(self,
             case_sys_id: str,
             state: Optional[str] = None,
             priority: Optional[str] = None,
             short_description: Optional[str] = None,
             description: Optional[str] = None,
             assigned_to: Optional[str] = None) -> str:
        """Update a ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            
            updates = {}
            if state:
                updates["state"] = state
            if priority:
                updates["priority"] = priority
            if short_description:
                updates["short_description"] = short_description
            if description:
                updates["description"] = description
            if assigned_to:
                updates["assigned_to"] = assigned_to
            
            if not updates:
                return "No updates provided. Please specify at least one field to update."
            
            result = operations.update_case(case_sys_id, updates)
            
            if result.get("success"):
                case = result.get("case", {})
                return (f"Case updated successfully!\n"
                       f"Case Number: {case.get('number')}\n"
                       f"Updated Fields: {', '.join(updates.keys())}")
            else:
                return f"Failed to update case: {result.get('error')}"
        except Exception as e:
            return f"Error updating case: {str(e)}"


class ServiceNowQueryCasesTool(BaseTool):
    """Tool for querying ServiceNow cases."""
    name: str = "servicenow_query_cases"
    description: str = """
    Query ServiceNow cases with various filters.
    Query types: 'open' (all open cases), 'high_priority' (priority 1-2), 'custom' (use query parameter),
    'search' (search text in description), 'by_contact' (cases for a contact), 'by_account' (cases for an account)
    """
    args_schema: type[BaseModel] = QueryCasesInput

    def _run(self,
             query_type: str,
             query: Optional[str] = None,
             search_text: Optional[str] = None,
             contact_sys_id: Optional[str] = None,
             account_sys_id: Optional[str] = None,
             limit: Optional[int] = 50) -> str:
        """Query ServiceNow cases."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            
            if query_type == "open":
                result = operations.get_open_cases(limit=limit)
            elif query_type == "high_priority":
                result = operations.get_high_priority_cases(limit=limit)
            elif query_type == "custom":
                if not query:
                    return "Error: 'query' parameter required for custom query type"
                result = operations.query_cases(query=query, limit=limit)
            elif query_type == "search":
                if not search_text:
                    return "Error: 'search_text' parameter required for search query type"
                result = operations.search_cases_by_text(search_text=search_text, limit=limit)
            elif query_type == "by_contact":
                if not contact_sys_id:
                    return "Error: 'contact_sys_id' parameter required for by_contact query type"
                result = operations.get_cases_by_contact(contact_sys_id=contact_sys_id, limit=limit)
            elif query_type == "by_account":
                if not account_sys_id:
                    return "Error: 'account_sys_id' parameter required for by_account query type"
                result = operations.get_cases_by_account(account_sys_id=account_sys_id, limit=limit)
            else:
                return f"Error: Unknown query_type '{query_type}'"
            
            if result.get("success"):
                cases = result.get("cases", [])
                count = result.get("count", 0)
                
                if count == 0:
                    return "No cases found matching the query."
                
                output = [f"Found {count} case(s):\n"]
                for case in cases:
                    output.append(
                        f"\n- Case {case.get('number')}: {case.get('short_description')}\n"
                        f"  Priority: {case.get('priority')}, State: {case.get('state')}\n"
                        f"  Sys ID: {case.get('sys_id')}"
                    )
                
                return "".join(output)
            else:
                return f"Failed to query cases: {result.get('error')}"
        except Exception as e:
            return f"Error querying cases: {str(e)}"


class ServiceNowAddCommentTool(BaseTool):
    """Tool for adding comments to ServiceNow cases."""
    name: str = "servicenow_add_comment"
    description: str = """
    Add a comment or work note to a ServiceNow case.
    Use 'work_notes' for internal comments or 'comments' for customer-visible comments.
    """
    args_schema: type[BaseModel] = AddCommentInput

    def _run(self,
             case_sys_id: str,
             comment: str,
             comment_type: Optional[str] = "work_notes") -> str:
        """Add a comment to a ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            result = operations.add_case_comment(
                case_sys_id=case_sys_id,
                comment=comment,
                comment_type=comment_type
            )
            
            if result.get("success"):
                return f"Comment added successfully to case."
            else:
                return f"Failed to add comment: {result.get('error')}"
        except Exception as e:
            return f"Error adding comment: {str(e)}"


class ServiceNowCloseCaseTool(BaseTool):
    """Tool for closing ServiceNow cases."""
    name: str = "servicenow_close_case"
    description: str = """
    Close a ServiceNow case. Optionally provide resolution notes and close code.
    This sets the case state to 'Resolved'.
    """
    args_schema: type[BaseModel] = CloseCaseInput

    def _run(self,
             case_sys_id: str,
             resolution_notes: Optional[str] = None,
             close_code: Optional[str] = None) -> str:
        """Close a ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            result = operations.close_case(
                case_sys_id=case_sys_id,
                resolution_notes=resolution_notes,
                close_code=close_code
            )
            
            if result.get("success"):
                case = result.get("case", {})
                return (f"Case closed successfully!\n"
                       f"Case Number: {case.get('number')}\n"
                       f"State: Resolved")
            else:
                return f"Failed to close case: {result.get('error')}"
        except Exception as e:
            return f"Error closing case: {str(e)}"


class ServiceNowAssignCaseTool(BaseTool):
    """Tool for assigning ServiceNow cases."""
    name: str = "servicenow_assign_case"
    description: str = """
    Assign a ServiceNow case to a user or assignment group.
    Provide the case_sys_id, assigned_to user sys_id, and optionally an assignment_group sys_id.
    """
    args_schema: type[BaseModel] = AssignCaseInput

    def _run(self,
             case_sys_id: str,
             assigned_to: str,
             assignment_group: Optional[str] = None) -> str:
        """Assign a ServiceNow case."""
        try:
            operations = ServiceNowOperations(table_name="incident")
            result = operations.assign_case(
                case_sys_id=case_sys_id,
                assigned_to=assigned_to,
                assignment_group=assignment_group
            )
            
            if result.get("success"):
                case = result.get("case", {})
                return (f"Case assigned successfully!\n"
                       f"Case Number: {case.get('number')}\n"
                       f"Assigned To: {case.get('assigned_to')}")
            else:
                return f"Failed to assign case: {result.get('error')}"
        except Exception as e:
            return f"Error assigning case: {str(e)}"


# Export all tools for easy import
servicenow_tools = [
    ServiceNowCreateCaseTool(),
    ServiceNowGetCaseTool(),
    ServiceNowUpdateCaseTool(),
    ServiceNowQueryCasesTool(),
    ServiceNowAddCommentTool(),
    ServiceNowCloseCaseTool(),
    ServiceNowAssignCaseTool()
]
