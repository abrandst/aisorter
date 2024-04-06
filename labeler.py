import imaplib
import email
from email.header import decode_header
import langchain
from openai import OpenAI
import json
import os
import sys





class Labeler:
    def __init__(self) -> None:
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def label(self,text):
        prompt="""
        Please categorize the following email. Respond in JSON like this:
        {
            category: CATEGORY,
            summary: SUMMARY,
            total: TOTAL
        }
        Skip fields that would be empty in the specific answer.
        Only use the first category that applies.
        If it contains a verification code, use category "verification".
        If it is related to an order, please write the items ordered and the new status.
        Specificially if it is a bill, write the items and the total cost. Use the category "bill".
        If it is a notification, use category "notification".
        If it is a promotional email, use category "ad".
        If it is a mail related to the flat in Jahngasse 19, please summarize it in a single line and use  category "flat".
        If it is a personal email, use category "personal".
        EMAIL:

        """

        user_query=prompt+"\n"+text
        function_descriptions=[]

        self.client = OpenAI(
                    # This is the default and can be omitted
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
        


        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            model="gpt-3.5-turbo",
        )
        response=chat_completion.choices[0].message.content
        
        print(response)
        return json.loads(response)
