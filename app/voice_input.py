import speech_recognition as sr

def get_voice_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query
    except sr.UnknownValueError:
        return "Sorry, could not understand."
    except sr.RequestError as e:
        return f"Error from Google API: {e}"