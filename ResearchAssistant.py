from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import json
import sys
import openai

load_dotenv()

class ResearchAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def ask(self, question: str) -> str:

        for attempt in range(1,4):
            try:
                response = self.client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": question}])
                return response.choices[0].message.content
            except openai.RateLimitError:
                print(f"Attempt: {attempt} rate limited, retrying...")
            except openai.APITimeoutError:
                print(f"Attempt: {attempt} timed out, retrying")
            except openai.AuthenticationError as e:
                raise ValueError("Invalid API key") from e
            
            time.sleep(1)
        
        raise RuntimeError(f"Exhuasted all 3 attempts ")
    
    def save_result(self, question: str, answer: str):
        entry = {"question": question, "answer": answer}
        filename = "research_log.json"


        if os.path.exists(filename): 
            with open(filename, "r") as f: # file already exists, read what's in it first
                log = json.load(f) # gives list of past entries
        else:
            log = [] # file doesn't exist yet star with empty list
        log.append(entry) # add new entry to it
        # write entire updated list back to file
        with open(filename, "w") as f: 
            json.dump(log, f, indent=2)

            

if __name__ == "__main__":
    question = sys.argv[1]
    assistant = ResearchAssistant()
    answer = assistant.ask(question)
    print(answer)
    assistant.save_result(question, answer)