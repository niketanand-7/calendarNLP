import openai
from prompt import prompt
from dotenv import load_dotenv
import os
from Data.MachineLearningClass import Prompt

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self):
        self.prompt = prompt

    def read_file(self, file_name):
        with open(file_name, 'r') as file:
            data = file.readlines()
            for line in data:
                print(line.strip()) 
    
    def returnResponse(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60
        )
        return response.choices[0].text.strip()

# main function
if __name__ == "__main__":
    agent = Agent()
    file_name = "Prompt.txt"
    agent.read_file(file_name)
    response = agent.returnResponse(agent.prompt)
    print(response)
