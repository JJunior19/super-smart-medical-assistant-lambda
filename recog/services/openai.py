import openai
from recog.models.symptoms import Symptoms
from recog.models.diagnosis import Diagnosis
import os
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools import Logger

logger = Logger(service=os.environ.get("POWERTOOLS_SERVICE_NAME", "recog"))


class OpenAI:
    def __init__(self, **kwargs) -> None:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = kwargs.get("model", "gpt-3.5-turbo")

    def get_diagnosis(self, symptoms: Symptoms) -> Diagnosis:
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a virtual doctor highly trained to diagnose patients, that give diagnoses in less than 100 words based on the symptoms they describe.",
                },
                {
                    "role": "user",
                    "content": "I have a the following symptoms: "
                    + ", ".join(symptoms.symptoms),
                },
            ]
            response = openai.ChatCompletion.create(
                model=self.model, messages=messages, max_tokens=200
            )
            logger.info(response)
            return parse(
                {"diagnosis": response.choices[0].message["content"]}, Diagnosis
            )
        except Exception as e:
            raise e
