
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import speech_recognition as sr
import pyttsx3
import wikipedia

class ShivAssistant(App):
    def build(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.avatar = Image(source="assets/avatar_neutral.png")
        
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.chat_history = Label(text="Hello, I am Shiv!", size_hint=(1, 0.2))
        self.input = TextInput(hint_text="Ask me anything...", size_hint=(1, 0.1))
        self.button_speak = Button(text="🎤 Speak", size_hint=(1, 0.1))
        self.button_send = Button(text="Send", size_hint=(1, 0.1))
        
        self.button_speak.bind(on_press=self.listen_voice)
        self.button_send.bind(on_press=self.answer_text)
        
        layout.add_widget(self.avatar)
        layout.add_widget(self.chat_history)
        layout.add_widget(self.input)
        layout.add_widget(self.button_speak)
        layout.add_widget(self.button_send)
        
        return layout

    def speak(self, text):
        self.avatar.source = "assets/avatar_speaking.png"
        self.engine.say(text)
        self.engine.runAndWait()
        self.avatar.source = "assets/avatar_neutral.png"

    def listen_voice(self, instance):
        self.avatar.source = "assets/avatar_listening.png"
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
        try:
            query = self.recognizer.recognize_google(audio)
            self.chat_history.text = "You: " + query
            self.answer(query)
        except:
            self.chat_history.text = "Sorry, I didn't catch that."
        self.avatar.source = "assets/avatar_neutral.png"

    def answer_text(self, instance):
        query = self.input.text
        self.chat_history.text = "You: " + query
        self.answer(query)

    def answer(self, query):
        try:
            result = wikipedia.summary(query, sentences=1)
        except:
            result = "I don't know that yet."
        self.chat_history.text += "\nShiv: " + result
        self.speak(result)

if __name__ == "__main__":
    ShivAssistant().run()
