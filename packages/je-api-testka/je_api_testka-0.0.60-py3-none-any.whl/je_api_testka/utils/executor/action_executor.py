import sys

from je_api_testka.requests_wrapper.request_method import test_api_method
from je_api_testka.utils.exception.api_test_exceptions import APITesterExecuteException
from je_api_testka.utils.exception.api_test_eceptions_tag import executor_data_error
from je_api_testka.utils.exception.api_test_eceptions_tag import executor_list_error
from je_api_testka.utils.html_report.html_report_generate import generate_html
from je_api_testka.utils.json.json_file.json_file import read_action_json

event_dict = {
    # test api
    "test_api_method": test_api_method,
    "generate_html": generate_html,
}


def execute_event(action: list):
    """
    :param action: execute action
    :return: what event return
    """
    event = event_dict.get(action[0])
    if len(action) == 2:
        return event(**action[1])
    else:
        raise APITesterExecuteException(executor_data_error)


def execute_action(action_list: list):
    """
    :param action_list: like this structure
    [
        ["method on event_dict", {"param": params}],
        ["method on event_dict", {"param": params}]
    ]
    for loop and use execute_event function to execute
    :return: recode string, response as list
    """
    execute_record_string = ""
    event_response_list = []
    try:
        if len(action_list) > 0 or type(action_list) is not list:
            for action in action_list:
                event_response = execute_event(action)
                print("execute: ", str(action))
                execute_record_string = "".join(execute_record_string)
                event_response_list.append(event_response)
        else:
            raise APITesterExecuteException(executor_list_error)
        return execute_record_string, event_response_list
    except Exception as error:
        print(repr(error), file=sys.stderr)


def execute_files(execute_files_list: list):
    """
    :param execute_files_list: list include execute files path
    :return: every execute detail as list
    """
    execute_detail_list = list()
    for file in execute_files_list:
        execute_detail_list.append(execute_action(read_action_json(file)))
    return execute_detail_list
