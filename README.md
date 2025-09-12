# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

## 🧪 Testing & Observability

### Comprehensive Test Suite

This project includes a comprehensive test suite with detailed observability to help you understand exactly how the MCP system works.

#### Running Tests

**Quick Test Run:**
```bash
./run_tests.sh
```

**Direct Execution:**
```bash
python test_mcp_system.py
```

**With UV:**
```bash
uv run python test_mcp_system.py
```

#### What the Tests Cover

The test suite includes **8 comprehensive test categories**:

1. **🔌 MCP Server Connection** - Basic connectivity testing
2. **🔍 Tool Discovery** - Finding and analyzing available tools
3. **📚 Resource Discovery** - Finding and analyzing available resources
4. **📝 List Documents Tool** - Testing the document listing functionality
5. **📖 Read Document Tool** - Testing document content retrieval
6. **📋 Resource Reading** - Testing direct resource access
7. **🎯 Full CLI Integration** - End-to-end system testing
8. **🚨 Error Handling** - Testing failure scenarios

#### Understanding Test Output

The test output provides **detailed observability** into the MCP protocol:

**Real-time Protocol Inspection:**
```
DEBUG - list_tools() result: meta=None nextCursor=None tools=[...]
DEBUG - calling tool 'list_documents' with input: {}
DEBUG - call_tool() result: meta=None content=[...] isError=False
```

**Performance Metrics:**
```
[04:33:19.446] SUCCESS: ✅ Test #2 PASSED: Tool Discovery
  duration_ms: 376.59
  result: Found 3 tools
```

**Complete Tool Analysis:**
```
📋 Found 3 tools
  tool_names: ["read_doc_contents", "edit_document", "list_documents"]
  tool_details: [complete JSON schemas for each tool]
```

#### Learning from Tests

The test suite is designed to be **educational**. Each test explains:

- **What's happening** at the protocol level
- **How tools are discovered** and executed
- **How resources are accessed** and parsed
- **What data structures** are used
- **How errors are handled**

#### Test Reports

Tests automatically generate detailed JSON reports:
- **`test_report_YYYYMMDD_HHMMSS.json`** - Complete test execution log
- **Performance metrics** for each test
- **Protocol-level details** for debugging
- **Success/failure analysis**

#### Using Tests for Development

**For Learning MCP:**
1. Run tests to see complete protocol flow
2. Study the debug output to understand data structures
3. Examine test reports for detailed analysis

**For Debugging:**
1. Run tests after code changes
2. Check specific test categories that relate to your changes
3. Use detailed logs to identify issues

**For Verification:**
1. Ensure all components work together
2. Validate error handling
3. Confirm performance characteristics

### Example Test Output

```bash
🧪 MCP System Test Suite - Automated Testing with Observability
================================================================================
[04:33:18.682] INFO: 🚀 Starting MCP System Test Suite
[04:33:19.446] SUCCESS: 📋 Found 3 tools
[04:33:21.372] SUCCESS: 🛠️ Tool manager found 3 tools

================================================================================
🏁 TEST SUMMARY
================================================================================
Total Tests: 8
Passed: 7
Failed: 1
Success Rate: 87.5%
Total Duration: 3.07 seconds
================================================================================
```

#### Quick Test Reference

**Available Test Files:**
- `test_mcp_system.py` - Main comprehensive test suite
- `run_tests.sh` - Automated test runner script
- `test_report_*.json` - Generated test reports
- `MCP_Protocol_Guide.md` - Detailed protocol documentation

**Test Features:**
- 🎯 **8 test categories** covering all MCP functionality
- 🔍 **Real-time protocol inspection** with debug output
- ⚡ **Performance metrics** for each operation
- 📊 **JSON test reports** with detailed logs
- 🎨 **Color-coded console output** for easy reading
- 🚨 **Error scenario testing** for robust validation

**Quick Commands:**
```bash
# Run all tests with observability
./run_tests.sh

# Test specific functionality
python test_mcp_system.py

# View generated test report
cat test_report_*.json | jq .summary
```

### Linting and Typing Check

There are no lint or type checks implemented.
