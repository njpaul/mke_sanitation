from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_model.services import ServiceException
from ask_sdk_core.utils.request_util import get_slot_value, get_device_id, get_api_access_token
import pendulum
import sanitation

sb = CustomSkillBuilder(api_client=DefaultApiClient())

WELCOME = ("Welcome to Milwaukee Sanitation. "
           "Ask me when your garbage or recycling day is.")
REPROMT = "Ask me when your garbage or recycling day is."
NOTIFY_MISSING_PERMISSIONS = ("Please enable Location permissions in "
                              "the Amazon Alexa app.")
NO_ADDRESS = ("It looks like you don't have an address set. "
              "You can set your address from the companion app.")
ADDRESS_AVAILABLE = "Here is your full address: {}, {}, {}"
ERROR = "Uh Oh. Looks like something went wrong."
LOCATION_FAILURE = ("There was an error with the Device Address API. "
                    "Please try again.")
FALLBACK = "Milwaukee Sanitation can't help with that. Ask me when your garbage or recycling day is."
HELP = ("You can use this skill by asking something like: "
        "When is recycling day? ")
EXCEPTION = "Sorry, I ran into a problem. Please ask me again."

# Location Consent permission to be shown on the card.
PERMISSIONS = ["read::alexa:device:all:address"]


@sb.request_handler(is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    handler_input.response_builder.speak(WELCOME).ask(REPROMT)
    return handler_input.response_builder.response


@sb.request_handler(is_intent_name("GetCollectionDate"))
def get_collection_date_handler(handler_input):
    req_envelope = handler_input.request_envelope
    response_builder = handler_input.response_builder
    service_client_fact = handler_input.service_client_factory

    if not (req_envelope.context.system.user.permissions and
            req_envelope.context.system.user.permissions.consent_token):
        response_builder.speak(NOTIFY_MISSING_PERMISSIONS)
        response_builder.set_card(
            AskForPermissionsConsentCard(permissions=PERMISSIONS))
        return response_builder.response

    try:
        device_id = req_envelope.context.system.device.device_id
        device_addr_client = service_client_fact.get_device_address_service()
        addr = device_addr_client.get_full_address(device_id)

        if addr.address_line1 is None and addr.state_or_region is None:
            response_builder.speak(NO_ADDRESS)
        else:
            response_builder.speak(ADDRESS_AVAILABLE.format(
                addr.address_line1, addr.state_or_region, addr.postal_code))
        return response_builder.response
    except ServiceException:
        response_builder.speak(ERROR)
        return response_builder.response
    except Exception as e:
        raise e


# class GetAddressExceptionHandler(AbstractExceptionHandler):
#     # Custom Exception Handler for handling device address API call exceptions
#     def can_handle(self, handler_input, exception):
#         return isinstance(exception, ServiceException)

#     def handle(self, handler_input, exception):
#         if exception.status_code == 403:
#             handler_input.response_builder.speak(
#                 NOTIFY_MISSING_PERMISSIONS).set_card(
#                 AskForPermissionsConsentCard(permissions=PERMISSIONS))
#         else:
#             handler_input.response_builder.speak(
#                 LOCATION_FAILURE).ask(LOCATION_FAILURE)

#         return handler_input.response_builder.response

@sb.request_handler(is_request_type("SessionEndedRequest"))
def session_ended_handle(handler_input):
    return handler_input.response_builder.response


@sb.request_handler(is_intent_name("AMAZON.HelpIntent"))
def help_handler(handler_input):
    handler_input.response_builder.speak(HELP).ask(HELP)
    return handler_input.response_builder.response


@sb.request_handler(lambda handler_input:
                    is_intent_name("AMAZON.CancelIntent")(handler_input) or
                    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_handler(handler_input):
    return handler_input.response_builder.response


@sb.request_handler(is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    handler_input.response_builder.speak(FALLBACK).ask(HELP)
    return handler_input.response_builder.response


@sb.exception_handler(lambda handler_input, ex: True)
def exception_handler(handler_input, ex):
    print(ex)
    handler_input.response_builder.speak(EXCEPTION).ask(EXCEPTION)
    return handler_input.response_builder.response


handler = sb.lambda_handler()


# @sb.request_handler(is_intent_name("GetCollectionDateAtAddress"))
# def get_collection_date_at_address_handler(handler_input):
#     coll_type = get_slot_value(handler_input, "collectionType")
#     coll_addr = get_slot_value(handler_input, "collectionAddress")

#     print(coll_addr)

#     # TODO: Handle exceptions with additional dialog. For now, let the
#     # exception handler do the work.
#     # TODO: Find a way to test the timezone here because this issue was
#     # suspected and then confirmed through a manual test.
#     # TODO: While we know the timezone is Central, we don't want the UI
#     # to know that. Move this knowledge elsewhere.
#     now = pendulum.today("America/Chicago").date()
#     print(now)
#     coll_date = sanitation.get_collection_date(coll_type, coll_addr)
#     speech = 'The next {} day at <say-as interpret-as="address">{}</say-as> is {}'.format(
#         coll_type, coll_addr, convert_collection_date_to_speech(now, coll_date))
#     handler_input.response_builder.speak(
#         speech).set_should_end_session(True)
#     return handler_input.response_builder.response


# @sb.request_handler(is_intent_name("GetCollectionDate"))
# def get_collection_date_handler(handler_input):
#     device_id = get_device_id(handler_input)
#     addr_service = handler_input.service_client_factory.get_device_address_service()
#     try:
#         coll_addr = addr_service.get_full_address(device_id)
#         handler_input.response_builder.speak(coll_addr)
#     except ServiceException as ex:
#         return handler_input.response_builder.speak(str(ex)).set_should_end_session(True)

#     coll_type = get_slot_value(handler_input, "collectionType")

#     handler_input.set_should_end_session(True)
#     return handler_input


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

    if days_until < 0:
        raise sanitation.UnknownCollectionDate()
    elif days_until == 0:
        return "today"
    elif days_until == 1:
        return "tomorrow"
    elif days_until < 7:
        return coll_date.strftime("%A")
    elif now.year == coll_date.year:
        return '{}, <say-as interpret-as="date" format="md">{}</say-as>'.format(
            coll_date.strftime("%A"), coll_date.strftime("%m/%d"))
    else:
        return '{}, <say-as interpret-as="date" format="mdy">{}</say-as>'.format(
            coll_date.strftime("%A"), coll_date.strftime("%m/%d/%Y"))
