from aws_lambda_powertools.utilities.parser import BaseModel


class Diagnosis(BaseModel):
    diagnosis: str
