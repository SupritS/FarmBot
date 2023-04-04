import requests
import json
import os
from dialogflow_api import detect_intent_texts
from speech2text import convert_and_translate
from text2speech import text_to_speech


class TeleBot:
    def __init__(self):
        self.token = "telegram token"  # write your token here!
        self.url = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self, offset=None):
        url = (
            self.url + "/getUpdates?timeout=100"
        )  # In 100 seconds if user input query then process that, use it as the read timeout from the server
        if offset:
            url = url + f"&offset={offset+1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)

    def get_file(self, file_path):
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"

        response = requests.get(url)

        return response

    def speech_text(self, chat_id, file_id, lang_code):
        url = f"https://api.telegram.org/bot{self.token}/getFile"

        payload = {"file_id": file_id}
        headers = {"accept": "application/json", "content-type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)

        json_reposne = json.loads(response.content)

        file_path = json_reposne["result"]["file_path"]
        response = self.get_file(file_path)

        file_name = file_path.strip("voice/")
        path = f"{os.getcwd()}/{chat_id}"
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, file_name), "wb") as f:
            f.write(response.content)

        text = convert_and_translate(os.path.join(path, file_name), lang_code)

        text = detect_intent_texts("google project id", chat_id, text, lang_code)

        file_path = text_to_speech(text, file_name, chat_id, lang_code)

        self.send_audio(chat_id, file_path)

    def send_audio(self, chat_id, response_path):
        with open(response_path, "rb") as audio:
            payload = {"chat_id": chat_id, "title": "response", "parse_mode": "HTML"}
            files = {
                "audio": audio.read(),
            }
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendAudio",
                data=payload,
                files=files,
            )

    def receive_message(self):
        pass

    def send_message(self, chat_id, message):
        payload = {
            "text": message,
            "parse_mode": "markdown",
            "disable_web_page_preview": False,
            "disable_notification": False,
            "reply_to_message_id": None,
            chat_id: chat_id,
        }
        headers = {"accept": "application/json", "content-type": "application/json"}

        url = self.url + f"/sendMessage?chat_id={chat_id}"

        requests.post(url, json=payload, headers=headers)

    def get_lang_code(self, chat_id):
        payload = {
            "text": "संचार के लिए अपनी पसंदीदा भाषा का चयन करें।\n\nसंवादासाठी तुमची पसंतीची भाषा निवडा.\n\nSelect your preferred language for communication.",
            "parse_mode": "markdown",
            "disable_web_page_preview": False,
            "disable_notification": False,
            "reply_to_message_id": None,
            chat_id: chat_id,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "मराठी", "callback_data": "mr"}],
                    [{"text": "हिंदी", "callback_data": "hi"}],
                    [{"text": "English", "callback_data": "en"}],
                ]
            },
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        token = "telegram token"  # write your token here!
        url = f"https://api.telegram.org/bot{token}"
        url = url + f"/sendMessage?chat_id={chat_id}"

        requests.post(url, json=payload, headers=headers)
