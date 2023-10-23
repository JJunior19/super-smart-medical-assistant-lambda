import json
import pytest
import app
from recog.models.diagnosis import Diagnosis
from unittest.mock import patch


def lambda_context():
    class LambdaContext:
        def __init__(self):
            self.function_name = "test-func"
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = (
                "arn:aws:lambda:eu-west-1:809313241234:function:test-func"
            )
            self.aws_request_id = "52fdfc07-2182-154f-163f-5f0f9a621d72"

        def POST_remaining_time_in_millis(self) -> int:
            return 1000

    return LambdaContext()


@pytest.fixture()
def apigw_event_ok():
    """Generates API GW Event"""
    with open("events/apigw_event_ok.json", "r") as fp:
        return json.load(fp)


@pytest.fixture()
def apigw_event_ko():
    """Generates API GW Event"""
    with open("events/apigw_event_ko.json", "r") as fp:
        return json.load(fp)


def test_diagnosis_ok(apigw_event_ok):
    with patch("recog.services.openai.OpenAI.get_diagnosis") as mock_get_diagnosis:
        mock_get_diagnosis.return_value = Diagnosis(
            diagnosis="You have a cold. You should take some medicine and rest."
        )
        ret = app.lambda_handler(apigw_event_ok, lambda_context())
        data = json.loads(ret["body"])

        assert ret["statusCode"] == 200
        assert "diagnosis" in ret["body"]
        assert (
            data["diagnosis"]
            == "You have a cold. You should take some medicine and rest."
        )


def test_diagnosis_ko(apigw_event_ko):
    with patch("recog.services.openai.OpenAI.get_diagnosis") as mock_get_diagnosis:
        mock_get_diagnosis.return_value = Diagnosis(
            diagnosis="You have a cold. You should take some medicine and rest."
        )
        ret = app.lambda_handler(apigw_event_ko, lambda_context())
        assert ret["statusCode"] == 400
        assert "Invalid symptoms format" in ret["body"]
