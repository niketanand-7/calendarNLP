from openai import OpenAI
from prompt import PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self):
        self.prompt = PROMPT

    def read_file(self, file_path):
        data = ""
        with open(file_path, 'r') as file:
            # Read the entire file content
            data = file.read() # Strip to remove any leading/trailing whitespace
        return data
        

    
    def returnResponse(self, data):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"Read the following TXT file and output in this format: Assignment ---- Deadline \n"},
                      {"role": "user", "content": data}],
            max_tokens=100
        )
        print(response)
        
        return response.choices[0].message.content.strip()

# main function
if __name__ == "__main__":
    agent = Agent()
    file_path = os.path.join("Data", "data1.txt")
    
    data = agent.read_file(file_path)

    response = agent.returnResponse(data)
    print(response)
