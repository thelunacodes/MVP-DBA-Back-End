from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Defines how the error message should be structured.
    """

    message: str