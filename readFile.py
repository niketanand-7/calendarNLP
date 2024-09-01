from openai import OpenAI
from prompt import PROMPT
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

class calendarExtraction(BaseModel):
    summary: str
    start: str
    end: str


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
        new_prompt = f"""Based on the following information, extract all the assignments. 
                     Each assignment should have a 'summary' field as the title, 'start' as the closest date to the title, 
                     and 'end' should be an hour apart from 'start'. 
                     The data should be structured as a list of dictionaries with fields 'summary', 'start', and 'end'. The year is 2024.
                     THERE SHOULD BE MORE THAN 1 ASSIGNMENT
                     Data: {data}
                     """
        
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured data about my syllabus, I want you to determine start and end date and time in the dictionary and timezone to be New York, and convert it into sturctured data"},
                {"role": "user", "content": new_prompt}
            ],
            response_format = calendarExtraction,
            max_tokens = 16384,
            temperature = 0.1
        )
        res = response.choices[0].message.parsed
        print(res)
        return res

# main function
if __name__ == "__main__":
    agent = Agent()
    file_path = os.path.join("Data", "data2.csv")
    
    data = agent.read_file(file_path)

    response = agent.returnResponse(data)

    # print(response)
