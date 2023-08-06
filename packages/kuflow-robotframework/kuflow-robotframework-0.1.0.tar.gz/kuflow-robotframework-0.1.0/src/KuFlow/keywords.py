#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.#

import logging
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.element_value_or_array_value import (
    ElementValueOrArrayValue,
)
from kuflow_rest_client.model.log import Log
from kuflow_rest_client.model.log_level import LogLevel
from kuflow_rest_client.model.save_element_document_command import (
    SaveElementDocumentCommand,
)
from robot.api.deco import keyword


class Keywords:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._client_configuration = None

    @keyword(tags=("settings",))
    def set_client_authentication(self, endpoint, identifier, token):
        """Configure the client authentication in order to execute keywords against Rest API.

        Before using any other KuFlow Keyword, this one must be called.

        Example:
        | Set Client Authentication | %{KUFLOW_API_ENDPOINT} | %{KUFLOW_APPLICATION_IDENTIFIER} | %{KUFLOW_APPLICATION_TOKEN}
        =>
        | Set Client Authentication | https://api.kuflow.com/v1.0 | identifier | token
        """
        self._client_configuration = kuflow_rest_client.Configuration(
            host=endpoint,
            username=identifier,
            password=token,
        )

    @keyword()
    def append_log_message(self, task_id: str, message: str, level=LogLevel.INFO):
        """Add a log entry to the task

        If the number of log entries is reached, the oldest log entry is removed.
        The level of log can be INFO, WARN or ERROR.

        Example:
        | Append Log Message | ${TASK_ID} | ${MESSAGE}
        | Append Log Message | ${TASK_ID} | ${MESSAGE} | level=${LEVEL}
        =>
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My info message
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My warning message | level=WARN
        """

        body = Log(
            message=message,
            level=level,
        )

        self._do_append_log_request(task_id, body)

    @keyword()
    def save_element_document(self, task_id: str, code: str, path):
        """Save a element of type document

        If it is a multiple element, and the Id referenced in the body does not exist or is empty,
        the document will be added to the element.

        If the element already exists (the Id referenced in the body corresponds to an existing one), it updates it.

        Example:
        | Save Element Document | ${TASK_ID} | ${CODE} | ${PATH}
        =>
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg
        """

        body = dict(
            json=SaveElementDocumentCommand(
                code=code,
            ),
            file=open(path, "rb"),
        )

        self._do_save_element_document_request(task_id, body)

    @keyword()
    def save_element(self, task_id, code, value, valid=True):
        """Save a element

        Allow to save an element that is not a document i.e., a field, a decision or form. If you want to add documents,
        use the appropriate API method.

        If values already exist for the provided element code, it replaces them with the new ones, otherwise it creates
        them. To remove an element, use the appropriate API method.

        Example:
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE} | ${VALID}
        =>
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | My value
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | My value | ${False}
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | 123
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | {}

        """
        body = ElementValueOrArrayValue(
            code=code,
            value=ElementValueOrArrayValue.value({"value": value, "valid": valid}),
        )
        self._do_save_element_request(task_id, body)

    @keyword()
    def save_elements(self, task_id, code, source_values: list):
        """Save a element

        Allow to save an element that is not a document i.e., a field, a decision or form. If you want to add documents,
        use the appropriate API method.

        If values already exist for the provided element code, it replaces them with the new ones, otherwise it creates
        them. To remove an element, use the appropriate API method.

        source_values: It is a list of dictionaries with at least one element. Each dictionary must contain at least the
        'value' key and optionally the 'valid' key.

        The 'value' field of the dictionary will contain a value according to its specification in the process
        definition in KuFlow.

        The 'value' field of the dictionary shall contain a Boolean value.

        Example:
        | Save Elements | ${TASK_ID} | ${CODE} | ${ELEMENT_VALUES}
        =>
        | &{element_one} | Create Dictionary | value=My Example Value One | valid=${False}
        | &{element_two} | Create Dictionary | value=My Example Value Two
        | ${elements}    | Create List       | ${element_one} | ${element_two}
        | Save Elements    d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec    ELEMENT_KEY    ${elements}
        """
        target = []
        for source_value in source_values:
            target.append({**source_value})

        body = ElementValueOrArrayValue(
            code=code,
            value=ElementValueOrArrayValue.value(target),
        )
        self._do_save_element_request(task_id, body)

    def _do_save_element_document_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_save_element_document(
                    path_params=path_params,
                    body=body,
                )
            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_save_element_document: %s\n"
                    % e
                )
                raise e

    def _do_append_log_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_append_log(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_append_log: %s\n"
                    % e
                )
                raise e

    def _do_save_element_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                return api_instance.actions_save_element(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling TaskApi->actions_save_element: %s\n" % e
                )
                raise e
