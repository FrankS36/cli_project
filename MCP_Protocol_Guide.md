# MCP Protocol Guide: Understanding the Debug Output

This document explains the Model Context Protocol (MCP) concepts and what you can learn from the debug output in this CLI application.

## Table of Contents
- [Overview](#overview)
- [Core MCP Concepts](#core-mcp-concepts)
- [Debug Output Explained](#debug-output-explained)
- [Tool Discovery Process](#tool-discovery-process)
- [Tool Execution Process](#tool-execution-process)
- [MCP Data Structures](#mcp-data-structures)
- [Practical Examples](#practical-examples)

## Overview

The Model Context Protocol (MCP) is a standardized way for AI applications to connect to external data sources and tools. It enables:
- **Tool Discovery**: Finding available tools from MCP servers
- **Tool Execution**: Calling tools with parameters and getting results
- **Resource Access**: Reading data from external sources
- **Prompt Templates**: Using predefined prompts from servers

## Core MCP Concepts

### 1. **Client-Server Architecture**
- **MCP Client**: Your CLI application that requests tools and data
- **MCP Server**: External service that provides tools and resources
- **Transport**: Communication layer (stdio, HTTP, WebSocket)

### 2. **Tools**
- **Definition**: Functions provided by MCP servers
- **Schema**: JSON schema defining input parameters
- **Execution**: Client calls tools with parameters, server returns results

### 3. **Resources**
- **Definition**: Data sources (files, databases, APIs)
- **URI-based**: Accessed via unique resource identifiers
- **Content**: Can be text, binary, or structured data

## Debug Output Explained

### Tool Discovery Debug Output

When you see:
```
DEBUG - list_tools() result: ListToolsResult(...)
```

**What's happening:**
1. Client requests available tools from MCP server
2. Server responds with tool definitions
3. Each tool includes name, description, and input schema

**Key Fields:**
- `meta`: Protocol metadata (usually None for simple operations)
- `nextCursor`: Pagination token for large tool lists
- `tools`: Array of available tool definitions

### Tool Execution Debug Output

When you see:
```
DEBUG - calling tool 'read_doc_contents' with input: {'doc_id': 'report.pdf'}
DEBUG - call_tool() result: CallToolResult(...)
```

**What's happening:**
1. Client sends tool name and parameters to server
2. Server executes the tool
3. Server returns result with content or error information

## Tool Discovery Process

### 1. **ListToolsResult Structure**
```python
ListToolsResult(
    meta=None,                    # Protocol metadata
    nextCursor=None,              # Pagination cursor
    tools=[                       # Available tools
        Tool(
            name='read_doc_contents',
            description='Read the contents of a document...',
            inputSchema={...}     # JSON schema for parameters
        ),
        Tool(
            name='edit_document',
            description='Edit a document by replacing...',
            inputSchema={...}
        )
    ]
)
```

### 2. **Tool Schema Example**
```json
{
    "properties": {
        "doc_id": {
            "description": "Id of the document to read",
            "title": "Doc Id",
            "type": "string"
        }
    },
    "required": ["doc_id"],
    "title": "read_documentArguments",
    "type": "object"
}
```

## Tool Execution Process

### 1. **Tool Call Request**
```python
# Client sends
tool_name = "read_doc_contents"
tool_input = {"doc_id": "report.pdf"}
```

### 2. **Tool Call Response**
```python
CallToolResult(
    meta=None,                    # Protocol metadata
    content=[                     # Result content
        TextContent(
            type='text',
            text='The report details the state of a 20m condenser tower.',
            annotations=None
        )
    ],
    isError=False                 # Success/failure indicator
)
```

## MCP Data Structures

### Core Types

#### **Tool**
```python
Tool(
    name: str,                    # Unique tool identifier
    description: str,             # Human-readable description
    inputSchema: dict,            # JSON schema for parameters
    annotations: Optional[dict]   # Additional metadata
)
```

#### **CallToolResult**
```python
CallToolResult(
    meta: Optional[dict],         # Protocol metadata
    content: List[Content],       # Result content blocks
    isError: bool                 # Success/failure flag
)
```

#### **Content Types**
- **TextContent**: Plain text results
- **ImageContent**: Image data
- **ResourceContent**: References to resources

### Error Handling

When `isError=True`, the content contains error information:
```python
CallToolResult(
    meta=None,
    content=[
        TextContent(
            type='text',
            text='Error: Document not found: invalid.pdf'
        )
    ],
    isError=True
)
```

## Practical Examples

### Example 1: Reading a Document

**Debug Output:**
```
DEBUG - list_tools() result: ListToolsResult(meta=None, nextCursor=None, tools=[...])
DEBUG - calling tool 'read_doc_contents' with input: {'doc_id': 'report.pdf'}
DEBUG - call_tool() result: CallToolResult(meta=None, content=[TextContent(type='text', text='The report details...', annotations=None)], isError=False)
```

**What you learn:**
1. Tool discovery found the `read_doc_contents` tool
2. Client called tool with document ID parameter
3. Server successfully returned document content
4. No errors occurred (`isError=False`)

### Example 2: Editing a Document

**Debug Output:**
```
DEBUG - calling tool 'edit_document' with input: {'doc_id': 'plan.md', 'old_str': 'phase 1', 'new_str': 'phase one'}
DEBUG - call_tool() result: CallToolResult(meta=None, content=[TextContent(type='text', text='Document edited successfully', annotations=None)], isError=False)
```

**What you learn:**
1. Edit tool requires three parameters: doc_id, old_str, new_str
2. Server processed the text replacement
3. Operation completed successfully

## Advanced Concepts

### 1. **Resource URIs**
- Format: `mcp://server-name/resource-type/resource-id`
- Example: `mcp://docs/file/report.pdf`

### 2. **Prompt Templates**
- Predefined prompts with parameters
- Reusable across different contexts
- Can include tool recommendations

### 3. **Server Capabilities**
- Tools: What functions are available
- Resources: What data can be accessed
- Prompts: What templates are provided

## Best Practices

### 1. **Error Handling**
Always check `isError` before processing content:
```python
result = await client.call_tool(tool_name, params)
if result.isError:
    handle_error(result.content)
else:
    process_success(result.content)
```

### 2. **Schema Validation**
Validate input against tool schema before calling:
```python
# Check required parameters exist
# Validate parameter types
# Handle optional parameters
```

### 3. **Resource Management**
- Close client connections properly
- Handle connection timeouts
- Implement retry logic for network issues

## Debugging Tips

### 1. **Understanding Output**
- Look for `DEBUG - list_tools()` to see tool discovery
- Look for `DEBUG - calling tool` to see tool execution
- Check `isError` field in results

### 2. **Common Issues**
- **Missing tools**: Check if MCP server is running
- **Parameter errors**: Validate against inputSchema
- **Connection issues**: Check transport configuration

### 3. **Performance**
- Tool discovery is cached per session
- Multiple tool calls reuse the same connection
- Consider tool call batching for efficiency

## Conclusion

Understanding MCP protocol helps you:
- Debug connection and tool issues
- Design better tool integrations
- Optimize performance
- Build robust error handling

The debug output provides valuable insights into the protocol flow and helps you understand how your application interacts with MCP servers.
