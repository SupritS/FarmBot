from flask import Flask, request
from weather_api import get_temp
from google.cloud import dialogflow_v2beta1 as dialogflow
from fine_tuning import custom_data
from dialogflow_api import detect_intent_texts
from translate import translator
import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "Path to your google application credential json file"

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    response = request.get_json(force=True)
    intent = response["queryResult"]["intent"]["displayName"]
    language_code = response["queryResult"]["languageCode"]

    details = {
        "commodities": {
            "onion": {
                "districts": {
                    "pune": [
                        {
                            "market": "Pune(Moshi)",
                            "max_rate": "Rs. 900/Quintal",
                            "min_rate": "Rs. 300/Quintal",
                            "date": "24-03-2023",
                        },
                        {
                            "market": "Pune(Pimpri)",
                            "max_rate": "Rs. 800/Quintal",
                            "min_rate": "Rs. 700/Quintal",
                            "date": "24-03-2023",
                        },
                    ],
                    "satara": [
                        {
                            "market": "Karad",
                            "max_rate": "Rs. 1,500/Quintal",
                            "min_rate": "Rs. 1,000/Quintal",
                            "date": "24-03-2023",
                        },
                        {
                            "market": "Lonand",
                            "max_rate": "Rs. 1,311",
                            "min_rate": "Rs. 400/Quintal",
                            "date": "24-03-2023",
                        },
                    ],
                }
            },
            "carrot": {
                "districts": {
                    "pune": [
                        {
                            "market": "Khed(Chakan)",
                            "max_rate": "Rs. 1,500/Quintal",
                            "min_rate": "Rs. 1,000/Quintal",
                            "date": "24-03-2023",
                        },
                        {
                            "market": "Pune(Moshi)",
                            "max_rate": "Rs. 2,000/Quintal",
                            "min_rate": "Rs. 1,000/Quintal",
                            "date": "24-03-2023",
                        },
                    ],
                    "nagpur": [
                        {
                            "market": "Ramtek",
                            "max_rate": "Rs. 2,000/Quintal",
                            "min_rate": "Rs. 1,800/Quintal",
                            "date": "24-03-2023",
                        }
                    ],
                }
            },
        }
    }

    if intent == "Get weather update":
        geo_name = response["queryResult"]["parameters"]["place"]
        temp = get_temp(geo_name)
        text = f"The current tempreature in {geo_name} is {temp}"
        if language_code == "mr":
            text = translator(text, language_code)
            fulfillmentText = {"fulfillmentText": text}
        if language_code == "en":
            fulfillmentText = {"fulfillmentText": text}
        if language_code == "hi":
            text = translator(text, language_code)
            fulfillmentText = {"fulfillmentText": text}

    if intent == "Mandi Rates":
        geo_name = response["queryResult"]["parameters"]["place"]
        commodity = response["queryResult"]["parameters"]["commodity"]

        markets = details["commodities"][commodity]["districts"][geo_name.lower()]
        reply = ""
        for i in range(len(markets)):
            market = markets[i]
            if i == 0:
                reply = (
                    f"market rate of {commodity} in "
                    + market.get("market")
                    + " is max "
                    + market.get("max_rate")
                    + " and minimum is "
                    + market.get("min_rate")
                )
            if i > 0:
                reply += (
                    ",in "
                    + market.get("market")
                    + " is max "
                    + market.get("max_rate")
                    + " and minimum is "
                    + market.get("min_rate")
                )

        text = translator(reply, language_code)

        fulfillmentText = {"fulfillmentText": text}

    if intent == "farming pratices":
        prompt = response["queryResult"]["queryText"]
        prompt = prompt.replace("ask!", "")
        text = custom_data(prompt)
        fulfillmentText = {"fulfillmentText": text}

    return fulfillmentText


@app.route("/get-reply", methods=["POST"])
def reply():
    response = request.get_json(force=True)
    unique_id = response.get("phone_number")
    message = response.get("received_text")
    language_code = response.get("language_code")
    reply_user = detect_intent_texts("agri-bot-smjr", unique_id, message, language_code)
    return reply_user


if (__name__) == "__main__":
    app.run(port=8000, debug=True)
