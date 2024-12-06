""" Module for abstract optimization models """
from typing import Dict
import json
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from gurobipy import Model, Var, GRB
from decisify.core import OptInputModel, OptOutputModel


class OptimizerSettings(BaseModel):
    """Settings for the optimization model"""
    mip_gap: float = Field(default=0.01, description="MIP gap for the optimization model", ge=0.0, le=1.0)
    time_limit: int = Field(default=300, description="Time limit for the optimization model in seconds", ge=0)


class BaseOptModel(ABC):

    """ Abstract class for optimization models """

    @abstractmethod
    def _generate_model(self, input_data: OptInputModel):
        """ Generate the optimization model """
        pass

    @abstractmethod
    def solve_model(self):
        """ Solve the optimization model """
        pass

    @abstractmethod
    def is_solved(self) -> bool:
        """ Check if the model is solved """
        pass

    @abstractmethod
    def get_solution(self, input_data: OptInputModel) -> OptOutputModel:
        """ Get the solution for the model """
        pass


class OptModel(BaseOptModel):

    """ Optimization model for the transportation problem"""

    def __init__(self, opt_settings: OptimizerSettings = OptimizerSettings()):
        self.opt_settings = opt_settings
        self.model: Model
        self.decision_vars: Dict[str, Var]


    def __new__(cls, *args, **kwargs):
        """ Prevent direct instance of this class """
        if cls is OptModel:
            raise TypeError(f"{cls.__name__} class cannot be instantiated")
        return super().__new__(cls)
      
    def _generate_model(self, input_data: OptInputModel):
        """Generate the optimization model"""
        raise NotImplementedError("Method generate_model must be implemented in subclass")
       
    def solve_model(self):
        """Solve the optimization model"""
        self.model.optimize()
   
    def is_solved(self) -> bool:
        """Check if the model is solved"""
        return self.model.status == GRB.OPTIMAL or self.model.status == GRB.INTEGER or self.model.status == GRB.TIME_LIMIT
    
   
    def get_solution(self, input_data: OptInputModel) -> OptOutputModel:
        """Get the solution for the model"""
        raise NotImplementedError("Method get_solution must be implemented in subclass")
    


class ModelMetaData(ABC):
    """Metadata for the optimization model"""
    
    @abstractmethod
    def get_basic_info(self):
        """Retrieve basic metadata about the model"""
        pass
    
    @abstractmethod
    def get_variables_info(self):
        """Retrieve information about the model variables"""
        pass
    
    @abstractmethod
    def get_constraints_info(self):
        """Retrieve information about the model constraints"""
        pass
    
    @abstractmethod
    def get_solution_info(self):
        """Retrieve information about the optimization solution"""
        pass
    
    @abstractmethod
    def get_metadata_as_json(self):
        """Combine all metadata and return as a JSON string"""
        pass




class GurobiModelMetaData(ModelMetaData):
    """Metadata for the Gurobi optimization model"""
    def __init__(self, model: Model):
        """
        Initialize the GurobiModelMetaData with a Gurobi model instance.
        
        Args:
            model (Model): A Gurobi model object.
        """
        self.model: Model = model.model

    def get_basic_info(self):
        """Retrieve basic metadata about the model."""
        return {
            "ModelName": self.model.ModelName,
            "NumVars": self.model.NumVars,
            "NumConstrs": self.model.NumConstrs,
            "NumQConstrs": self.model.NumQConstrs,
            "NumSOS": self.model.NumSOS,
            "ObjectiveSense": "Minimize" if self.model.ModelSense == GRB.MINIMIZE else "Maximize",
        }
    
    def get_variables_info(self):
        """Retrieve information about the model variables."""
        return [
            {
                "Name": var.VarName,
                "LowerBound": var.LB,
                "UpperBound": var.UB,
                "ObjectiveCoeff": var.Obj,
                "SolutionValue": var.X if self.model.Status == GRB.OPTIMAL else None,
            }
            for var in self.model.getVars()
        ]
    
    def get_constraints_info(self):
        """Retrieve information about the model constraints."""
        return [
            {
                "Name": constr.ConstrName,
                "Sense": constr.Sense,
                "RHS": constr.RHS,
                "ShadowPrice": constr.Pi if self.model.Status == GRB.OPTIMAL else None,
            }
            for constr in self.model.getConstrs()
        ]
    
    def get_solution_info(self):
        """Retrieve information about the optimization solution."""
        if self.model.Status == GRB.OPTIMAL:
            return {
                "Status": "Optimal",
                "ObjectiveValue": self.model.ObjVal,
                "Runtime": self.model.Runtime,
                "MIPGap": self.model.MIPGap if hasattr(self.model, "MIPGap") else None,
                "NodeCount": self.model.NodeCount,
            }
        else:
            return {"Status": self.model.Status}

    def get_metadata_as_json(self):
        """Combine all metadata and return as a JSON string."""
        metadata = {
            "BasicInfo": self.get_basic_info(),
            "Variables": self.get_variables_info(),
            "Constraints": self.get_constraints_info(),
            "Solution": self.get_solution_info(),
        }
        return json.dumps(metadata, indent=4)




