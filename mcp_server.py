from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.tool(
    name="list_documents",
    description="List all available document IDs"
)
def list_documents():
    return list(docs.keys())

@mcp.resource(
    uri="docs://list",
    name="Document List",
    description="A list of all document ids"
)
def list_docs():
    return list(docs.keys())

@mcp.resource(
    uri="docs://content/{doc_id}",
    name="Document Content",
    description="The content of a specific document"
)
def get_doc_content(doc_id: str):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

@mcp.prompt(
    name="markdown_rewrite",
    description="Rewrite a document's content in markdown format"
)
def markdown_rewrite(
    doc_id: str = Field(description="Id of the document to rewrite"),
    system: str = Field(description="System prompt for the model"),
    model: str = Field(description="Model to use for rewriting")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    content = docs[doc_id]
    return {
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": f"Please rewrite the following content in markdown format:\n\n{content}"
            }
        ],
        "model": model
    }

@mcp.prompt(
    name="summarize_doc",
    description="Summarize a document's content"
)
def summarize_doc(
    doc_id: str = Field(description="Id of the document to summarize"),
    system: str = Field(description="System prompt for the model"),
    model: str = Field(description="Model to use for summarizing")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    content = docs[doc_id]
    return {
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": f"Please summarize the following content:\n\n{content}"
            }
        ],
        "model": model
    }
    
@mcp.prompt(
    name="extract_key_points",
    description="Extract key points from a document's content"
)
def extract_key_points(
    doc_id: str = Field(description="Id of the document to analyze"),
    system: str = Field(description="System prompt for the model"),
    model: str = Field(description="Model to use for extraction")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    content = docs[doc_id]
    return {
        "system": system,
        "messages": [
            {
                "role": "user", 
                "content": f"Please extract and list the key points from the following content:\n\n{content}"
            }
        ],
        "model": model
    }




if __name__ == "__main__":
    mcp.run(transport="stdio")
