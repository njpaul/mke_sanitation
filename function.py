from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.utils.request_util import get_slot_value
import sanitation


# Returns an SSML representation of the collection date, given the current
# date and the collection date. If the date is less than 7 days away and
# within the same month, just speak the day. If the date is at least 7 days
# away or the month changes, speak the day and the month. If the year
# changes, speak the day, month, and year. If it's only one day away,
# say "tomorrow" instead of the name of the day. If collection date
# is today, alawys return "today". All numbers are zero-padded.
# Raises UnknownCollectionDate if coll_date is in the past
def convert_collection_date_to_speech(now, coll_date):
    days_until = (coll_date - now).days

    # TODO: This nasty block needs some refactoring
    if days_until < 0:
        raise sanitation.UnknownCollectionDate()
    elif days_until == 0:
        return "today"
    elif days_until == 1:
        if now.month == coll_date.month:
            return "tomorrow"
        elif now.year == coll_date.year:
            return 'tomorrow, {}, <say-as interpret-as="date" format="md">{}</say-as>'.format(
                coll_date.strftime("%A"), coll_date.strftime("%m/%d"))
        else:
            return 'tomorrow, {}, <say-as interpret-as="date" format="mdy">{}</say-as>'.format(
                coll_date.strftime("%A"), coll_date.strftime("%m/%d/%Y"))
    elif days_until < 7:
        if now.month == coll_date.month:
            return coll_date.strftime("%A")
        elif now.year == coll_date.year:
            return '{}, <say-as interpret-as="date" format="md">{}</say-as>'.format(
                coll_date.strftime("%A"), coll_date.strftime("%m/%d"))
        else:
            return '{}, <say-as interpret-as="date" format="mdy">{}</say-as>'.format(
                coll_date.strftime("%A"), coll_date.strftime("%m/%d/%Y"))
    elif now.year != coll_date.year:
        return '{}, <say-as interpret-as="date" format="mdy">{}</say-as>'.format(
            coll_date.strftime("%A"), coll_date.strftime("%m/%d/%Y"))
    else:
        return '{}, <say-as interpret-as="date" format="md">{}</say-as>'.format(
            coll_date.strftime("%A"), coll_date.strftime("%m/%d"))


def create_skill_builder():
    sb = SkillBuilder()

    @sb.request_handler(is_request_type("LaunchRequest"))
    def launch_request_handler(handler_input):
        speech = "Welcome to Milwaukee Sanitation. Ask me when your garbage or recycling day is."
        handler_input.response_builder.speak(
            speech).set_should_end_session(False)
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

    return sb


sb = create_skill_builder()
handler = sb.lambda_handler()
