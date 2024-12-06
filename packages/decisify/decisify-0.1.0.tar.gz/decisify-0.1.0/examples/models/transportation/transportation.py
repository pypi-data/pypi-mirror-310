from typing import List
import gurobipy as gp
from gurobipy import GRB, Model, Var
from pydantic import BaseModel, Field
from decisify.optimizer import OptModel
from decisify.core import OptInputModel, OptOutputModel
from decisify.explainer import GurobiInterrogator


# A simple transportation problem, data from https://www.gurobi.com/resource/transportation-optimization/
warehouses = ["W1", "W2"]
customers = ["C1", "C2", "C3"]

# Parameters
supply = {"W1": 20, "W2": 30}
demand = {"C1": 10, "C2": 10, "C3": 30}
cost ={"W1": {"C1": 2, "C2": 3, "C3": 1},
         "W2": {"C1": 4, "C2": 1, "C3": 3}}



class TransportationInputs(OptInputModel):
    """Input data for the transportation problem"""
    warehouses: list[str] = Field(description="List of warehouses")
    customers: list[str] = Field(description="List of customers")
    supply: dict[str, int] = Field(description="Supply at each warehouse")
    demand: dict[str, int] = Field(description="Demand at each customer")
    cost: dict[str, dict[str, int]] = Field(description="Cost of transportation between warehouses and customers")

    


class TransportationOutputs(OptOutputModel):
    """Output data for the transportation problem"""
    status: int = Field(description="Status of the optimization model")
    total_cost: float = Field(description="Total transportation cost")
    solution: dict[tuple[str, str], float] = Field(description="Solution for the transportation problem")


class TransportationModel(OptModel):
    """ Optimization model for the transportation problem"""

    def _generate_opt_model(self, input_data: TransportationInputs):
        """ Generate the optimization model for the transportation problem"""
        # Create a new model
        model = gp.Model("transportation")

        # Create variables
        x = model.addVars(input_data.warehouses, input_data.customers, name="x")

        # Set objective
        model.setObjective(gp.quicksum(input_data.cost[w][c] * x[w, c] for w in input_data.warehouses for c in input_data.customers), GRB.MINIMIZE)

        # Add supply constraints
        model.addConstrs((gp.quicksum(x[w, c] for c in input_data.customers) <= input_data.supply[w] for w in input_data.warehouses), "Supply")

        # Add demand constraints
        model.addConstrs((gp.quicksum(x[w, c] for w in input_data.warehouses) == input_data.demand[c] for c in input_data.customers), "Demand")

        self.model = model
        self.decision_vars = {'x': x}


    def get_solution(self, input_data: TransportationInputs) -> TransportationOutputs:
        """ Get the solution for the transportation problem"""
        self._generate_opt_model(input_data)
        if self.is_solved():
            for w in input_data.warehouses:
                for c in input_data.customers:
                    if self.decision_vars['x'][w, c].x > 0:
                        print(f"Send {self.decision_vars['x'][w, c].x} units from {w} to {c} at cost {input_data.cost[w][c]}")

            # Print the total cost
            print(f"Total transportation cost: {self.model.objVal}")

            return TransportationOutputs(status=GRB.OPTIMAL, total_cost=self.model.objVal, solution={self.decision_vars['x'][w, c]: self.decision_vars['x'][w, c].x for w in input_data.warehouses for c in input_data.customers})
        else:
            self.solve_model()
            # Print the total cost
            if self.model.Status == GRB.OPTIMAL or self.model.Status == GRB.INTEGER or self.model.Status == GRB.TIME_LIMIT:
                print(f"Total transportation cost: {self.model.objVal}")
                solution = {
                                (w, c): self.decision_vars['x'][w, c].x
                                for w in input_data.warehouses
                                for c in input_data.customers
                                if self.decision_vars['x'][w, c].x > 1e-6  # Filter near-zero values for clarity
                            }
                return TransportationOutputs(status=self.model.Status, total_cost=self.model.objVal, solution=solution)
            else:
                # run IIS to get infeasible constraints
                # Run IIS to identify infeasible constraints
                self.model.computeIIS()

                # Collect IIS details
                iis_details = "Irreducible Inconsistent Subsystem (IIS) Details:\n"

                # Constraints in the IIS
                for constr in self.model.getConstrs():
                    if constr.IISConstr:
                        iis_details += f"Constraint: {constr.ConstrName}\n"

                # Variables with bound issues in the IIS
                for var in self.model.getVars():
                    if var.IISLB:
                        iis_details += f"Variable {var.VarName} has an issue with its lower bound.\n"
                    if var.IISUB:
                        iis_details += f"Variable {var.VarName} has an issue with its upper bound.\n"

                return f"Model is infeasible. {iis_details}"



if __name__ == "__main__":
    input_data = TransportationInputs(
    warehouses=warehouses,
    customers=customers,
    supply=supply,
    demand=demand,
    cost=cost)
    
    trnsprt_model = TransportationModel()
    solution = trnsprt_model.get_solution(input_data)
    print(solution.model_dump_json())
    interrogator = GurobiInterrogator(trnsprt_model, input_data)
    answer = interrogator.answer("What is the optimal solution for the transportation problem?")
    print(answer)
    answer = interrogator.answer("How many factories and how many distribution centers are there?")
    print(answer)
    #Now, lets assume the user wants to change the supply at warehouse W1 to 20
    answer = interrogator.what_if("the courier company just doubled the transportation costs, how does this affect the total cost?")
    print(answer)
    answer = interrogator.what_if("The demand at customer C1 has increased by 100 times, how does this affect the total cost?")
    print(answer)

