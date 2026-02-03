from crewai.tools.agent_tools import Tool
from pydantic.v1 import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="A mathematical expression, e.g. 150+25 or 300/5*2")

def _calculate(expression: str):
    """Perform a calculation from a simple expression string."""
    try:
        # Be explicit about allowed characters to reduce abuse risk in eval
        allowed_chars = set("0123456789+-*/(). %")
        if not set(expression) <= allowed_chars:
            return "Error: Expression contains unsupported characters"
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="calculate",
    func=_calculate,
    description="Perform arithmetic calculations provided as an expression string",
    args_schema=CalculatorInput,
    verbose=True,
)
