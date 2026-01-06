# AI Production Support Assistant

A sophisticated AI-powered assistant built with Azure OpenAI and available in two implementations: **Semantic Kernel** (recommended) and **LangGraph** (legacy). This intelligent agent streamlines production support workflows by combining conversational AI with powerful integrations to GitHub, Elasticsearch, and ServiceNow, enabling support staff and developers to quickly diagnose issues, search code repositories, analyze application logs, and manage support cases.

## 🎯 Overview

The AI Production Support Assistant serves as a conversational interface that can autonomously:
- Search and analyze application logs stored in Elasticsearch
- Browse GitHub repositories and examine source code
- Create GitHub issues for tracking problems
- Manage ServiceNow support cases
- Provide intelligent assistance for production support scenarios
- Maintain conversation context and memory across interactions

## 🆕 Two Implementation Options

### 1. **Semantic Kernel (Recommended) - NEW!** ✨

The modern implementation using Microsoft's Semantic Kernel framework.

**Benefits:**
- Simpler, more maintainable code
- Native Azure OpenAI integration
- Built-in async support
- Automatic function calling
- Easier plugin development

**Run with:**
```bash
python chat_sk.py
```

**Learn more:** See [SEMANTIC_KERNEL_MIGRATION.md](SEMANTIC_KERNEL_MIGRATION.md)

### 2. **LangGraph (Legacy)**

The original implementation using LangGraph's state management system.

**Run with:**
```bash
python chat.py
```

## 🏗️ Architecture

### Semantic Kernel Architecture (Recommended)

The solution follows a plugin-based architecture built on Semantic Kernel:

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[🖥️ Chat Interface<br/>chat_sk.py]
    end
    
    subgraph "AI Orchestration Layer"
        SK[🧠 Semantic Kernel<br/>Framework]
        CH[💭 Chat History<br/>Management]
        AOI[🤖 Azure OpenAI<br/>GPT-4 Integration]
    end
    
    subgraph "Plugin Layer"
        GP[🐙 GitHub Plugin<br/>@kernel_function]
        EP[🔍 Elasticsearch Plugin<br/>@kernel_function]
        SP[🎫 ServiceNow Plugin<br/>@kernel_function]
    end
    
    subgraph "Operations Layer"
        GO[📂 GitHub Operations<br/>Repository Management]
        EO[📊 Elasticsearch Operations<br/>Log Analysis]
        SO[🔧 ServiceNow Operations<br/>Incident Management]
    end
    
    subgraph "External Systems"
        GH[🌐 GitHub API<br/>REST v4]
        ES[⚡ Elasticsearch<br/>Search Engine]
        SN[🏢 ServiceNow<br/>Table API]
    end
    
    %% User Interface Flow
    UI --> SK
    SK --> CH
    SK --> AOI
    
    %% Plugin Registration
    SK --> GP
    SK --> EP
    SK --> SP
    
    %% Plugin to Operations Flow
    GP --> GO
    EP --> EO
    SP --> SO
    
    %% Operations to External Systems
    GO --> GH
    EO --> ES
    SO --> SN
    
    %% Data Flow Styling
    classDef userLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef aiLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef pluginLayer fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef opsLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef extLayer fill:#ffebee,stroke:#b71c1c,stroke-width:2px
    
    class UI userLayer
    class SK,CH,AOI aiLayer
    class GP,EP,SP pluginLayer
    class GO,EO,SO opsLayer
    class GH,ES,SN extLayer
```

### Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant C as 🖥️ Chat Interface
    participant K as 🧠 Semantic Kernel
    participant P as 🔌 Plugin
    participant O as ⚙️ Operations
    participant A as 🌐 External API
    
    U->>C: "Show me open incidents"
    C->>K: Process user message
    K->>K: Function selection<br/>(auto-routing)
    K->>P: ServiceNow Plugin<br/>query_open_incidents()
    P->>O: ServiceNow Operations<br/>query_incidents()
    O->>A: REST API Call<br/>GET /table/incident
    A->>O: JSON Response<br/>(incidents data)
    O->>P: Formatted results<br/>(paging info)
    P->>K: Plugin response<br/>(user-friendly text)
    K->>C: AI-generated response<br/>(with context)
    C->>U: "Open Incidents - Page 1<br/>(showing 1-20)..."
```

### Key Architectural Patterns

**1. Plugin-Based Architecture (Semantic Kernel)**
- Modular plugin system using `@kernel_function` decorators
- Automatic function calling with FunctionChoiceBehavior
- Native async/await support throughout
- Simple, declarative function definitions

**2. Operations Layer Abstraction**
- Clean separation between plugin interfaces and business logic
- Reusable operations classes for GitHub, Elasticsearch, and ServiceNow
- Centralized error handling and connection management

**3. Conversation Management**
- Built-in ChatHistory for context persistence
- System message configuration for behavior control
- Automatic tool invocation without manual routing

## 🔧 Technical Stack

### Core Technologies
- **Semantic Kernel**: Microsoft's AI orchestration framework (recommended)
- **LangGraph**: State graph framework (legacy implementation)
- **Azure OpenAI**: Large language model for natural language processing
- **Python 3.12+**: Primary development language

### Integrations
- **GitHub API**: Repository browsing, file content access, issue creation
- **Elasticsearch**: Log search and analysis with KQL support
- **ServiceNow REST API**: Complete incident lifecycle management
  - Table API for incident CRUD operations
  - Advanced querying with encoded query strings
  - Paging support for large datasets
  - Field-level access control and validation
- **PyGithub**: Python wrapper for GitHub API operations
- **Elasticsearch-py**: Official Elasticsearch Python client
- **Requests**: HTTP client for ServiceNow REST API integration

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

### ServiceNow Incident Management
Comprehensive internal IT support with ServiceNow incident management system:

**Incident Lifecycle Management:**
- Create new IT incidents with detailed categorization (priority, urgency, impact)
- Query and browse open incidents with intelligent paging (default 20 per page)
- Search incidents by text content across descriptions and comments
- Retrieve specific incident details by number (e.g., INC0001234) or system ID

**Advanced Incident Operations:**
- Add contextual comments and work notes to existing incidents
- Update incident status through resolution workflow
- Assign incidents to appropriate technical staff members
- Close resolved incidents with proper resolution codes
- Filter incidents by priority levels (high priority: P1/P2)

**Intelligent Paging System:**
- Automatic pagination for large incident datasets
- Configurable page sizes (default: 20, customizable: 10, 50, 100)
- Smart navigation with "More incidents available" guidance
- Optimized queries using ServiceNow's REST Table API

**ServiceNow Integration Features:**
- REST API-based integration using Table API endpoints
- Support for both username/password and API token authentication
- Clean error handling with fallback mechanisms
- Compatible with all ServiceNow instance versions

**Supported ServiceNow Fields:**
```json
{
  "number": "Incident identifier (e.g., INC0001234)",
  "short_description": "Brief incident summary",
  "description": "Detailed incident description", 
  "priority": "Business priority (1=Critical, 2=High, 3=Medium, 4=Low)",
  "urgency": "Business urgency (1=High, 2=Medium, 3=Low)",
  "impact": "Business impact (1=High, 2=Medium, 3=Low)",
  "state": "Incident state (1=New, 2=In Progress, 6=Resolved, 7=Closed)",
  "assigned_to": "Assigned technician",
  "assignment_group": "Responsible team",
  "caller_id": "Person reporting the incident",
  "work_notes": "Technical work notes",
  "comments": "Customer-facing comments"
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
├── chat_sk.py                  # Semantic Kernel chat implementation (NEW - RECOMMENDED)
├── chat.py                     # LangGraph chat implementation (LEGACY)
├── messages.py                 # Message handling utilities
├── requirements.txt            # Python dependencies
├── docker-compose.yaml         # Infrastructure setup (PostgreSQL, Adminer)
├── env.sample                  # Environment variable template
├── plugins/                    # Semantic Kernel plugins (NEW)
│   ├── __init__.py             # Plugin exports
│   ├── github_plugin.py        # GitHub operations plugin
│   ├── elasticsearch_plugin.py # Elasticsearch search plugin
│   └── servicenow_plugin.py    # ServiceNow incident management plugin
├── tools/                      # LangChain tool implementations (LEGACY)
│   ├── github_tools.py         # GitHub API tool wrappers
│   ├── elastic_search_tools.py # Elasticsearch tool wrappers
│   └── servicenow_tools.py     # ServiceNow tool wrappers
├── operations/                 # Business logic layer (SHARED)
│   ├── github_operations.py    # GitHub API operations
│   ├── elastic_search_operations.py # Elasticsearch operations
│   └── servicenow_operations.py # ServiceNow operations
├── utils/                      # Utility functions
│   └── graph_utils.py          # Graph visualization utilities
├── tests/                      # Test suite
│   ├── test_github.py          # GitHub integration tests
│   ├── test_elastic.py         # Elasticsearch integration tests
│   └── test_servicenow.py      # ServiceNow integration tests
├── images/                     # Generated graph visualizations
├── output/                     # Output files and reports
├── SEMANTIC_KERNEL_MIGRATION.md # Migration guide
├── SERVICENOW_INTEGRATION.md   # ServiceNow integration documentation
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

# ServiceNow Configuration (for Incident Management)
SERVICENOW_INSTANCE=your-instance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
# OR use API token instead (recommended for production)
SERVICENOW_API_TOKEN=your_api_token
```

### Authentication Methods

#### GitHub PAT Permissions
Your GitHub Personal Access Token should have the following permissions:
- `repo` (for private repository access)
- `public_repo` (for public repository access)
- `read:user` (for user information)

#### ServiceNow Authentication
**Choose one of two authentication methods:**

**Option 1: Username/Password**
```bash
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
```

**Option 2: API Token (Recommended for Production)**
```bash
SERVICENOW_API_TOKEN=your_api_token
```

**ServiceNow Setup Requirements:**
- ServiceNow instance with incident table access
- User account with appropriate roles:
  - `incident_manager` - Full incident lifecycle management
  - `itil` - Standard ITSM operations  
  - `rest_api_explorer` - REST API access
- Network access to ServiceNow instance REST endpoints
- Optional: Custom incident forms and business rules

**ServiceNow API Endpoints Used:**
- `GET/POST /api/now/table/incident` - Incident CRUD operations
- `PUT/PATCH /api/now/table/incident/{sys_id}` - Incident updates
- Query parameters: `sysparm_limit`, `sysparm_offset`, `sysparm_query`, `sysparm_orderby`

**ServiceNow Developer Resources:**
- [ServiceNow Developer Portal](https://developer.servicenow.com/dev.do) - Official documentation, tutorials, and API references for ServiceNow development and integration

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Access to Azure OpenAI service
- GitHub Personal Access Token
- Elasticsearch cluster (optional, for log analysis)
- ServiceNow instance (optional, for case management)
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
   
   **Option A: Semantic Kernel (Recommended)**
   ```bash
   python chat_sk.py
   ```
   
   **Option B: LangGraph (Legacy)**
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

### ServiceNow Incident Management
```
User: Do I have any open incidents?
Assistant: Open Incidents - Page 1 (showing 1-5):

- Incident INC0001234: Database connection timeout
  Priority: 1, Urgency: 1, Impact: 2, State: 2

- Incident INC0001235: API rate limiting errors  
  Priority: 2, Urgency: 2, Impact: 2, State: 1

More incidents available. Use query_open_incidents with page_number='2' to continue.

User: Create an incident for the new authentication service failing
Assistant: ✅ Incident Created Successfully!
Incident Number: INC0001236
System ID: abc123def456ghi789
Priority: 3 (Medium)

The incident has been logged and is now in "New" status.

User: Search for incidents containing ContosoBankAPI
Assistant: Search Results for 'ContosoBankAPI' - Page 1 (showing 1-3):

- Incident INC0001220: ContosoBankAPI authentication timeouts
  Priority: 1, Urgency: 1, Impact: 2, State: 6
  
- Incident INC0001225: ContosoBankAPI rate limiting issues
  Priority: 2, Urgency: 2, Impact: 2, State: 2

User: Add a comment to incident INC0001234 that we've identified the root cause
Assistant: ✅ Comment Added Successfully!
Added comment to incident INC0001234: "Root cause identified: Database connection pool exhausted during peak load times."

User: Show me high priority incidents
Assistant: High Priority Incidents - Page 1 (showing 1-2):

- Incident INC0001234: Database connection timeout
  Priority: 1, Urgency: 1, Impact: 2, State: 2
  
- Incident INC0001235: API rate limiting errors
  Priority: 2, Urgency: 2, Impact: 2, State: 1

User: Resolve incident INC0001234 
Assistant: ✅ Incident INC0001234 Resolved Successfully!
Status updated to "Resolved" with resolution code "Solution provided"
```

### Advanced ServiceNow Operations
```
User: Assign incident INC0001235 to john.smith
Assistant: ✅ Incident INC0001235 assigned successfully to john.smith

User: Show me page 2 of open incidents with page size 10
Assistant: Open Incidents - Page 2 (showing 11-20):
[Lists next 10 incidents...]

User: Close incident INC0001234 with resolution "Database connection pool tuned"
Assistant: ✅ Incident INC0001234 closed successfully!
Resolution: "Database connection pool tuned"
Final State: Closed
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

### Troubleshooting

#### ServiceNow Common Issues

**Connection Issues:**
```bash
# Test ServiceNow connection
User: Test ServiceNow connection
Assistant: ✅ ServiceNow Connection Test: SUCCESS
Sample incident: INC0001234 - Database connection timeout
Found 1 incident(s) in test query
```

**Authentication Problems:**
- Verify `SERVICENOW_INSTANCE` URL format (without https://)
- Check username/password or API token validity
- Ensure user has required ServiceNow roles
- Verify network connectivity to ServiceNow instance

**API Limitations:**
- ServiceNow instances may have API rate limits
- Some fields may be read-only based on user permissions
- Custom incident forms may require additional field mappings

**Performance Optimization:**
- Use paging for large incident datasets (default: 20 per page)
- Leverage ServiceNow's encoded query syntax for complex filters
- Consider using API tokens instead of username/password for better performance

#### GitHub Integration Issues
- Verify GitHub PAT has correct repository permissions
- Check for API rate limiting (5000 requests/hour for authenticated users)
- Ensure repository names and usernames are correct

#### Elasticsearch Connectivity
- Verify Elasticsearch cluster accessibility
- Check index names and field mappings
- Validate KQL query syntax for log searches

## 🔐 Security Best Practices

### ServiceNow Security
- **Use API Tokens**: Prefer API tokens over username/password authentication
- **Principle of Least Privilege**: Grant minimum required ServiceNow roles
- **Network Security**: Use HTTPS for all ServiceNow API communications
- **Credential Rotation**: Regularly rotate ServiceNow API tokens and passwords
- **Audit Logging**: Enable ServiceNow audit logs for API access tracking

### General Security Guidelines
- **Environment Variables**: Store all sensitive credentials in `.env` files
- **Version Control**: Never commit credentials to Git repositories  
- **Access Control**: Use least-privilege GitHub Personal Access Tokens
- **Network Security**: Ensure all external APIs use encrypted connections
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