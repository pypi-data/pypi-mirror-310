from enum import IntEnum
from typing import Any, Dict
from gurobipy import Model, Var, GRB
from pydantic import BaseModel


class SolveStatus(IntEnum):
    """Status of the optimization model"""
    LOADED          = 1
    OPTIMAL         = 2
    INFEASIBLE      = 3
    INF_OR_UNBD     = 4
    UNBOUNDED       = 5
    CUTOFF          = 6
    ITERATION_LIMIT = 7
    NODE_LIMIT      = 8
    TIME_LIMIT      = 9
    SOLUTION_LIMIT  = 10
    INTERRUPTED     = 11
    NUMERIC         = 12
    SUBOPTIMAL      = 13
    INPROGRESS      = 14
    USER_OBJ_LIMIT  = 15
    WORK_LIMIT      = 16
    MEM_LIMIT       = 17



class OptInputModel(BaseModel):
    """Input data for the optimization model"""
    
    def __new__(cls, *args, **kwargs):
        """ Prevent direct instance of this class """
        if cls is OptInputModel:
            raise TypeError(f"{cls.__name__} class cannot be instantiated")
        return super(BaseModel, cls).__new__(cls)
    

class OptOutputModel(BaseModel):
    """Output data for the optimization model"""
    
    def __new__(cls, *args, **kwargs):
        """ Prevent direct instance of this class """
        if cls is OptOutputModel:
            raise TypeError(f"{cls.__name__} class cannot be instantiated")
        return super(BaseModel, cls).__new__(cls)

    