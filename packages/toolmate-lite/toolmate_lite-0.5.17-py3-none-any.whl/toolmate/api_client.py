from toolmate import config
import requests, argparse

# Create the parser
parser = argparse.ArgumentParser(description="ToolMate AI API server/client cli options")
# Add arguments
parser.add_argument("default", nargs="?", default=None, help="instruction sent to ToolMate API server")
parser.add_argument('-a', '--all', action='store', dest='all', help="output the whole conversation instead of the last response; either 'plain' or 'json'")
parser.add_argument('-k', '--key', action='store', dest='key', help="API key")
parser.add_argument('-p', '--port', action='store', dest='port', help="API server port")
parser.add_argument('-s', '--server', action='store', dest='server', help="specify the API server to be connected")
# Parse arguments
args = parser.parse_args()

def main():
    if args.default is not None and args.default.strip():
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
