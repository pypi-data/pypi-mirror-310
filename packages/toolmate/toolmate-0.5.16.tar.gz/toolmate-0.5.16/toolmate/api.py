from flask import Flask, request, jsonify
from toolmate import config
from toolmate.utils.assistant import ToolMate

app = Flask(__name__)
config.toolmate = ToolMate()

@app.route("/api/toolmate", methods=["POST"])
def process_query():
    data = request.get_json() 
    key = data.get("key", "")
    query = data.get("query", "")

    if key != config.toolmate_api_key:
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized

    if query := query.strip():
        config.toolmate.runMultipleActions(query)
        response = [i for i in config.currentMessages if not i.get("role", "") == "system"]
        config.currentMessages = config.toolmate.resetMessages()
        return jsonify(response)

def main():
    app.run(debug=True, port=config.toolmate_api_port)

if __name__ == '__main__':
    import requests
    prompt = {"key": "", "query": "Tell me a joke!"}
    response = requests.post("http://localhost:5000/api/toolmate", json=prompt)
    print(response.json())
