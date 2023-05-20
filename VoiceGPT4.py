import openai
import pyttsx3
import speech_recognition as sr
import time

# Open AI Key
openai.api_key = "----INSERT Your API KEY HERE----"

# Iniciar Text para Speech Engine.
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as Source:
        audio = recognizer.record(Source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unkown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for user to say "genius"
        print("Say 'Book' to start recording...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "book":
                    #Record the rest ot the sentence.
                    filename = "input.wav"
                    print("Im all ears!(^///^)")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    #Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said: {text}")
                        
                        #generate response with gpt-3
                        response = generate_response(text)
                        print(f"Book Says: {response}")
                        
                        #Read Response
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
