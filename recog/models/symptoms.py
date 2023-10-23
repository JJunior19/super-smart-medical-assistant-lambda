from aws_lambda_powertools.utilities.parser import BaseModel
from typing import List


class Symptoms(BaseModel):
    symptoms: List[str]
