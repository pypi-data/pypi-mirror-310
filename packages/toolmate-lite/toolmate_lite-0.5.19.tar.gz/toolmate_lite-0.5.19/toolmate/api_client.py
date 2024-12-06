import requests, argparse, json, sys
from toolmate import config

# Create the parser
parser = argparse.ArgumentParser(description="ToolMate AI API client cli options")
# Add arguments
parser.add_argument("default", nargs="?", default=None, help="instruction sent to ToolMate API server")
parser.add_argument('-a', '--all', action='store', dest='all', help="display the whole conversation; either 'plain' or 'json'")
parser.add_argument('-c', '--chat', action='store', dest='chat', help="set 'true' to chat as an on-going conversation")
parser.add_argument('-k', '--key', action='store', dest='key', help="API key")
parser.add_argument('-p', '--port', action='store', dest='port', help="server port")
parser.add_argument('-s', '--server', action='store', dest='server', help="server address; 'http://localhost' by default")
parser.add_argument('-t', '--tools', action='store', dest='tools', help="search enabled tools; '@' to display all; regex pattern to filter")
# Parse arguments
args = parser.parse_args()

def chat():
    main(True if not (args.chat is not None and args.chat.lower() == "false") else False)

def main(chat: bool = False):
    cliDefault = args.default.strip() if args.default is not None and args.default.strip() else ""
    stdin_text = sys.stdin.read() if not sys.stdin.isatty() else ""

    if args.tools is not None and args.tools.strip(): # search tools; ignore all other arguments
        query = args.tools.strip().lower()
        endpoint = f"{args.server if args.server else config.toolmate_api_client_host}:{args.port if args.port else config.toolmate_api_client_port}/api/tools"

        url = f"""{endpoint}?query={query}"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": args.key if args.key else config.toolmate_api_client_key,
        }
        response = requests.post(url, headers=headers)
        print(json.loads(response.json())["tools"])

    elif (cliDefault + stdin_text):
        query = cliDefault + stdin_text
        endpoint = f"{args.server if args.server else config.toolmate_api_client_host}:{args.port if args.port else config.toolmate_api_client_port}/api/toolmate"
        if args.chat:
            chat = True

        url = f"""{endpoint}?chat={chat}&query={query}"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": args.key if args.key else config.toolmate_api_client_key,
        }
        response = requests.post(url, headers=headers)

        #response = requests.post(endpoint, json=prompt)
        if args.all and args.all.lower() in ("plain", "json"):
            if args.all.lower() == "plain":
                for i in json.loads(response.json()):
                    role = i.get("role", "")
                    content = i.get("content", "")
                    print(f"```{role}\n{content.rstrip()}\n```")
            elif args.all.lower() == "json":
                print(response.json())
        else:
            print(json.loads(response.json())[-1]["content"])

if __name__ == '__main__':
    main()
