from typing_extensions import override
import time
import re
import os


import streamlit as st

'''
import openai
from openai import AssistantEventHandler

# should be secrets.toml file with OPENAI_API_KEY in streanlit folder
openai.api_key = st.secrets["OPENAI_API_KEY"]
    
client = openai.OpenAI()

assistant_id = 'asst_HGHaPA96oqQZJIX1532GTUoK'


# First, we create a EventHandler class to define
    # how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # Call the parent class's __init__ method
        self.response_text = ""
        self.response_placeholder = st.empty()
        self.response_placeholder.text('Analysis running...')

    @override
    def on_text_created(self, text) -> None:
        st.empty()
        self.response_placeholder.markdown(f"{self.response_text.strip()}") #**assistant >** 
        # st.write(f"\nassistant > ")

    @override
    def on_text_delta(self, delta, snapshot):
        self.response_text += sanitize_text(delta.value)
        self.response_placeholder.markdown(f"{self.response_text.strip()}") #**assistant >** 

    def on_tool_call_created(self, tool_call):
        st.empty()
        # st.write(f"\nassistant > {tool_call.type}\n")

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                st.write(delta.code_interpreter.input)
            if delta.code_interpreter.outputs:
                st.write(f"\n\noutput >")
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        st.write(f"\n{output.logs}")

'''
def sanitize_text(text):
    # Example regex to remove patterns like  
    clean_text = re.sub(r"【\d+:\d+†source】", "", text)
    return clean_text


# Define a function to get assistant response
def get_assistant_response(prompt):
    file_path = os.path.join('reports//block_reports', 'text.txt')

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            full_text = file.read()
            lines = full_text.split('\n')   
            for line in lines:
                words = line.split()
                line_placeholder = st.empty()
                accumulated_line = ""
                for word in words:
                    accumulated_line += word + " "
                    line_placeholder.markdown(accumulated_line.strip())
                    time.sleep(len(word)%3 / 10)
            return full_text
    else:
        st.write('Report doesn''t exist!')
        return ""

# Define a function to get assistant response
def get_full_report_check(user_file, industry):

    reports = {}

    for file_name in os.listdir('reports//full_reports'):
        file_path = os.path.join('reports//full_reports', file_name)
        if os.path.isfile(file_path):
            reports[os.path.splitext(file_name)[0]] = file_path

    file_name = user_file.name
    file_type = user_file.type.split('/')[-1]
    file_name = os.path.splitext(file_name)[0]

    if file_name in reports.keys():
        with open(reports[file_name], 'r', encoding='utf-8') as file:
            full_text = file.read()

            lines = full_text.split('\n')
        #with open(reports[file_name], 'r', encoding='utf-8') as file:
        #   lines = file.readlines()    
            for line in lines:
                words = line.split()
                line_placeholder = st.empty()
                accumulated_line = ""
                for word in words:
                    accumulated_line += word + " "
                    line_placeholder.markdown(accumulated_line.strip())
                    time.sleep(len(word)%3 / 10)
            return full_text
    else:
        st.write('Report doesn''t exist!')
        return ""

def get_part_report_check(user_file):

    reports = {}

    for file_name in os.listdir('reports//block_reports'):
        file_path = os.path.join('reports//block_reports', file_name)
        if os.path.isfile(file_path):
            reports[os.path.splitext(file_name)[0]] = file_path

    file_name = user_file.name
    file_type = user_file.type.split('/')[-1]
    file_name = os.path.splitext(file_name)[0]

    if file_name in reports.keys():
        with open(reports[file_name], 'r', encoding='utf-8') as file:
            #lines = file.readlines()    
            full_text = file.read()
            lines = full_text.split('\n')
            for line in lines:
                words = line.split()
                line_placeholder = st.empty()
                accumulated_line = ""
                for word in words:
                    accumulated_line += word + " "
                    line_placeholder.markdown(accumulated_line.strip())
                    time.sleep(len(word)%3 / 10)
            return full_text
    else:
        st.write('Report doesn''t exist!')
        return ""
