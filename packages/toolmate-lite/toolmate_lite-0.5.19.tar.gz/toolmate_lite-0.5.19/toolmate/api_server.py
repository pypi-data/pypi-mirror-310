from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from toolmate import config
from toolmate.utils.assistant import ToolMate
import requests, argparse, json, uvicorn, re


# Create the parser
parser = argparse.ArgumentParser(description="ToolMate AI API server cli options")
# Add arguments
parser.add_argument('-b', '--backend', action='store', dest='backend', help="AI backend")
parser.add_argument('-k', '--key', action='store', dest='key', help="API key")
parser.add_argument('-p', '--port', action='store', dest='port', help="server port")
parser.add_argument('-s', '--server', action='store', dest='server', help="server address; '0.0.0.0' by default")
# Parse arguments
args = parser.parse_args()

# app object
app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key") 

# Function to check the API key
async def get_api_key(api_key: str = Depends(api_key_header)):
    correct_key = args.key if args.key else config.toolmate_api_server_key
    if api_key != correct_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

@app.post("/api/toolmate")
async def process_query(query: str, chat: str = "false", api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    if query := query.strip():
        config.toolmate.runMultipleActions(query)
        response = [i for i in config.currentMessages if not i.get("role", "") == "system"]
        if not chat.lower == "true":
            config.currentMessages = config.toolmate.resetMessages()
        return json.dumps(response)

@app.post("/api/tools")
async def process_tools(query: str, api_key: str = Depends(get_api_key) if config.toolmate_api_server_key else ""):
    if query := query.strip():
        searchPattern = query.strip().lower()
        if searchPattern == "@":
            tools = config.allEnabledTools
        else:
            tools = [i for i in config.allEnabledTools if re.search(searchPattern, i)]
        return json.dumps({"tools": tools})

def main():
    config.initialCompletionCheck = False
    backends = ("llamacpp", "llamacppserver", "ollama", "groq", "googleai", "vertexai", "chatgpt", "letmedoit")
    if args.backend and args.backend.lower() in backends:
        config.llmInterface = args.backend.lower()
    config.toolmate = ToolMate()
    # TODO
    uvicorn.run(app, host=args.server if args.server else config.toolmate_api_server_host, port=args.port if args.port else config.toolmate_api_server_port) 

if __name__ == '__main__':
    main()
