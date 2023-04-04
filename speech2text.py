from pydub import AudioSegment
import speech_recognition as sr


def convert_and_translate(file_path, lang_code):
    ofn = file_path
    wfn = ofn.replace(".oga", ".wav")
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format="wav")

    r = sr.Recognizer()

    harvard = sr.AudioFile(wfn)
    with harvard as source:
        audio = r.record(source)

    return r.recognize_google(audio, language=lang_code)
