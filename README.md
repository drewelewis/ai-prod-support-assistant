# AI Production Support Assistant

A sophisticated AI-powered assistant built with Azure OpenAI and LangGraph to streamline production support workflows for development teams. This intelligent agent combines conversational AI with powerful integrations to GitHub and Elasticsearch, enabling support staff and developers to quickly diagnose issues, search code repositories, and analyze application logs.

## 🎯 Overview

The AI Production Support Assistant serves as a conversational interface that can autonomously:
- Search and analyze application logs stored in Elasticsearch
- Browse GitHub repositories and examine source code
- Create GitHub issues for tracking problems
- Provide intelligent assistance for production support scenarios
- Maintain conversation context and memory across interactions

## 🏗️ Architecture

### Core Components

The solution follows a modular, agent-based architecture built on LangGraph's state management system:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat Layer    │    │  LangGraph      │    │  Tool Layer     │
│   (chat.py)     │◄──►│  State Graph    │◄──►│  GitHub Tools   │
│                 │    │                 │    │  Elastic Tools  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Azure OpenAI    │    │ Memory Saver    │    │  Operations     │
│ Integration     │    │ (Persistence)   │    │  Layer          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Architectural Patterns

**1. State Graph Architecture (LangGraph)**
- Implements a conversational state graph with memory persistence
- Supports tool routing and conditional execution
- Maintains conversation context across multiple interactions

**2. Tool-Based Agent Pattern**
- Modular tool system with dedicated GitHub and Elasticsearch integrations
- Each tool is self-contained with validation and error handling
- Dynamic tool selection based on user queries

**3. Operations Layer Abstraction**
- Clean separation between tool interfaces and business logic
- Reusable operations classes for GitHub and Elasticsearch interactions
- Centralized error handling and connection management

## 🔧 Technical Stack

### Core Technologies
- **LangGraph**: State graph framework for building conversational AI agents
- **LangChain**: Tool integration and prompt management
- **Azure OpenAI**: Large language model for natural language processing
- **Python 3.12**: Primary development language

### Integrations
- **GitHub API**: Repository browsing, file content access, issue creation
- **Elasticsearch**: Log search and analysis with KQL support
- **PyGithub**: Python wrapper for GitHub API operations
- **Elasticsearch-py**: Official Elasticsearch Python client

### Infrastructure
- **Docker Compose**: Local development environment with PostgreSQL and Adminer
- **Environment Configuration**: Secure credential management via environment variables

## 🚀 Capabilities

### GitHub Integration
The assistant provides comprehensive GitHub repository management:

**Repository Operations:**
- List all repositories for a given user
- Browse repository file structures
- Access and display file contents
- Create issues with detailed descriptions

**Code Analysis:**
- Search through repository contents
- Analyze code patterns and structures
- Provide insights into application architecture

### Elasticsearch Integration
Advanced log analysis capabilities with structured querying:

**Log Search Features:**
- KQL (Kibana Query Language) support for precise log filtering
- Multi-field search across log attributes (levelname, message, host, timestamp)
- Structured log parsing for Python applications

**Supported Log Fields:**
```json
{
  "exc_info": "Exception information",
  "exc_text": "Exception text details", 
  "filename": "Source file name",
  "funcName": "Function name where log originated",
  "host": "Server hostname",
  "host_ip": "Server IP address",
  "levelname": "Log level (ERROR, INFO, WARNING, etc.)",
  "lineno": "Line number in source code",
  "message": "Log message content",
  "module": "Python module name",
  "pathname": "Full file path",
  "process": "Process ID",
  "processName": "Process name",
  "timestamp": "Log timestamp"
}
```

### Conversational AI Features
- **Context Awareness**: Maintains conversation history and context
- **Intelligent Routing**: Automatically selects appropriate tools based on user queries
- **Memory Persistence**: Remembers previous interactions within a session
- **Error Handling**: Graceful degradation when tools encounter issues

## 📁 Project Structure

```
ai-prod-support-assistant/
├── chat.py                     # Main application entry point and LangGraph configuration
├── messages.py                 # Message handling utilities
├── requirements.txt            # Python dependencies
├── docker-compose.yaml         # Infrastructure setup (PostgreSQL, Adminer)
├── env.sample                  # Environment variable template
├── tools/                      # Tool implementations
│   ├── github_tools.py         # GitHub API tool wrappers
│   └── elastic_search_tools.py # Elasticsearch tool wrappers
├── operations/                 # Business logic layer
│   ├── github_operations.py    # GitHub API operations
│   └── elastic_search_operations.py # Elasticsearch operations
├── utils/                      # Utility functions
│   └── graph_utils.py          # Graph visualization utilities
├── tests/                      # Test suite
│   ├── test_github.py          # GitHub integration tests
│   └── test_elastic.py         # Elasticsearch integration tests
├── images/                     # Generated graph visualizations
├── output/                     # Output files and reports
└── *.bat                       # Windows batch files for environment management
```

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file based on `env.sample`:

```bash
# Azure OpenAI Configuration
OPENAI_API_ENDPOINT=https://your-instance.openai.azure.com/
OPENAI_API_KEY=your-azure-openai-key
OPENAI_API_VERSION=2024-02-15-preview
OPENAI_API_MODEL_VERSION=gpt-4
OPENAI_API_MODEL_DEPLOYMENT_NAME=your-deployment-name

# GitHub Integration
GITHUB_PAT=ghp_your-github-personal-access-token

# Elasticsearch Configuration  
ELASTICSEARCH_URL=https://your-elasticsearch-url:9200
ELASTICSEARCH_INDEX=your-log-index-name
```

### GitHub PAT Permissions
Your GitHub Personal Access Token should have the following permissions:
- `repo` (for private repository access)
- `public_repo` (for public repository access)
- `read:user` (for user information)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Access to Azure OpenAI service
- GitHub Personal Access Token
- Elasticsearch cluster (optional, for log analysis)
- Docker and Docker Compose (for local development)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/drewelewis/ai-prod-support-assistant.git
   cd ai-prod-support-assistant
   ```

2. **Set up Python environment:**
   ```bash
   # On Windows
   _env_create.bat    # Create virtual environment
   _env_activate.bat  # Activate environment
   _install.bat       # Install dependencies
   
   # On Unix/Linux/Mac
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp env.sample .env
   # Edit .env with your actual configuration values
   ```

4. **Start supporting services (optional):**
   ```bash
   # On Windows
   _up.bat
   
   # On Unix/Linux/Mac
   docker compose up -d
   ```

5. **Run the assistant:**
   ```bash
   python chat.py
   ```

## 📖 Usage Examples

### Basic Interaction
```
> How can I help you?
User: Show me the repositories for user drewelewis
Assistant: [Lists all repositories with descriptions]

User: Get the file list for drewelewis/ContosoBankAPI
Assistant: [Displays repository file structure]

User: Show me the content of the main.py file
Assistant: [Displays file content with syntax highlighting]
```

### Log Analysis
```
User: Find all error logs from the last hour
Assistant: [Searches Elasticsearch and returns filtered error logs]

User: Show me logs from host server-01 with level ERROR
Assistant: [Returns specific error logs from the specified host]
```

### Issue Management
```
User: Create an issue in drewelewis/ContosoBankAPI titled "Database connection timeout" with details about the recent connection issues
Assistant: [Creates GitHub issue and returns the issue URL]
```

## 🔍 Advanced Features

### Graph Visualization
The assistant automatically generates visual representations of its conversation flow and saves them to the `images/` directory. These diagrams help understand the agent's decision-making process.

### Memory Management
- Persistent conversation memory within sessions
- Context-aware responses based on previous interactions
- Automatic cleanup and session management

### Error Handling and Resilience
- Graceful degradation when external services are unavailable
- Comprehensive error logging and user feedback
- Automatic retry mechanisms for transient failures

### Extensibility
The modular architecture makes it easy to add new tools:
1. Create a new tool class inheriting from `BaseTool`
2. Implement the corresponding operations class
3. Register the tool in the main graph configuration

## 🧪 Testing

Run the test suite to verify integrations:

```bash
# Test GitHub integration
python tests/test_github.py

# Test Elasticsearch integration  
python tests/test_elastic.py
```

## 🔐 Security Considerations

- **API Keys**: Store all sensitive credentials in environment variables
- **Access Control**: Use least-privilege GitHub PATs
- **Network Security**: Ensure Elasticsearch clusters are properly secured
- **Data Privacy**: Be mindful of sensitive information in logs and repositories

## 🚦 Operational Excellence

### Performance Optimization
- Connection pooling for external APIs
- Efficient query patterns for Elasticsearch
- Streaming responses for better user experience

### Monitoring and Observability
- Comprehensive error logging
- Tool usage tracking
- Performance metrics collection

### Scalability Considerations
- Stateless tool operations for horizontal scaling
- Configurable connection limits
- Resource usage optimization

## 🛠️ Development Workflow

### Environment Management
Use the provided batch files for streamlined development:
- `_env_create.bat`: Initialize Python virtual environment
- `_env_activate.bat`: Activate development environment
- `_env_deactivate.bat`: Deactivate environment
- `_install.bat`: Install/update dependencies
- `_up.bat`: Start supporting services
- `_down.bat`: Stop supporting services

### Adding New Capabilities
1. Define new tool requirements
2. Implement operations class with business logic
3. Create tool wrapper with validation
4. Register tool in main graph
5. Add comprehensive tests
6. Update documentation

## 📋 Roadmap

Future enhancements planned:
- **Multi-model Support**: Integration with additional LLM providers
- **Advanced Analytics**: Enhanced log analysis with ML-powered insights
- **Workflow Automation**: Automated incident response workflows
- **Integration Expansion**: Support for additional platforms (Jira, Slack, etc.)
- **Performance Monitoring**: Real-time application performance insights
- **Custom Dashboards**: Web-based interface for visual interactions

## 🤝 Contributing

This project follows standard GitHub workflow practices. Please ensure all contributions include appropriate tests and documentation updates.

## 📄 License

This project is licensed under the terms specified in the LICENSE file.