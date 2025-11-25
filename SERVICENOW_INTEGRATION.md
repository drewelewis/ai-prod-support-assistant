# ServiceNow Integration Guide

## Overview

This document provides comprehensive information about the ServiceNow Case API integration in the AI Production Support Assistant. The integration enables the assistant to create, read, update, and query ServiceNow cases directly through conversational interactions.

## Architecture

### Components

1. **servicenow_operations.py** - Core operations class that handles API communication
2. **servicenow_tools.py** - LangChain tool wrappers for the agent
3. **test_servicenow.py** - Test suite for verifying integration

### API Reference

The integration is based on the ServiceNow Case API:
- **Documentation**: https://developer.servicenow.com/dev.do#!/reference/api/zurich/rest/case-api
- **Table**: `sn_customerservice_case`
- **API Endpoint**: `https://{instance}/api/now/table/sn_customerservice_case`

## Configuration

### Required Environment Variables

Add the following to your `.env` file:

```bash
# ServiceNow Instance URL (without https://)
SERVICENOW_INSTANCE=dev12345.service-now.com

# Authentication Option 1: Username/Password
SERVICENOW_USERNAME=your.username
SERVICENOW_PASSWORD=your_password

# Authentication Option 2: OAuth/API Token (recommended)
SERVICENOW_API_TOKEN=your_api_token
```

### Authentication Methods

The integration supports two authentication methods:

#### 1. Basic Authentication (Username/Password)
- Set `SERVICENOW_USERNAME` and `SERVICENOW_PASSWORD`
- Simple to set up for development
- Not recommended for production

#### 2. OAuth Token (Recommended)
- Set `SERVICENOW_API_TOKEN`
- More secure and recommended for production
- Supports token refresh and rotation

## Features

### Available Operations

#### 1. Create Case
Create a new support case in ServiceNow.

**Parameters:**
- `short_description` (required): Brief summary of the issue
- `description` (optional): Detailed description
- `priority` (optional): 1-5 (1=Critical, 5=Planning), default: 3
- `contact` (optional): Contact sys_id or email
- `account` (optional): Account sys_id
- `category` (optional): Case category

**Example:**
```python
operations.create_case(
    short_description="Database connection timeout",
    description="Production database intermittently timing out",
    priority="1"
)
```

#### 2. Get Case
Retrieve case details by sys_id or case number.

**Parameters:**
- `case_sys_id` OR `case_number`: Identifier for the case

**Example:**
```python
operations.get_case("a1b2c3d4e5f6g7h8i9j0")
operations.get_case_by_number("CS0001001")
```

#### 3. Update Case
Update existing case fields.

**Parameters:**
- `case_sys_id` (required): The case to update
- `updates` (required): Dictionary of fields to update

**Example:**
```python
operations.update_case(
    case_sys_id="a1b2c3d4e5f6g7h8i9j0",
    updates={
        "priority": "2",
        "state": "2",  # Work in Progress
        "description": "Updated details..."
    }
)
```

#### 4. Query Cases
Search for cases using ServiceNow encoded queries.

**Parameters:**
- `query` (optional): ServiceNow encoded query string
- `limit` (optional): Maximum results (default: 100)
- `offset` (optional): Starting record index
- `order_by` (optional): Sort field (prefix ^ for descending)
- `fields` (optional): Specific fields to return

**Query Operators:**
- `=` : Equals
- `!=` : Not equals
- `LIKE` : Contains text
- `>`, `<`, `>=`, `<=` : Comparison
- `^` : AND
- `^OR` : OR
- `^NQ` : NOT

**Examples:**
```python
# Get open high-priority cases
operations.query_cases(query="priority<=2^state!=4", limit=50)

# Search by text
operations.query_cases(query="short_descriptionLIKEdatabase")

# Complex query
operations.query_cases(
    query="priority=1^ORpriority=2^state!=3^state!=4",
    order_by="^sys_updated_on"
)
```

#### 5. Get Open Cases
Convenience method to retrieve all open cases.

**Example:**
```python
operations.get_open_cases(limit=50)
```

#### 6. Get High Priority Cases
Retrieve cases with priority 1 or 2.

**Example:**
```python
operations.get_high_priority_cases(limit=50)
```

#### 7. Search Cases by Text
Search for text across case fields.

**Parameters:**
- `search_text` (required): Text to search for
- `search_fields` (optional): Fields to search in
- `limit` (optional): Maximum results

**Example:**
```python
operations.search_cases_by_text(
    search_text="authentication error",
    search_fields=["short_description", "description", "work_notes"],
    limit=25
)
```

#### 8. Get Cases by Contact
Retrieve all cases for a specific contact.

**Example:**
```python
operations.get_cases_by_contact(
    contact_sys_id="xyz123",
    limit=50
)
```

#### 9. Get Cases by Account
Retrieve all cases for a specific account.

**Example:**
```python
operations.get_cases_by_account(
    account_sys_id="abc456",
    limit=50
)
```

#### 10. Add Case Comment
Add internal notes or customer-visible comments.

**Parameters:**
- `case_sys_id` (required): The case to comment on
- `comment` (required): Comment text
- `comment_type` (optional): 'work_notes' (internal) or 'comments' (customer-visible)

**Example:**
```python
operations.add_case_comment(
    case_sys_id="a1b2c3d4e5f6g7h8i9j0",
    comment="Investigated the issue, found root cause in configuration",
    comment_type="work_notes"
)
```

#### 11. Close Case
Mark a case as resolved.

**Parameters:**
- `case_sys_id` (required): The case to close
- `resolution_notes` (optional): Resolution description
- `close_code` (optional): Close reason code

**Example:**
```python
operations.close_case(
    case_sys_id="a1b2c3d4e5f6g7h8i9j0",
    resolution_notes="Fixed by restarting the service and updating configuration",
    close_code="Solved (Permanently)"
)
```

#### 12. Assign Case
Assign a case to a user or group.

**Parameters:**
- `case_sys_id` (required): The case to assign
- `assigned_to` (required): User sys_id
- `assignment_group` (optional): Group sys_id

**Example:**
```python
operations.assign_case(
    case_sys_id="a1b2c3d4e5f6g7h8i9j0",
    assigned_to="user_sys_id_123",
    assignment_group="support_team_sys_id"
)
```

## Case States

ServiceNow cases typically use these state values:

| State | Value | Description |
|-------|-------|-------------|
| Open | 1 | Case is open and awaiting action |
| Work in Progress | 2 | Case is being actively worked |
| Resolved | 3 | Case has been resolved |
| Closed | 4 | Case is closed |

## Priority Levels

| Priority | Value | Description |
|----------|-------|-------------|
| Critical | 1 | Critical impact, system down |
| High | 2 | High impact, significant degradation |
| Moderate | 3 | Moderate impact, some functionality affected |
| Low | 4 | Low impact, minor issue |
| Planning | 5 | Planning/future enhancement |

## LangChain Tools

The following tools are available for the AI agent:

### 1. servicenow_create_case
Creates a new ServiceNow case.

### 2. servicenow_get_case
Retrieves case details by sys_id or case number.

### 3. servicenow_update_case
Updates an existing case.

### 4. servicenow_query_cases
Queries cases with various filter options.

### 5. servicenow_add_comment
Adds comments or work notes to a case.

### 6. servicenow_close_case
Closes/resolves a case.

### 7. servicenow_assign_case
Assigns a case to a user or group.

## Integration with Chat Agent

To integrate ServiceNow tools into your chat agent, add them to the tools list in `chat.py`:

```python
from tools.servicenow_tools import servicenow_tools

# Add to existing tools
tools = github_tools + elastic_search_tools + servicenow_tools
```

## Usage Examples

### Conversational Examples

**Creating a case:**
```
User: Create a ServiceNow case for the database timeout issue we've been seeing
Assistant: [Uses servicenow_create_case tool to create the case]
Case created successfully!
Case Number: CS0001234
Sys ID: abc123def456
Priority: 3
URL: https://instance.service-now.com/...
```

**Querying cases:**
```
User: Show me all high priority open cases
Assistant: [Uses servicenow_query_cases with query_type='high_priority']
Found 5 high priority cases:
- CS0001234: Database connection timeout (Priority: 1)
- CS0001235: API rate limiting errors (Priority: 2)
...
```

**Updating a case:**
```
User: Update case CS0001234 to priority 1
Assistant: [Uses servicenow_get_case to get sys_id, then servicenow_update_case]
Case updated successfully!
Case Number: CS0001234
Updated Fields: priority
```

**Adding comments:**
```
User: Add a work note to case CS0001234 saying we've identified the root cause
Assistant: [Uses servicenow_add_comment with comment_type='work_notes']
Comment added successfully to case.
```

## Testing

### Running Tests

```bash
# Ensure environment variables are set
python tests/test_servicenow.py
```

### Test Coverage

The test suite covers:
- Case creation
- Case retrieval by sys_id and number
- Case updates
- Querying open cases
- Querying high priority cases
- Text search
- Custom queries
- Adding comments

### Manual Testing Checklist

- [ ] Create a test case
- [ ] Retrieve the case by sys_id
- [ ] Retrieve the case by case number
- [ ] Update case priority
- [ ] Add a work note
- [ ] Add a customer comment
- [ ] Query open cases
- [ ] Search cases by text
- [ ] Assign the case
- [ ] Close the case
- [ ] Verify all operations in ServiceNow UI

## Error Handling

All operations return a standardized response format:

**Success Response:**
```python
{
    "success": True,
    "case": {...},  # or other relevant data
    # additional fields based on operation
}
```

**Error Response:**
```python
{
    "success": False,
    "error": "Error message describing what went wrong"
}
```

### Common Errors

1. **Authentication Failure**
   - Verify credentials are correct
   - Check if account has necessary permissions
   - Ensure API token hasn't expired

2. **404 Not Found**
   - Verify case sys_id or number exists
   - Check table name is correct for your instance

3. **403 Forbidden**
   - User lacks permissions for the operation
   - Contact ServiceNow admin to grant necessary roles

4. **Network Timeout**
   - Check network connectivity
   - Verify ServiceNow instance URL is correct
   - Check if instance is accessible

## Security Best Practices

1. **Never commit credentials** to source control
2. **Use OAuth tokens** instead of passwords when possible
3. **Rotate tokens regularly**
4. **Use least-privilege access** - only grant necessary permissions
5. **Enable audit logging** in ServiceNow for API operations
6. **Use HTTPS** for all API calls (enforced by default)
7. **Validate input** before sending to API
8. **Handle errors gracefully** without exposing sensitive information

## Performance Optimization

1. **Use field filtering** to retrieve only needed fields:
   ```python
   operations.query_cases(fields=["number", "short_description", "priority"])
   ```

2. **Implement pagination** for large result sets:
   ```python
   operations.query_cases(limit=100, offset=0)
   operations.query_cases(limit=100, offset=100)
   ```

3. **Cache frequently accessed data** (user sys_ids, group sys_ids)

4. **Use batch operations** when possible

5. **Set appropriate timeouts** to prevent hanging requests

## Troubleshooting

### Issue: "Instance not accessible"
- Verify `SERVICENOW_INSTANCE` is set correctly (without https://)
- Check network connectivity
- Verify instance is running (check ServiceNow status page)

### Issue: "Authentication failed"
- Verify credentials are correct
- Check if using correct authentication method
- Try testing credentials in ServiceNow UI first

### Issue: "No results returned"
- Verify query syntax is correct
- Check if data exists matching the query
- Test query directly in ServiceNow UI

### Issue: "Permission denied"
- User needs appropriate roles (itil, sn_customerservice_agent)
- Contact ServiceNow administrator to grant access
- Review ServiceNow ACL (Access Control List) rules

## Additional Resources

- [ServiceNow REST API Explorer](https://developer.servicenow.com/dev.do#!/reference/api/zurich/rest/)
- [ServiceNow Table API Documentation](https://docs.servicenow.com/bundle/utah-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html)
- [ServiceNow Query Operators](https://docs.servicenow.com/bundle/utah-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html)
- [ServiceNow Authentication](https://docs.servicenow.com/bundle/utah-api-reference/page/integrate/inbound-rest/concept/c_RESTAPIAuth.html)

## Support

For issues related to:
- **ServiceNow API**: Contact ServiceNow support or check developer forums
- **Integration code**: Open an issue in this repository
- **Feature requests**: Submit a feature request in the repository

## Changelog

### Version 1.0.0 (Initial Release)
- Complete CRUD operations for ServiceNow cases
- Query and search functionality
- Comment and work note support
- Case assignment and closure
- Comprehensive error handling
- Full LangChain tool integration
- Test suite with coverage
