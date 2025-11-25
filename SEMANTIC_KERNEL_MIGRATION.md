# Semantic Kernel Migration Guide

## Overview

The AI Production Support Assistant has been migrated from **LangGraph** to **Semantic Kernel**. This document explains the changes, benefits, and how to use the new implementation.

## What Changed?

### Architecture Changes

**Before (LangGraph):**
- Used LangGraph's StateGraph for conversation flow
- LangChain tools with BaseTool classes
- MemorySaver for conversation history
- Complex node-based graph architecture

**After (Semantic Kernel):**
- Semantic Kernel orchestration with native function calling
- Plugins with `@kernel_function` decorators
- Built-in ChatHistory management
- Simpler, more intuitive architecture

### File Structure

**New Files:**
```
plugins/
├── __init__.py              # Plugin exports
├── github_plugin.py         # GitHub operations plugin
├── elasticsearch_plugin.py  # Elasticsearch search plugin
└── servicenow_plugin.py     # ServiceNow case management plugin

chat_sk.py                   # New Semantic Kernel chat implementation
SEMANTIC_KERNEL_MIGRATION.md # This file
```

**Legacy Files (Still Available):**
```
tools/                       # Original LangChain tools
chat.py                      # Original LangGraph implementation
```

## Benefits of Semantic Kernel

### 1. **Simpler Plugin System**
Semantic Kernel plugins use simple decorators instead of complex class hierarchies:

```python
@kernel_function(
    name="get_repos_by_user",
    description="Get a list of repositories from a GitHub user account"
)
def get_repos_by_user(self, user: str) -> str:
    # Implementation
```

### 2. **Native Async Support**
Semantic Kernel is built async-first, providing better performance and scalability.

### 3. **Better Azure OpenAI Integration**
Native support for Azure OpenAI with simpler configuration and better token management.

### 4. **Automatic Function Calling**
The kernel automatically handles function invocation without manual tool routing:

```python
execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
    auto_invoke=True
)
```

### 5. **Cleaner Code**
- Less boilerplate code
- More intuitive API
- Better separation of concerns
- Easier to extend and maintain

## Installation

### 1. Update Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `semantic-kernel>=1.0.0` (replaces langchain, langgraph, langchain-openai)
- All existing dependencies (PyGithub, elasticsearch, etc.)

### 2. Verify Environment Variables

Ensure your `.env` file has the required variables:

```bash
# Azure OpenAI Configuration
OPENAI_API_ENDPOINT=https://your-instance.openai.azure.com/
OPENAI_API_KEY=your-azure-openai-key
OPENAI_API_VERSION=2024-02-15-preview
OPENAI_API_MODEL_DEPLOYMENT_NAME=your-deployment-name

# GitHub Integration
GITHUB_PAT=ghp_your-github-personal-access-token

# Elasticsearch Configuration
ELASTICSEARCH_URL=https://your-elasticsearch-url:9200
ELASTICSEARCH_INDEX=your-log-index-name

# ServiceNow Configuration (Optional)
SERVICENOW_INSTANCE=your-instance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
```

## Usage

### Running the New Chat Interface

```bash
python chat_sk.py
```

### Commands

- `/q`, `/quit`, `/exit` - Exit the chat
- `/clear`, `/reset` - Clear chat history and start fresh

### Example Conversations

**GitHub Operations:**
```
> Show me repositories for user drewelewis
Assistant: Found 15 repositories for user 'drewelewis':
- drewelewis/ContosoBankAPI
- drewelewis/ai-prod-support-assistant
...

> Get the file list for drewelewis/ContosoBankAPI
Assistant: Found 42 files in repository 'drewelewis/ContosoBankAPI':
- README.md
- app.py
- requirements.txt
...

> Show me the content of app.py
Assistant: Content of file 'app.py' from repository 'drewelewis/ContosoBankAPI':
...
```

**Elasticsearch Queries:**
```
> Find all error logs
Assistant: Found 25 log entries:
--- Log Entry 1 ---
Timestamp: 2025-11-24T10:30:00
Level: ERROR
Message: Database connection timeout
...

> Show me logs from host server-01 with errors
Assistant: [Searches with proper Elasticsearch query]
...
```

**ServiceNow Cases:**
```
> Create a case for the database timeout issue
Assistant: Case created successfully!
Case Number: CS0001234
Priority: 3
...

> Show me all open high priority cases
Assistant: Found 5 high priority case(s):
- Case CS0001234: Database connection timeout
  Priority: 1, State: Open
...
```

## Plugin Development

### Creating a New Plugin

1. **Create a new plugin file** in the `plugins/` directory:

```python
# plugins/my_plugin.py
from semantic_kernel.functions import kernel_function

class MyPlugin:
    """Description of your plugin"""
    
    @kernel_function(
        name="my_function",
        description="What this function does"
    )
    def my_function(self, param1: str, param2: str = "default") -> str:
        """
        Function docstring
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Description of return value
        """
        # Your implementation
        return f"Result: {param1} and {param2}"
```

2. **Register the plugin** in `chat_sk.py`:

```python
from plugins.my_plugin import MyPlugin

# In setup_plugins method:
self.kernel.add_plugin(
    MyPlugin(),
    plugin_name="MyPlugin"
)
```

### Plugin Best Practices

1. **Clear Descriptions:** Provide detailed descriptions for functions so the AI knows when to use them
2. **Type Hints:** Always use type hints for parameters and return values
3. **Error Handling:** Handle exceptions gracefully and return user-friendly error messages
4. **Parameter Validation:** Validate inputs before processing
5. **Consistent Return Types:** Return strings for display to the user

## Comparison: LangGraph vs Semantic Kernel

| Feature | LangGraph | Semantic Kernel |
|---------|-----------|-----------------|
| **Architecture** | Graph-based state machine | Plugin-based orchestration |
| **Tool Definition** | BaseTool classes | @kernel_function decorators |
| **Complexity** | Higher (nodes, edges, state) | Lower (simple functions) |
| **Learning Curve** | Steeper | Gentler |
| **Async Support** | Bolt-on | Native |
| **Function Calling** | Manual routing | Automatic |
| **Code Lines** | More boilerplate | Less boilerplate |
| **Extensibility** | Good | Excellent |
| **Azure Integration** | Via LangChain | Native |
| **Memory Management** | MemorySaver | ChatHistory |

## Migration Checklist

- [x] Create plugin directory structure
- [x] Convert GitHub tools to GitHubPlugin
- [x] Convert Elasticsearch tools to ElasticsearchPlugin
- [x] Convert ServiceNow tools to ServiceNowPlugin
- [x] Create new chat_sk.py with Semantic Kernel
- [x] Update requirements.txt
- [x] Test all plugin functions
- [x] Document migration process

## Testing

### Unit Testing Plugins

Test individual plugin functions:

```python
from plugins.github_plugin import GitHubPlugin

plugin = GitHubPlugin()
result = plugin.get_repos_by_user("drewelewis")
print(result)
```

### Integration Testing

Test the full chat workflow:

```bash
python chat_sk.py
```

Then interact with the assistant to verify:
- GitHub operations work correctly
- Elasticsearch queries return results
- ServiceNow integration functions properly
- Function calling is automatic
- Chat history is maintained

## Troubleshooting

### Issue: Import errors for semantic_kernel

**Solution:** Install Semantic Kernel
```bash
pip install semantic-kernel
```

### Issue: Functions not being called

**Check:**
1. Function descriptions are clear and specific
2. Parameters are properly typed
3. Plugin is registered in the kernel
4. Function choice behavior is set to Auto

### Issue: Azure OpenAI connection errors

**Verify:**
1. Environment variables are set correctly
2. API endpoint includes `/` at the end
3. API version is compatible
4. Deployment name matches your Azure resource

## Performance Considerations

### Semantic Kernel Advantages:
- **Async Operations:** Better concurrency handling
- **Efficient Token Usage:** Optimized prompt engineering
- **Faster Function Calling:** Native implementation
- **Memory Efficiency:** Better resource management

### Optimization Tips:
1. Use async operations where possible
2. Limit chat history size for long conversations
3. Implement caching for frequently accessed data
4. Use connection pooling for external services

## Migration from LangGraph

If you want to continue using the LangGraph version:

```bash
# Use the original implementation
python chat.py
```

Both implementations are maintained in the repository for compatibility.

## Future Enhancements

Potential improvements with Semantic Kernel:

1. **Memory Plugins:** Long-term memory storage
2. **Planners:** Advanced multi-step planning
3. **Multiple Models:** Support for different AI models
4. **Prompt Templates:** Reusable prompt engineering
5. **Semantic Functions:** Dynamic prompt-based functions
6. **Telemetry:** Built-in logging and monitoring
7. **Embedding Integration:** Vector search capabilities

## Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Plugin Development Guide](https://learn.microsoft.com/en-us/semantic-kernel/agents/plugins/)

## Support

For issues or questions:
1. Check this migration guide
2. Review the Semantic Kernel documentation
3. Examine the plugin code for examples
4. Open an issue in the repository

## Conclusion

The migration to Semantic Kernel provides:
- ✅ Simpler, more maintainable code
- ✅ Better Azure OpenAI integration
- ✅ Native async support
- ✅ Automatic function calling
- ✅ Easier plugin development
- ✅ Better performance

The new implementation maintains all the functionality of the original while providing a better developer experience and foundation for future enhancements.
