from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import parse, ValidationError
import os
from recog.models.diagnosis import Diagnosis
from recog.models.symptoms import Symptoms
from recog.services.openai import OpenAI
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
)

app = APIGatewayRestResolver()
tracer = Tracer(service=os.environ.get("POWERTOOLS_SERVICE_NAME", "recog"))
logger = Logger(service=os.environ.get("POWERTOOLS_SERVICE_NAME", "recog"))
metrics = Metrics(
    namespace=os.environ.get("POWERTOOLS_METRICS_NAMESPACE", "POWERTOOLS")
)


@app.get("/hello")
@tracer.capture_method
def hello():
    metrics.add_metric(name="HelloWorldInvocations", unit=MetricUnit.Count, value=1)
    logger.info("Hello world API - HTTP 200")
    return {"message": "hello world"}


@app.post("/diagnosis")
@tracer.capture_method
def diagnosis() -> dict:
    try:
        symptoms = parse(event=app.current_event.body, model=Symptoms)
        logger.info(symptoms)
        oai = OpenAI()
        diagnosis: Diagnosis = oai.get_diagnosis(symptoms)
        return diagnosis.dict()
    except ValidationError as e:
        logger.error(e)
        raise BadRequestError("Invalid symptoms format")
    except Exception as e:
        logger.error(e)
        raise InternalServerError(e)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
