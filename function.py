from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.utils.request_util import get_slot_value
import sanitation

sb = SkillBuilder()


@sb.request_handler(is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    speech = "Welcome to Milwaukee Sanitation. Ask me when your garbage or recycling day is."
    handler_input.response_builder.speak(speech).set_should_end_session(False)
    return handler_input.response_builder.response


@sb.request_handler(is_intent_name("GetCollectionDate"))
def get_collection_date_handler(handler_input):
    coll_type = get_slot_value(handler_input, "collectionType")
    coll_addr = get_slot_value(handler_input, "collectionAddress")
    date = sanitation.get_collection_date(coll_type, coll_addr)
    handler_input.response_builder.speak(date).set_should_end_session(True)
    return handler_input.response_builder.response


@sb.request_handler(is_request_type("SessionEndedRequest"))
def session_ended_handler(handler_input):
    return handler_input.response_builder.response


@sb.exception_handler(lambda i, e: True)
def catch_all_exception_handler(handler_input, ex):
    print(ex)

    speech = "Sorry, I didn't understand that. Can you say it again?"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


handler = sb.lambda_handler()
