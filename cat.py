import imaplib
import email
from email.header import decode_header
import langchain
from openai import OpenAI
import json
import os
import sys
import labeler


# Define the filename
filename = sys.argv[1]

# Open the file and read its contents into a string
try:
    with open(filename, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Use the file_contents string as needed
    #print(file_contents)
except FileNotFoundError:
    print(f'The file {filename} was not found.')
except Exception as e:
    print(f'An error occurred: {e}')

labeler=labeler.Labeler

labeler.label(file_contents)