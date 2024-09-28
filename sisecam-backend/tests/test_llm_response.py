from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.test_case import LLMTestCaseParams
import pytest
import json
from evaluation_models.azure_openai import AZURE_MODEL

with open('./tests/data/llm_cases_test.json') as f:
    data = json.load(f)

correctness_metric = GEval(
    model=AZURE_MODEL,
    threshold=0.8,
    name="Correctness",
    criteria="Determine whether the actual output is factually correct based on the expected output. \
              Penalize heavily if actual and expected output are not written in the same language. \
              Do not penalize the output on detail level, as long as you are getting the correct answer.",

    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
)

@pytest.mark.parametrize("key", data.keys())
def test_answer_relevancy(key):
    test_case = LLMTestCase(
        input = data[key]["input"],
        expected_output = data[key]["expected_output"],
        actual_output = data[key]["actual_output"],
    )
    assert_test(test_case, [correctness_metric])

