import speech_recognition as sr
from speech_recognition import Recognizer, Microphone


class VoiceRecognition:

    def call_me(self):
        self.register_voice()
        self.voice_to_text()

    def register_voice(self):
        recognizer = Recognizer()

        # enregistrement du son
        with Microphone() as source:
            print("Réglage du bruit ambiant... Patientez...")
            recognizer.adjust_for_ambient_noise(source)
            print("Vous pouvez parler...")
            audio = recognizer.listen(source)
            print("Enregistrement terminé !")
            with open('record.wav', 'wb') as f:
                f.write(audio.get_wav_data())

    def voice_to_text(self):
        r = sr.Recognizer()

        with sr.AudioFile("record.wav") as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="fr-FR")
            print("The audio file contains: " + text)

            with open("command.txt", "w") as file:
                file.write(text)
                print("Text file saved: command.txt")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
