# MCP Inspector Guide: Testing Your MCP Server

This guide explains how to use the MCP Inspector to test, debug, and understand your MCP server implementation.

## Table of Contents
- [What is the MCP Inspector?](#what-is-the-mcp-inspector)
- [Starting the Inspector](#starting-the-inspector)
- [Inspector Interface Overview](#inspector-interface-overview)
- [Testing Tools](#testing-tools)
- [Testing Resources](#testing-resources)
- [Testing Prompts](#testing-prompts)
- [Understanding Results](#understanding-results)
- [Debugging Tips](#debugging-tips)
- [Common Issues](#common-issues)

## What is the MCP Inspector?

The MCP Inspector is a web-based tool that provides a graphical interface for:
- **Discovering** available tools, resources, and prompts
- **Testing** MCP server functionality interactively
- **Debugging** MCP protocol interactions
- **Understanding** data structures and schemas

It acts as a visual client that connects to your MCP server, allowing you to explore and test all capabilities without writing code.

## Starting the Inspector

### 1. Start the Inspector
```bash
mcp dev mcp_server.py
```

This command will:
- Start your MCP server
- Launch the inspector proxy
- Open a web interface
- Display connection information

### 2. Expected Output
```
Starting MCP inspector...
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: [your-session-token]
🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=[token]
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

### 3. Access the Inspector
Open your browser to: **http://localhost:6274**

## Inspector Interface Overview

### Main Sections

1. **Connection Panel** (Left Side)
   - Server configuration
   - Connection status
   - Authentication settings

2. **Tools Tab**
   - List of available tools
   - Tool schemas and parameters
   - Execute tools with inputs

3. **Resources Tab**
   - Available resources
   - Resource URIs and metadata
   - Read resource content

4. **Prompts Tab** 
   - Available prompt templates
   - Prompt parameters and usage
   - Execute prompts with arguments

5. **History Panel**
   - Previous requests and responses
   - Request/response timing
   - Error messages

## Testing Tools

### Available Tools in Your MCP Server

#### 1. `list_documents`
**Purpose:** Get all available document IDs

**How to Test:**
1. Go to the **Tools** tab
2. Find `list_documents` in the list
3. Click on the tool name
4. Click **"Execute"** (no parameters needed)

**Expected Result:**
```json
[
  "deposition.md",
  "report.pdf", 
  "financials.docx",
  "outlook.pdf",
  "plan.md",
  "spec.txt"
]
```

#### 2. `read_doc_contents`
**Purpose:** Read the content of a specific document

**How to Test:**
1. Go to the **Tools** tab
2. Find `read_doc_contents`
3. Click on the tool name
4. Fill in the parameter:
   - `doc_id`: `"report.pdf"` (or any document ID)
5. Click **"Execute"**

**Expected Result:**
```
"The report details the state of a 20m condenser tower."
```

#### 3. `edit_document`
**Purpose:** Replace text within a document

**How to Test:**
1. Go to the **Tools** tab
2. Find `edit_document`
3. Click on the tool name
4. Fill in the parameters:
   - `doc_id`: `"plan.md"`
   - `old_str`: `"steps"`
   - `new_str`: `"phases"`
5. Click **"Execute"**

**Expected Result:**
The document content will be updated with the text replacement.

### Understanding Tool Schemas

Each tool displays its **input schema** showing:
- **Required parameters** (marked with *)
- **Parameter types** (string, number, etc.)
- **Descriptions** for each parameter
- **Validation rules**

Example schema for `read_doc_contents`:
```json
{
  "properties": {
    "doc_id": {
      "type": "string",
      "description": "Id of the document to read",
      "title": "Doc Id"
    }
  },
  "required": ["doc_id"],
  "type": "object"
}
```

## Testing Resources

### Available Resources

#### 1. `docs://list`
**Purpose:** Resource containing list of all document IDs

**How to Test:**
1. Go to the **Resources** tab
2. Find `docs://list` in the list
3. Click on the resource
4. Click **"Read Resource"**

**Expected Result:**
```json
[
  "deposition.md",
  "report.pdf",
  "financials.docx", 
  "outlook.pdf",
  "plan.md",
  "spec.txt"
]
```

#### 2. `docs://content/{doc_id}`
**Purpose:** Resource containing specific document content

**How to Test:**
1. Go to the **Resources** tab
2. In the URI field, enter: `docs://content/report.pdf`
3. Click **"Read Resource"**

**Expected Result:**
```
"The report details the state of a 20m condenser tower."
```

### Resource Metadata

Resources show important metadata:
- **URI**: The resource identifier
- **Name**: Human-readable name
- **Description**: What the resource contains
- **MIME Type**: Content type (e.g., text/plain)

## Testing Prompts

### Available Prompts

#### 1. `markdown_rewrite`
**Purpose:** Convert document content to markdown format

**How to Test:**
1. Go to the **Prompts** tab
2. Find `markdown_rewrite`
3. Fill in parameters:
   - `doc_id`: `"report.pdf"`
   - `system`: `"You are a markdown formatting expert"`
   - `model`: `"claude-3-5-sonnet-20241022"`
4. Click **"Execute"**

#### 2. `summarize_doc`
**Purpose:** Generate a summary of document content

**How to Test:**
1. Go to the **Prompts** tab
2. Find `summarize_doc`
3. Fill in parameters:
   - `doc_id`: `"financials.docx"`
   - `system`: `"You are a financial analyst"`
   - `model`: `"claude-3-5-sonnet-20241022"`
4. Click **"Execute"**

## Understanding Results

### Successful Responses

**Tool Results:**
- Show the actual returned data
- Include execution metadata
- Display timing information

**Resource Results:**
- Show resource content
- Include MIME type information
- Display resource metadata

**Prompt Results:**
- Return formatted prompt templates
- Include system instructions
- Show model parameters

### Error Responses

**Common Error Types:**
```json
{
  "error": "Doc with id nonexistent.doc not found",
  "type": "ValueError"
}
```

**Resource Errors:**
```json
{
  "error": "Unknown resource: docs://invalid"
}
```

## Debugging Tips

### 1. Check Connection Status
- Green indicator = Connected
- Red indicator = Connection failed
- Look for error messages in the connection panel

### 2. Verify Tool Parameters
- Ensure all required parameters are provided
- Check parameter types match the schema
- Use exact string matches for document IDs

### 3. Monitor Console Output
The terminal running the inspector shows detailed logs:
```
Received POST message for sessionId 823d4253-5788-4140-8499-e8c11a6f6904
STDIO transport: command=uv, args=run,--with,mcp,mcp,run,mcp_server.py
Created server transport
Created client transport
```

### 4. Use Browser Developer Tools
- Press F12 to open developer tools
- Check Network tab for HTTP requests
- Look for JavaScript errors in Console

### 5. Test with Known Good Values
Start with these working examples:
- Tool: `list_documents` (no parameters)
- Resource: `docs://list`
- Document ID: `report.pdf`

## Common Issues

### Issue: Connection Failed
**Symptoms:** Red connection indicator, no tools/resources visible

**Solutions:**
1. Ensure MCP server is running: `mcp dev mcp_server.py`
2. Check if port 6274 is available
3. Restart the inspector
4. Clear browser cache

### Issue: "spawn uv ENOENT" Error
**Symptoms:** Error messages about `uv` command not found

**Solutions:**
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Add to PATH: `source $HOME/.local/bin/env`
3. Use Python directly: `python mcp_server.py`

### Issue: Tool Returns Error
**Symptoms:** Tool execution shows error response

**Solutions:**
1. Check parameter spelling and types
2. Verify document IDs exist using `list_documents`
3. Check server logs for detailed error messages
4. Ensure all required parameters are provided

### Issue: Empty Results
**Symptoms:** Tool executes but returns empty or null results

**Solutions:**
1. Check if the document/resource exists
2. Verify server implementation
3. Test with different parameters
4. Check server logs for warnings

## Advanced Usage

### Testing Custom Documents
1. Add new documents to `mcp_server.py`:
```python
docs = {
    "your_doc.txt": "Your custom content here",
    # ... existing docs
}
```

2. Restart the inspector
3. Test with `doc_id`: `"your_doc.txt"`

### Performance Testing
- Use the History panel to monitor response times
- Test with larger documents to check performance
- Monitor memory usage with multiple requests

### Schema Validation
- Try invalid parameters to test error handling
- Test edge cases like empty strings
- Verify type validation works correctly

## Best Practices

### 1. Start Simple
- Begin with `list_documents` tool
- Test basic resources first
- Gradually try more complex operations

### 2. Understand the Schema
- Read tool descriptions carefully
- Check required vs optional parameters
- Understand data types and formats

### 3. Use Realistic Data
- Test with actual document content
- Use meaningful parameter values
- Test both success and error scenarios

### 4. Monitor Performance
- Check response times
- Test with multiple concurrent requests
- Monitor resource usage

### 5. Document Your Tests
- Keep track of working parameter combinations
- Note any issues or limitations
- Document expected vs actual results

## Conclusion

The MCP Inspector is a powerful tool for understanding and testing your MCP server implementation. Use it to:

- **Explore** available tools, resources, and prompts
- **Test** functionality interactively
- **Debug** issues and understand data flow
- **Validate** your MCP server implementation

Regular testing with the inspector ensures your MCP server works correctly and helps you understand the protocol better.

---

**Next Steps:**
- Try the automated test suite: `./run_tests.sh`
- Read the MCP Protocol Guide: `MCP_Protocol_Guide.md`
- Explore the CLI application: `uv run main.py`
