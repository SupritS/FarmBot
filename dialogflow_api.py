from google.cloud import dialogflow_v2beta1 as dialogflow
from google.protobuf.json_format import MessageToDict

import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "Path to your google application credential json file"


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    response_json = MessageToDict(response._pb)
    result = response_json["queryResult"]
    # text_1 = ''

    # for i in range(len(result['fulfillmentMessages'])):

    #     text_1 = (result['fulfillmentMessages'][i]['text']['text'][0])

    if result.get("allRequiredParamsPresent"):
        return result.get("fulfillmentText")
    return result.get("fulfillmentText")
