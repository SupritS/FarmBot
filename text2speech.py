from gtts import gTTS
import os


def text_to_speech(text, file_name, chat_id, language_code):
    path = f"{os.getcwd()}/{chat_id}/response"
    if not os.path.exists(path):
        os.mkdir(path)
    myobj = gTTS(text=text, lang=language_code, slow=False)
    file_path = os.path.join(path, file_name.replace(".oga", ".mp3"))
    myobj.save(file_path)
    return file_path
