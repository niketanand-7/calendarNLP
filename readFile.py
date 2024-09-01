from openai import OpenAI
from prompt import PROMPT
from dotenv import load_dotenv
from pydantic import BaseModel
# from addToCalendar import insertingCalendarEvent
import os

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

class calendarExtraction(BaseModel):
    summary: str
    start: dict
    end: dict


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
        Based on the following information, create a Python dictionary for a calendar event. 
        The output should be a Python dictionary in this exact format, with no additional text or explanations:

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

        Your output should strictly follow the format above, with the 'summary' field reflecting the event name, and the 'dateTime' fields reflecting the correct start and end times.
        """
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured data about my syllabus, I want you to determine start and end date and time in the dictionary and timezone to be New York, and convert it into sturctured data"},
                {"role": "user", "content": output_prompt}
            ],
            response_format=calendarExtraction,
            max_tokens = 150,
            temperature= 0.1
        )
        res = response.choices[0].message.parsed


        
        return res

# main function
if __name__ == "__main__":
    agent = Agent()
    file_path = os.path.join("Data", "data1.txt")
    
    data = agent.read_file(file_path)

    response = agent.returnResponse(data)
    print(response)
    print("-------")
    print(response[0])
