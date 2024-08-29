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
        output_prompt = f"""
        Based on the following information, create a calendar event dictionary in Python format with fields like 'summary', 'start', and 'end'. The 'start' and 'end' should be the date that you find, and end should 1 hour apart from start.

        Information:
        {data}

        Expected Output:
        event = {{
            'summary': '<Event Name>',
            'start': {{
                'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat(),
                'timeZone': 'America/New_York',
            }},
            'end': {{
                'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
                'timeZone': 'America/New_York',
            }},
        }}
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": output_prompt}
            ],
            max_tokens=150
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
