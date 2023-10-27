from flask import Flask, request, jsonify
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Load LLM inference endpoints from an env variable or a file
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# Initialize the Autogen agents
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})

@app.route('/initiate-chat', methods=['POST'])
def initiate_chat():
    try:
        # Get the user's request from the HTTP request
        data = request.get_json()
        user_request = data.get('user_request')

        # Initiate an automated chat between the two agents to solve the task
        response = user_proxy.initiate_chat(assistant, message=user_request)

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
