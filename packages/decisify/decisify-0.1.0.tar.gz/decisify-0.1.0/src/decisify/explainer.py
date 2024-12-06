""" Explainer abstract class for explainer classes """
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from decisify.core import OptInputModel, OptOutputModel
from decisify.optimizer import ModelMetaData, OptModel, GurobiModelMetaData
from decisify.utils import answer_query, data_transformer



class LLMSettings(BaseSettings):
    """ Settings for the LLM explainer """
    OPENAI_API_KEY: str = Field(description="API key for the LLM model that will be connected to the explainer")


class Interrogator(ABC):
    """ Abstract class for explainer classes """

    @abstractmethod
    def answer(self, query: str):
        """ Answer the query using the model """
        pass

    @abstractmethod
    def explain(self, query: str):
        """ Explain the model decision making process """
        pass

    @abstractmethod
    def what_if(self, query: str):
        """ Interrogate the model to understand the decision making process """
        pass


class GurobiInterrogator(Interrogator):
    """ GPT Explainer class for explaining the GPT models """

    def __init__(self, model: OptModel, 
                 input_data: OptInputModel,
                 model_metadata: ModelMetaData = GurobiModelMetaData):
        self.model = model
        self.input_data = input_data
        self.output_data = self.model.get_solution(input_data)
        self.model_metadata = model_metadata(self.model).get_metadata_as_json()



    def answer(self, query: str) -> str:
        """ Answer the query using the model """
        return answer_query(query, self.input_data, self.output_data, self.model_metadata)
        
        
    def explain(self, query: str):
        """ Explain the model decision making process """
        raise NotImplementedError("No implementation for explain method")



    def what_if(self, query: str) -> OptOutputModel:
        """ Interrogate the model to understand the decision making process """
        new_inputs = data_transformer(query, self.input_data)
        return self.model.get_solution(new_inputs)




