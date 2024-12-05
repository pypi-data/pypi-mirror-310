from typing import Dict, List, Optional

import requests
from requests import HTTPError
from urllib3.util import retry

from databricks import version
from databricks.rag_eval import context, env_vars, session
from databricks.rag_eval.clients import databricks_api_client
from databricks.rag_eval.clients.managedrag import proto_serde
from databricks.rag_eval.config import assessment_config, example_config
from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
)
from databricks.rag_eval.evaluation import entities

SESSION_ID_HEADER = "eval-session-id"
BATCH_SIZE_HEADER = "eval-session-batch-size"
CLIENT_VERSION_HEADER = "eval-session-client-version"
CLIENT_NAME_HEADER = "eval-session-client-name"
JOB_ID_HEADER = "eval-session-job-id"
JOB_RUN_ID_HEADER = "eval-session-job-run-id"
MONITORING_WHEEL_VERSION_HEADER = "eval-session-monitoring-wheel-version"


def get_default_retry_config():
    return retry.Retry(
        total=env_vars.RAG_EVAL_LLM_JUDGE_MAX_RETRIES.get(),
        backoff_factor=env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR.get(),
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_jitter=env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER.get(),
        allowed_methods=frozenset(
            ["GET", "POST"]
        ),  # by default, it doesn't retry on POST
    )


class ManagedRagClient(databricks_api_client.DatabricksAPIClient):
    """
    Client to interact with the managed-rag service (/chat-assessments).

    Note: this client reads the session from the current thread and uses it to construct the request headers.
      Make sure to construct this client in the same thread where the session is initialized.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )
        self.extra_headers = self._construct_request_headers_from_session(
            session.current_session()
        )
        self.proto_serde = proto_serde.ChatAssessmentProtoSerde()

    def get_assessment(
        self,
        eval_item: entities.EvalItem,
        assessment_name: str,
        assessment_type: AssessmentType,
        examples: List[example_config.AssessmentExample],
        domain_instructions: Optional[str],
    ) -> List[entities.AssessmentResult]:
        """
        Retrieves the assessment results from the LLM judge service for the given eval item and requested assessment
        """
        request_json = self.proto_serde.construct_assessment_request_json(
            eval_item, assessment_name, examples, domain_instructions
        )

        with self.get_default_request_session(
            get_default_retry_config(), self.extra_headers
        ) as session:
            resp = session.post(
                self.get_method_url("/agents/chat-assessments"),
                json=request_json,
            )

        if resp.status_code == requests.codes.ok:
            return self.proto_serde.construct_assessment_result(
                resp.json(), assessment_name, assessment_type
            )
        else:
            try:
                resp.raise_for_status()
            except HTTPError as e:
                return self.proto_serde.construct_assessment_error_result(
                    assessment_name,
                    assessment_type,
                    resp.status_code,
                    e,
                )

    def emit_chat_assessment_usage_event(
        self,
        custom_assessments: List[assessment_config.EvaluationMetricAssessmentConfig],
        num_questions: Optional[int],
    ):
        request_json = (
            self.proto_serde.construct_chat_assessment_usage_event_request_json(
                custom_assessments, num_questions
            )
        )
        # Use default retries. Don't need to use response
        with self.get_default_request_session(headers=self.extra_headers) as session:
            session.post(
                self.get_method_url("/agents/chat-assessment-usage-events"),
                json=request_json,
            )

    def get_assessment_metric_definitions(
        self, assessment_names: List[str]
    ) -> Dict[str, assessment_config.AssessmentInputRequirementExpression]:
        """Retrieves the metric definitions for the given assessment names."""
        request_json = (
            self.proto_serde.construct_assessment_metric_definition_request_json(
                assessment_names
            )
        )

        with self.get_default_request_session(
            get_default_retry_config(), self.extra_headers
        ) as session:
            resp = session.post(
                self.get_method_url("/agents/chat-assessment-definitions"),
                json=request_json,
            )

        if resp.status_code == requests.codes.ok:
            return self.proto_serde.construct_assessment_input_requirement_expressions(
                resp.json()
            )
        else:
            try:
                resp.raise_for_status()
            except HTTPError as e:
                raise e

    def emit_client_error_usage_event(self, error_message: str):
        request_json = self.proto_serde.construct_client_error_usage_event_request_json(
            error_message=error_message
        )
        with self.get_default_request_session(headers=self.extra_headers) as session:
            session.post(
                self.get_method_url("/agents/evaluation-client-usage-events"),
                json=request_json,
            )

    @classmethod
    def _construct_request_headers_from_session(
        cls, eval_session: Optional[session.Session]
    ) -> Dict[str, str]:
        """Constructs the request headers from the session."""
        headers = {
            CLIENT_VERSION_HEADER: version.VERSION,
            CLIENT_NAME_HEADER: env_vars.RAG_EVAL_EVAL_SESSION_CLIENT_NAME.get(),
            JOB_ID_HEADER: context.get_context().get_job_id(),
            JOB_RUN_ID_HEADER: context.get_context().get_job_run_id(),
        }

        # Pass the internal version of the monitoring wheel if it is set
        current_session = session.current_session()
        if current_session and current_session.monitoring_wheel_version:
            headers[MONITORING_WHEEL_VERSION_HEADER] = (
                current_session.monitoring_wheel_version
            )

        if eval_session is None:
            return headers
        headers[SESSION_ID_HEADER] = eval_session.session_id
        if eval_session.session_batch_size is not None:
            headers[BATCH_SIZE_HEADER] = str(eval_session.session_batch_size)

        return headers
