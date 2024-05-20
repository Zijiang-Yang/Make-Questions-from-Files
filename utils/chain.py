import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic 
from fastapi import HTTPException

def load_template(type:str):
    if type == "chanpin":
        template_path = r"assets/simple_question_chanpin_template.txt"
    elif type == "jibing":
        template_path = r"assets/simple_question_jibing_template.txt"
    elif type == "gongneng":
        template_path = r"assets/simple_question_gongneng_template.txt"
    else:
        raise HTTPException(status_code=405, detail="任务类别错误，只能是chanpin、jibing、gongneng")
    
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    return template


def get_anthropic_llm():
    return ChatAnthropic(
        model_name=os.environ.get("MODEL_NAME_SONNET"),
        temperature=0
        )


def get_chain(type:str):
    prompt = ChatPromptTemplate.from_template(load_template(type))
    model = get_anthropic_llm()
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    return chain