from telegram_handler import TeleBot
from dialogflow_api import detect_intent_texts

update_id = None
lang_log = {}

lang_code = ["hi", "en", "mr"]

while True:
    tbot = TeleBot()
    updates = tbot.get_updates(offset=update_id)
    updates = updates["result"]

    if updates:
        print(updates)
        for items in updates:
            update_id = items["update_id"]
            if "callback_query" in items:
                chat_id = items["callback_query"]["from"]["id"]
                callback_data = items["callback_query"]["data"]
                if callback_data in lang_code:
                    lang_log[chat_id] = callback_data
                    if callback_data == "en":
                        tbot.send_message(
                            chat_id,
                            "Hey, welcome to AgriAllies we are here to help the farmers of India with related agriculture practices, crop's prices in the district, a community page for farmers to ask questions or share their suggestions/opinions 's and weather updates!You can ask common agriculture questions to us and get an AI-generated answer which will be trained on the data from the community answer's given by experienced farmers.(Add *ask!* before the question to get the answer)",
                        )
                    if callback_data == "hi":
                        tbot.send_message(
                            chat_id,
                            "AgriAllies में आपका स्वागत है हम यहां भारत के किसानों को संबंधित कृषि पद्धतियों, जिले में फसल की कीमतों, किसानों से सवाल पूछने या उनके सुझाव/राय और मौसम अपडेट साझा करने के लिए एक सामुदायिक पृष्ठ के साथ मदद करने के लिए हैं!आप हमसे सामान्य कृषि प्रश्न पूछ सकते हैं और एआई-जनित उत्तर प्राप्त कर सकते हैं, जिसे अनुभवी किसानों द्वारा दिए गए सामुदायिक उत्तरों के डेटा पर प्रशिक्षित किया जाएगा।",
                        )
                    if callback_data == "mr":
                        tbot.send_message(
                            chat_id,
                            "AgriAllies मध्ये आपले स्वागत आहे आम्ही भारतातील शेतकऱ्यांना संबंधित कृषी पद्धती, जिल्ह्यातील पिकांच्या किमती, शेतकऱ्यांना प्रश्न विचारण्यासाठी किंवा त्यांच्या सूचना/मत आणि हवामानाच्या अपडेट्स शेअर करण्यासाठी एक समुदाय पेज मदत करण्यासाठी येथे आहोत!तुम्ही आम्हाला सामान्य शेतीविषयक प्रश्न विचारू शकता आणि AI-व्युत्पन्न उत्तर मिळवू शकता जे अनुभवी शेतकऱ्यांनी दिलेल्या सामुदायिक उत्तरांच्या डेटावर प्रशिक्षित केले जाईल.",
                        )

            if "message" in items:
                chat_id = items["message"]["chat"]["id"]

                if "entities" in items["message"]:
                    if "/start" in items["message"]["text"]:
                        tbot.get_lang_code(chat_id)
                    break

                if "text" in items["message"]:
                    text = items["message"]["text"]
                    text = detect_intent_texts(
                        "google project id", chat_id, text, lang_log[chat_id]
                    )
                    tbot.send_message(chat_id, text)

                if "voice" in items["message"]:
                    file_id = items["message"]["voice"]["file_id"]
                    chat_id = items["message"]["from"]["id"]
                    tbot.speech_text(chat_id, file_id, lang_log[chat_id])
