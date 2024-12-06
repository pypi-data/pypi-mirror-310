from flask import Flask, request, jsonify
from toolmate import config
import requests, argparse

# Create the parser
parser = argparse.ArgumentParser(description="ToolMate AI API server/client cli options")
# Add arguments
parser.add_argument("default", nargs="?", default=None, help="instruction sent to ToolMate API server; applicable to client only")
parser.add_argument('-a', '--all', action='store', dest='all', help="output the whole conversation instead of the last response; either 'plain' or 'json'; applicable to client only")
parser.add_argument('-b', '--backend', action='store', dest='backend', help="AI backend; applicable to server only")
parser.add_argument('-k', '--key', action='store', dest='key', help="API key; applicable to both server and client")
parser.add_argument('-p', '--port', action='store', dest='port', help="API port; applicable to both server and client")
parser.add_argument('-r', '--run', action='store', dest='run', help="run API server; set true/false to enable/disable debug feature; applicable to server only")
parser.add_argument('-s', '--server', action='store', dest='server', help="specify the API server to be connected; applicable to client only")
# Parse arguments
args = parser.parse_args()

# app object
app = Flask(__name__)

@app.route("/api/toolmate", methods=["POST"])
def process_query():
    data = request.get_json() 
    key = data.get("key", "")
    query = data.get("query", "")

    rightKey = args.key if args.key else config.toolmate_api_server_key
    if key != rightKey:
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized

    if query := query.strip():
        config.toolmate.runMultipleActions(query)
        response = [i for i in config.currentMessages if not i.get("role", "") == "system"]
        config.currentMessages = config.toolmate.resetMessages()
        return jsonify(response)

def main():
    if args.run:
        from toolmate.utils.assistant import ToolMate
        config.initialCompletionCheck = False
        backends = ("llamacpp", "llamacppserver", "ollama", "groq", "googleai", "vertexai", "chatgpt", "letmedoit")
        if args.backend and args.backend.lower() in backends:
            config.llmInterface = args.backend.lower()
        config.toolmate = ToolMate()
        app.run(debug=True if args.run.lower() == "true" else False, port=args.port if args.port else config.toolmate_api_server_port)
    elif args.default is not None and args.default.strip():
        prompt = {"key": args.key if args.key else config.toolmate_api_client_key, "query": args.default.strip()}
        endpoint = f"{args.server if args.server else config.toolmate_api_client_host}:{args.port if args.port else config.toolmate_api_client_port}/api/toolmate"
        response = requests.post(endpoint, json=prompt)
        if args.all and args.all.lower() in ("plain", "json"):
            if args.all.lower() == "plain":
                for i in response.json():
                    role = i.get("role", "")
                    content = i.get("content", "")
                    print(f"```{role}\n{content.rstrip()}\n```")
            elif args.all.lower() == "json":
                print(response.text)
        else:
            print(response.json()[-1]["content"])

if __name__ == '__main__':
    main()
