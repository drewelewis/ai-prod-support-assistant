# Quick Start: Semantic Kernel vs LangGraph

## Which Implementation Should I Use?

### ✅ Use Semantic Kernel (chat_sk.py) if:
- You're starting a new project
- You want simpler, more maintainable code
- You prefer native Azure OpenAI integration
- You need better async/await support
- You want easier plugin development
- You're building for production

### ⚠️ Use LangGraph (chat.py) if:
- You need complex state management with custom nodes
- You require graph-based conversation flows
- You're maintaining existing LangGraph code
- You need LangChain ecosystem compatibility

## Quick Comparison

| Feature | Semantic Kernel | LangGraph |
|---------|----------------|-----------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Simple | ⭐⭐⭐ Moderate |
| **Code Complexity** | Low | High |
| **Learning Curve** | Gentle | Steep |
| **Plugin Development** | Easy with decorators | Complex with classes |
| **Azure Integration** | Native | Via adapter |
| **Performance** | Fast | Fast |
| **Function Calling** | Automatic | Manual routing |
| **Production Ready** | Yes | Yes |

## Code Comparison

### Defining a Function

**Semantic Kernel:**
```python
@kernel_function(
    name="get_repos",
    description="Get user repositories"
)
def get_repos(self, user: str) -> str:
    return github_operations.get_repo_list(user)
```

**LangGraph:**
```python
class GithubGetReposTool(BaseTool):
    name: str = "GithubGetReposTool"
    description: str = "Get user repositories"
    return_direct: bool = False
    
    class InputModel(BaseModel):
        user: str = Field(description="user")
        
        @field_validator("user")
        def validate_query_param(user):
            if not user:
                raise ValueError("user parameter is empty")
            return user
    
    args_schema: Optional[ArgsSchema] = InputModel
    
    def _run(self, user: str) -> str:
        return github_operations.get_repo_list(user)
```

### Chat Loop

**Semantic Kernel:**
```python
async def chat(self, user_input: str) -> str:
    self.chat_history.add_user_message(user_input)
    
    response = await chat_completion.get_chat_message_contents(
        chat_history=self.chat_history,
        settings=execution_settings,
        kernel=self.kernel
    )
    
    return str(response[0])
```

**LangGraph:**
```python
def stream_graph_updates(role: str, content: str):
    config = {"configurable": {"thread_id": "1"}}
    events = graph.stream(
        {"messages": [{"role": role, "content": content}]},
        config,
        stream_mode="values",
    )
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
    return event["messages"][-1]
```

## Running Each Implementation

### Semantic Kernel
```bash
# Install dependencies
pip install semantic-kernel

# Run
python chat_sk.py

# Commands
> /q         # Exit
> /clear     # Clear history
```

### LangGraph
```bash
# Install dependencies
pip install langchain langgraph langchain-openai

# Run
python chat.py

# Commands
> /q         # Exit
```

## Migration Path

If you're currently using LangGraph:

1. **Keep LangGraph running** - Both implementations can coexist
2. **Test Semantic Kernel** - Try `chat_sk.py` alongside your current setup
3. **Compare results** - Verify functionality matches your needs
4. **Gradually migrate** - Move plugins one at a time if needed
5. **Update documentation** - Switch references when ready

## Plugin Development

### Adding a New Function

**Semantic Kernel (Easier):**
```python
@kernel_function(
    name="my_function",
    description="What this function does"
)
def my_function(self, param: str) -> str:
    # Your code here
    return result
```

**LangGraph (More Complex):**
```python
class MyTool(BaseTool):
    name: str = "MyTool"
    description: str = "What this function does"
    
    class InputModel(BaseModel):
        param: str = Field(description="param")
        
        @field_validator("param")
        def validate(param):
            if not param:
                raise ValueError("param is empty")
            return param
    
    args_schema: Optional[ArgsSchema] = InputModel
    
    def _run(self, param: str) -> str:
        # Your code here
        return result
```

## Performance Considerations

### Semantic Kernel
- **Async-first design** - Better concurrency
- **Efficient token usage** - Optimized prompts
- **Fast function calling** - Native implementation
- **Memory efficient** - Better resource management

### LangGraph
- **Graph optimization** - Efficient state transitions
- **Streaming support** - Real-time responses
- **Checkpointing** - Resume from any state
- **Flexible routing** - Custom conversation flows

## Recommendation

**For most use cases, we recommend Semantic Kernel** because:
1. Simpler to understand and maintain
2. Better Azure OpenAI integration
3. Easier to extend with new plugins
4. Less boilerplate code
5. Better async support
6. Actively developed by Microsoft

**Choose LangGraph only if:**
- You need complex graph-based flows
- You're already invested in LangChain ecosystem
- You require specific LangGraph features

## Need Help?

- **Semantic Kernel**: See [SEMANTIC_KERNEL_MIGRATION.md](SEMANTIC_KERNEL_MIGRATION.md)
- **LangGraph**: See original [README.md](README.md) sections
- **Both**: All operations classes are shared between implementations
