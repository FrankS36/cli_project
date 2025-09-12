#!/bin/bash

# MCP System Test Runner
# This script runs the comprehensive MCP system tests with observability

echo "🧪 MCP System Test Runner"
echo "=========================="
echo ""

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Activating..."
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "✅ Activated venv"
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "✅ Activated .venv"
    else
        echo "❌ No virtual environment found. Please run:"
        echo "   python -m venv venv && source venv/bin/activate"
        exit 1
    fi
fi

echo ""
echo "🚀 Starting MCP system tests..."
echo ""

# Run the test suite
if command -v uv &> /dev/null; then
    echo "📦 Using uv to run tests..."
    uv run python test_mcp_system.py
else
    echo "📦 Using python to run tests..."
    python test_mcp_system.py
fi

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed!"
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
fi
