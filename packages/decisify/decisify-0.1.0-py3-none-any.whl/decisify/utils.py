""" A module for utility functions, helper thats used in the decisify package. """
import json
from typing import TypeVar
from gurobipy import Model, GRB
from magentic import prompt
from modelsmith import Forge, OpenAIModel
from decisify.core import OptInputModel, OptOutputModel



@prompt("Write a description of the {input_data} such that a Large Language Model can recover the data model back, dont loose valuable information,\
        just keep the focus on data not on what the problem is")
def data_describer(input_data: OptInputModel | OptOutputModel) -> str:
    """Describe the data model"""
    pass




def data_transformer(query: str, data: OptInputModel):
    """Transform the data based on the query"""
    input_data_class = data.__class__
    forge = Forge(model=OpenAIModel("gpt-3.5-turbo"), response_model=input_data_class)
    data_description = data_describer(data)
    data_json = data.model_dump_json()
    user_prompt = f"{data_json}, now the user wants to {query}.\
    Change the data at approipriate places and give me a new data model, that satisfies the user's demands"
    transformed_data = forge.generate(user_prompt)
    return transformed_data


def answer_query(query: str, input_data: OptInputModel, output_data: OptOutputModel, model_metadata: str) -> str:
    """Answer the query using the model"""
    input_data_json = input_data.model_dump_json()
    output_data_json = output_data.model_dump_json()
    answer = (f"input_data: {input_data_json},\n output_data: {output_data_json},\n model_metadata: {model_metadata}")
    forge = Forge(model=OpenAIModel("gpt-3.5-turbo"), response_model=str)
    answer = forge.generate(query)
    return answer







