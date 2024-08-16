import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response.choices[0].message["content"]
    except openai.error.OpenAIError as e:
        text += f"Error: {e}"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

    return text
def say(text):
    # Escape double quotes in the text
    text = text.replace('"', '""')
    
    # Create the VBScript code for text-to-speech
    vbscript_code = f"""
    Set sapi = CreateObject("SAPI.SpVoice")
    sapi.Speak "{text}"
    """
    
    # Save the VBScript code to a temporary file
    with open("temp_say.vbs", "w") as vbscript_file:
        vbscript_file.write(vbscript_code)
    
    # Run the VBScript file using os.system
    os.system("cscript temp_say.vbs")
    
    # Optionally, remove the temporary VBScript file
    os.remove("temp_say.vbs")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        try:
            audio = r.listen(source)
        except sr.WaitTimeoutError:
            print("Timeout error: No audio input received")
            return "None"
        except sr.UnknownValueError:
            print("Unknown value error: Unable to recognize speech")
            return "None"
        except sr.RequestError as e:
            print(f"Request error: {e}")
            return "None"
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Unknown value error: Unable to recognize speech")
            return "None"
        except sr.RequestError as e:
            print(f"Request error: {e}")
            return "None"

def open_sites(voice_command_sites):
    sites = {
        "wikipedia": "https://www.wikipedia.org/",
        "youtube": "https://www.youtube.com/",
        "chess.com": "https://www.chess.com/",
        "whatsapp":"https://web.whatsapp.com/",
        # Add more sites here
    }
    for site, url in sites.items():
        if site in voice_command_sites.lower():
            try:
                webbrowser.open(url)
                print(f"Opening {site.capitalize()}: {url}")
                say(f"Opening {site.capitalize()} master")
            except Exception as e:
                print(f"Error opening {site.capitalize()}: {e}")
            return

def play_music():
    try:
        webbrowser.open("https://www.youtube.com/watch?v=TO-_3tck2tg")
        print("Playing music...")
        say("Playing music master")
    except Exception as e:
        print(f"Error playing music: {e}")

def tell_time():
    try:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"Current time: {current_time}")
        say(f"Current time is {current_time} master")
    except Exception as e:
        print(f"Error telling time: {e}")

def open_app(voice_command_app):
    app = {
        "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "control pannel": "C:\\Windows\\System32\\control.exe",
            
        }
        
    for app_name, location in app.items():
        if app_name in voice_command_app.lower():
            try:
                os.startfile(location)
                print(f"Opening {app_name.capitalize()}: {location}")
                say(f"Opening {app_name.capitalize()} master")
            except Exception as e:
                print(f"Error opening {app_name.capitalize()}: {e}")
            return

def main():
    print('Welcome to Jarvis A.I')
    say("Master I am Jarvis A I")
    while True:
        try:
            voice_command = takecommand()
            query = voice_command
            if voice_command is not None:
                if "open" in voice_command.lower():
                    open_sites(voice_command)
                elif "run" in voice_command.lower():
                    open_app(voice_command)
                elif "play music" in voice_command.lower():
                    play_music()
                elif "what's the time" in voice_command.lower():
                    tell_time()
                elif "intelligence".lower() in voice_command.lower():
                    response = ai(voice_command)
                    print(response)
                    say(response)
                else:
                    print("Unknown command master")
                    say("Unknown command master")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
