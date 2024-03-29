# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.embeddings import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
import os


system_message = """你是一位面试官，下面是一位面试者的工作经历和职位的要求，你负责判断该面试者是否符合职位要求。如果符合，你将回复1，不符合，你将回复0。"""

prompt_template = """
        面试者的工作经历：
        {}
        
        
        职位要求:
        {} 
    """

def is_qualified(client, resume_text, resume_requirement):
    if resume_requirement:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt_template.format(resume_text, resume_requirement)
                },
                {
                    "role": "assistant",
                    "content": "0"
                }
            ],
            temperature=0.2,
            max_tokens=20,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result_text = response.choices[0].message.content
        if result_text == "1":
            return True
        elif result_text == "0":
            return False
        else:
            print(f"OPENAI 回复为：{result_text}")
            return False


def initialize_client():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
    # Initialize OpenAI client
    if OPENAI_BASE_URL:
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    else:
        client = OpenAI(api_key=OPENAI_API_KEY)
    return client