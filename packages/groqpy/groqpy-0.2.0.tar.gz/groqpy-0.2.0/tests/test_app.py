import unittest
from groqpy.groq_agent import GroqAgent
import logging


GROQ_API_KEY = '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'
GROQ_MODEL = 'llama3-70b-8192'
GROQ_TEMPERATURE = 0

logging.basicConfig(filename='test.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class TestApp(unittest.TestCase):
    def test_app(self):
        agent = GroqAgent(api_key=GROQ_API_KEY)
        agent.ChatSettings(model=GROQ_MODEL, temperature=GROQ_TEMPERATURE)

        prompt = 'Say a random sentence'
        for i in range(1, 2):
            response = agent.Chat(prompt, remember=False, verbose=True)

            import json
            j_dmp = json.dumps(response, indent='\033[0m  ')
            print(i, '-', 'Agent:', response['choices'][0]['message']['content'], "\n", j_dmp, flush=True)

            import time
            time.sleep(.5)
        self.assertTrue(True)
