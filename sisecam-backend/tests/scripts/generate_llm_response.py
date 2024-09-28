import json
from controllers.chatbot import ChatController

def generate_llm_responses(naming=""):

    with open(f'./tests/data/llm_cases{naming}.json') as f:
        data = json.load(f)

    chat_controller = ChatController()

    for case, values in data.items():
        response = chat_controller.chat(input=values["input"]).data["response"]
        data[case]["actual_output"] = response
    
    with open(f'./tests/data/llm_cases_test{naming}.json', 'w') as fp:
        json.dump(data, fp)

if __name__ == "__main__":
    generate_llm_responses()
