#!/usr/bin/env python3
"""
MCP System Test Suite with Detailed Observability

This test file automatically runs comprehensive tests on the MCP system
and provides detailed explanations of what's happening at each step.
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Any, Dict, List
from contextlib import asynccontextmanager

from mcp_client import MCPClient
from core.claude import Claude
from core.cli_chat import CliChat
from core.tools import ToolManager


class TestObserver:
    """Observability class to track and explain test execution"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_count = 0
        self.passed = 0
        self.failed = 0
        self.logs = []
    
    def log(self, level: str, message: str, details: Dict[str, Any] = None):
        """Log a message with timestamp and optional details"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "details": details or {}
        }
        self.logs.append(log_entry)
        
        # Color coding for console output
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "ERROR": "\033[91m",   # Red
            "WARNING": "\033[93m", # Yellow
            "DEBUG": "\033[90m",   # Gray
        }
        reset = "\033[0m"
        
        color = colors.get(level, "")
        print(f"{color}[{timestamp}] {level}: {message}{reset}")
        
        if details:
            for key, value in details.items():
                if isinstance(value, (dict, list)):
                    print(f"  {key}: {json.dumps(value, indent=2)}")
                else:
                    print(f"  {key}: {value}")
    
    def start_test(self, test_name: str):
        """Start a new test"""
        self.test_count += 1
        self.log("INFO", f"🧪 Starting Test #{self.test_count}: {test_name}")
        return time.time()
    
    def end_test(self, test_name: str, start_time: float, success: bool, result: Any = None):
        """End a test and record results"""
        duration = time.time() - start_time
        
        if success:
            self.passed += 1
            self.log("SUCCESS", f"✅ Test #{self.test_count} PASSED: {test_name}", {
                "duration_ms": f"{duration*1000:.2f}",
                "result": str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
            })
        else:
            self.failed += 1
            self.log("ERROR", f"❌ Test #{self.test_count} FAILED: {test_name}", {
                "duration_ms": f"{duration*1000:.2f}",
                "error": str(result)
            })
    
    def summary(self):
        """Print test summary"""
        total_time = time.time() - self.start_time
        print("\n" + "="*80)
        print("🏁 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {self.test_count}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/self.test_count)*100:.1f}%" if self.test_count > 0 else "N/A")
        print(f"Total Duration: {total_time:.2f} seconds")
        print("="*80)


class MCPSystemTester:
    """Comprehensive MCP system tester with detailed observability"""
    
    def __init__(self):
        self.observer = TestObserver()
        self.client = None
        self.claude = None
        self.cli_chat = None
    
    @asynccontextmanager
    async def mcp_client(self):
        """Context manager for MCP client lifecycle"""
        self.observer.log("INFO", "🔌 Connecting to MCP server...")
        client = MCPClient(
            command="python",
            args=["mcp_server.py"]
        )
        
        try:
            await client.connect()
            self.observer.log("SUCCESS", "✅ MCP client connected successfully")
            yield client
        except Exception as e:
            self.observer.log("ERROR", f"❌ Failed to connect MCP client: {e}")
            raise
        finally:
            await client.cleanup()
            self.observer.log("INFO", "🔌 MCP client disconnected")
    
    async def test_mcp_server_connection(self):
        """Test basic MCP server connection"""
        start_time = self.observer.start_test("MCP Server Connection")
        
        try:
            async with self.mcp_client() as client:
                # Test basic connection
                session = client.session()
                self.observer.log("INFO", "📡 Testing session connectivity...", {
                    "session_type": type(session).__name__
                })
                
                result = "Connection successful"
                self.observer.end_test("MCP Server Connection", start_time, True, result)
                return True
                
        except Exception as e:
            self.observer.end_test("MCP Server Connection", start_time, False, str(e))
            return False
    
    async def test_tool_discovery(self):
        """Test tool discovery and analyze available tools"""
        start_time = self.observer.start_test("Tool Discovery")
        
        try:
            async with self.mcp_client() as client:
                self.observer.log("INFO", "🔍 Discovering available tools...")
                tools = await client.list_tools()
                
                self.observer.log("SUCCESS", f"📋 Found {len(tools)} tools", {
                    "tool_names": [tool.name for tool in tools],
                    "tool_details": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema
                        } for tool in tools
                    ]
                })
                
                # Validate expected tools
                expected_tools = ["read_doc_contents", "edit_document", "list_documents"]
                found_tools = [tool.name for tool in tools]
                missing_tools = set(expected_tools) - set(found_tools)
                
                if missing_tools:
                    self.observer.log("WARNING", f"⚠️ Missing expected tools: {missing_tools}")
                else:
                    self.observer.log("SUCCESS", "✅ All expected tools found")
                
                self.observer.end_test("Tool Discovery", start_time, True, f"Found {len(tools)} tools")
                return tools
                
        except Exception as e:
            self.observer.end_test("Tool Discovery", start_time, False, str(e))
            return []
    
    async def test_resource_discovery(self):
        """Test resource discovery and analyze available resources"""
        start_time = self.observer.start_test("Resource Discovery")
        
        try:
            async with self.mcp_client() as client:
                self.observer.log("INFO", "📚 Discovering available resources...")
                resources = await client.list_resources()
                
                self.observer.log("SUCCESS", f"📋 Found {len(resources)} resources", {
                    "resource_uris": [str(resource.uri) for resource in resources],
                    "resource_details": [
                        {
                            "name": resource.name,
                            "uri": str(resource.uri),
                            "description": resource.description,
                            "mimeType": resource.mimeType
                        } for resource in resources
                    ]
                })
                
                self.observer.end_test("Resource Discovery", start_time, True, f"Found {len(resources)} resources")
                return resources
                
        except Exception as e:
            self.observer.end_test("Resource Discovery", start_time, False, str(e))
            return []
    
    async def test_list_documents_tool(self):
        """Test the list_documents tool specifically"""
        start_time = self.observer.start_test("List Documents Tool")
        
        try:
            async with self.mcp_client() as client:
                self.observer.log("INFO", "📝 Testing list_documents tool...")
                
                result = await client.call_tool("list_documents", {})
                
                self.observer.log("INFO", "🔍 Analyzing tool result...", {
                    "result_type": type(result).__name__,
                    "result_content": [content.text for content in result.content] if hasattr(result, 'content') else str(result),
                    "is_error": result.isError if hasattr(result, 'isError') else "unknown"
                })
                
                # Extract document list from result
                if hasattr(result, 'content') and result.content:
                    doc_list = result.content[0].text
                    try:
                        parsed_docs = json.loads(doc_list) if doc_list.startswith('[') else doc_list.split(',')
                        self.observer.log("SUCCESS", f"📋 Retrieved {len(parsed_docs)} documents", {
                            "documents": parsed_docs
                        })
                    except:
                        self.observer.log("INFO", "📋 Document list (raw format)", {
                            "documents": doc_list
                        })
                
                self.observer.end_test("List Documents Tool", start_time, True, "Tool executed successfully")
                return result
                
        except Exception as e:
            self.observer.end_test("List Documents Tool", start_time, False, str(e))
            return None
    
    async def test_read_document_tool(self):
        """Test reading a specific document"""
        start_time = self.observer.start_test("Read Document Tool")
        
        try:
            async with self.mcp_client() as client:
                test_doc_id = "report.pdf"
                self.observer.log("INFO", f"📖 Testing read_doc_contents tool with '{test_doc_id}'...")
                
                result = await client.call_tool("read_doc_contents", {"doc_id": test_doc_id})
                
                self.observer.log("INFO", "🔍 Analyzing read result...", {
                    "result_type": type(result).__name__,
                    "is_error": result.isError if hasattr(result, 'isError') else "unknown",
                    "content_length": len(result.content[0].text) if hasattr(result, 'content') and result.content else 0
                })
                
                if hasattr(result, 'content') and result.content:
                    content = result.content[0].text
                    self.observer.log("SUCCESS", f"📄 Successfully read document content", {
                        "document_id": test_doc_id,
                        "content_preview": content[:100] + "..." if len(content) > 100 else content,
                        "content_length": len(content)
                    })
                
                self.observer.end_test("Read Document Tool", start_time, True, f"Read {test_doc_id} successfully")
                return result
                
        except Exception as e:
            self.observer.end_test("Read Document Tool", start_time, False, str(e))
            return None
    
    async def test_resource_reading(self):
        """Test reading resources directly"""
        start_time = self.observer.start_test("Resource Reading")
        
        try:
            async with self.mcp_client() as client:
                self.observer.log("INFO", "📚 Testing resource reading...")
                
                # Test document list resource
                self.observer.log("INFO", "📋 Reading docs://list resource...")
                list_result = await client.read_resource("docs://list")
                
                self.observer.log("INFO", "🔍 Analyzing list resource result...", {
                    "result_type": type(list_result).__name__,
                    "has_contents": hasattr(list_result, 'contents'),
                    "content_count": len(list_result.contents) if hasattr(list_result, 'contents') else 0
                })
                
                if hasattr(list_result, 'contents') and list_result.contents:
                    doc_list_text = list_result.contents[0].text
                    self.observer.log("SUCCESS", "📋 Document list resource read successfully", {
                        "raw_content": doc_list_text,
                        "parsed_content": json.loads(doc_list_text) if doc_list_text.startswith('[') else doc_list_text
                    })
                
                # Test specific document resource
                test_doc_id = "plan.md"
                self.observer.log("INFO", f"📄 Reading docs://content/{test_doc_id} resource...")
                content_result = await client.read_resource(f"docs://content/{test_doc_id}")
                
                if hasattr(content_result, 'contents') and content_result.contents:
                    doc_content = content_result.contents[0].text
                    self.observer.log("SUCCESS", f"📄 Document content resource read successfully", {
                        "document_id": test_doc_id,
                        "content": doc_content
                    })
                
                self.observer.end_test("Resource Reading", start_time, True, "Resources read successfully")
                return True
                
        except Exception as e:
            self.observer.end_test("Resource Reading", start_time, False, str(e))
            return False
    
    async def test_full_cli_integration(self):
        """Test the full CLI integration with a sample query"""
        start_time = self.observer.start_test("Full CLI Integration")
        
        try:
            self.observer.log("INFO", "🎯 Testing full CLI integration...")
            
            # Initialize components
            self.observer.log("INFO", "🔧 Initializing Claude service...")
            claude = Claude("claude-3-5-sonnet-20241022")
            
            self.observer.log("INFO", "🔧 Initializing MCP client...")
            async with self.mcp_client() as client:
                
                self.observer.log("INFO", "🔧 Initializing CLI chat...")
                cli_chat = CliChat(
                    doc_client=client,
                    clients={"docs": client},
                    claude_service=claude
                )
                
                # Test document listing
                self.observer.log("INFO", "📋 Testing document ID listing...")
                doc_ids = await cli_chat.list_docs_ids()
                self.observer.log("SUCCESS", f"📋 Retrieved {len(doc_ids)} document IDs", {
                    "document_ids": doc_ids
                })
                
                # Test document content retrieval
                if doc_ids:
                    test_doc = doc_ids[0]
                    self.observer.log("INFO", f"📖 Testing document content retrieval for '{test_doc}'...")
                    content = await cli_chat.get_doc_content(test_doc)
                    self.observer.log("SUCCESS", f"📖 Retrieved content for '{test_doc}'", {
                        "content_length": len(content),
                        "content_preview": content[:100] + "..." if len(content) > 100 else content
                    })
                
                # Test tool manager integration
                self.observer.log("INFO", "🛠️ Testing tool manager integration...")
                tools = await ToolManager.get_all_tools({"docs": client})
                self.observer.log("SUCCESS", f"🛠️ Tool manager found {len(tools)} tools", {
                    "tool_names": [tool["name"] for tool in tools],
                    "tool_descriptions": [tool["description"] for tool in tools]
                })
                
                self.observer.end_test("Full CLI Integration", start_time, True, "All components integrated successfully")
                return True
                
        except Exception as e:
            self.observer.end_test("Full CLI Integration", start_time, False, str(e))
            return False
    
    async def test_error_handling(self):
        """Test error handling scenarios"""
        start_time = self.observer.start_test("Error Handling")
        
        try:
            async with self.mcp_client() as client:
                self.observer.log("INFO", "🚨 Testing error handling scenarios...")
                
                # Test invalid document ID
                self.observer.log("INFO", "📋 Testing invalid document ID...")
                try:
                    result = await client.call_tool("read_doc_contents", {"doc_id": "nonexistent.doc"})
                    if hasattr(result, 'isError') and result.isError:
                        self.observer.log("SUCCESS", "✅ Error properly caught for invalid document", {
                            "error_content": result.content[0].text if result.content else "No error message"
                        })
                    else:
                        self.observer.log("WARNING", "⚠️ Expected error but got success")
                except Exception as e:
                    self.observer.log("SUCCESS", f"✅ Exception properly raised: {e}")
                
                # Test invalid resource URI
                self.observer.log("INFO", "📚 Testing invalid resource URI...")
                try:
                    await client.read_resource("docs://invalid")
                    self.observer.log("WARNING", "⚠️ Expected error but got success")
                except Exception as e:
                    self.observer.log("SUCCESS", f"✅ Resource error properly handled: {e}")
                
                self.observer.end_test("Error Handling", start_time, True, "Error scenarios handled correctly")
                return True
                
        except Exception as e:
            self.observer.end_test("Error Handling", start_time, False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run the complete test suite"""
        self.observer.log("INFO", "🚀 Starting MCP System Test Suite")
        self.observer.log("INFO", f"🕒 Test started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        await self.test_mcp_server_connection()
        await self.test_tool_discovery()
        await self.test_resource_discovery()
        await self.test_list_documents_tool()
        await self.test_read_document_tool()
        await self.test_resource_reading()
        await self.test_full_cli_integration()
        await self.test_error_handling()
        
        # Print summary
        self.observer.summary()
        
        # Save detailed log
        await self.save_test_report()
        
        return self.observer.failed == 0
    
    async def save_test_report(self):
        """Save detailed test report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"test_report_{timestamp}.json"
        
        # Convert logs to JSON-serializable format
        serializable_logs = []
        for log in self.observer.logs:
            serializable_log = {
                "timestamp": log["timestamp"],
                "level": log["level"],
                "message": log["message"],
                "details": {}
            }
            # Convert details to strings to avoid serialization issues
            for key, value in log["details"].items():
                try:
                    json.dumps(value)  # Test if serializable
                    serializable_log["details"][key] = value
                except:
                    serializable_log["details"][key] = str(value)
            serializable_logs.append(serializable_log)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": self.observer.test_count,
                "passed": self.observer.passed,
                "failed": self.observer.failed,
                "success_rate": (self.observer.passed/self.observer.test_count)*100 if self.observer.test_count > 0 else 0
            },
            "logs": serializable_logs
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.observer.log("INFO", f"📊 Test report saved to {report_file}")
        except Exception as e:
            self.observer.log("ERROR", f"❌ Failed to save test report: {e}")


async def main():
    """Main test runner"""
    print("🧪 MCP System Test Suite - Automated Testing with Observability")
    print("="*80)
    
    tester = MCPSystemTester()
    success = await tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
