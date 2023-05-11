import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pyaudio
import datetime
import webbrowser
import os
import random
import wikipedia
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Create the main window
window = tk.Tk()
window.title("Voice Assistant")

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to process the user's query
def process_query():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        print("Processing...")

    try:
        query = recognizer.recognize_google(audio)
        print("User Query:", query)

        # Process the user's query
        if "What is the time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            pyttsx3.speak(f"The current time is {current_time}")

        elif "What is the date today" in query:
            current_date = datetime.date.today().strftime("%B %d, %Y")
            pyttsx3.speak(f"Today's date is {current_date}")

        elif "what is the weather today" in query:
            # Fetch weather data from an API (replace 'YOUR_API_KEY' with your actual API key)
            api_key = "YOUR_API_KEY"
            city = "New York"  # Replace with the desired city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            weather_data = response.json()
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            pyttsx3.speak(f"The current temperature in {city} is {temperature} Kelvin with {description}")

        elif "open YouTube" in query:
            webbrowser.open("https://www.youtube.com")

        elif "play music" in query:
            music_folder = "F:\Songs™\Songs"  # Replace with the path to your music folder
            songs = os.listdir(music_folder)
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_folder, random_song))

        elif "open Instagram" in query:
            webbrowser.open("https://www.instagram.com")

        elif "open WhatsApp" in query:
            webbrowser.open("https://web.whatsapp.com")

        elif "open Gmail" in query:
            webbrowser.open("https://mail.google.com")

        elif "rock paper scissors" in query:
            choices = ["rock", "paper", "scissors"]
            computer_choice = random.choice(choices)
            pyttsx3.speak(f"The computer chose {computer_choice}")

        elif "search" in query:
            search_query = query.replace("search", "")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "tell me about" in query:
            search_query = query.replace("tell me about", "")
            summary = wikipedia.summary(search_query, sentences=2)
            pyttsx3.speak(f"Here's what I found on Wikipedia: {summary}")

        elif "send email" in query:
            # Configure the email settings
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "your_email@gmail.com"  # Replace with your email address
            sender_password = "your_password"  # Replace with your email password

            try:
                engine.say("What is the recipient's email address?")
                engine.runAndWait()
                recipient_email = input("Recipient's Email Address: ")

                engine.say("What should be the subject of the email?")
                engine.runAndWait()
                subject = input("Email Subject: ")

                engine.say("What is the content of the email?")
                engine.runAndWait()
                content = input("Email Content: ")

                # Create the email message
                msg = EmailMessage()
                msg["From"] = sender_email
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.set_content(content)

                # Connect to the SMTP server and send the email
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)

                engine.say("Email sent successfully!")
                engine.runAndWait()

            except Exception as e:
                engine.say("Sorry, I encountered an error while sending the email.")
                print(str(e))

        elif "schedule event" in query:
            engine.say("What is the event title?")
            engine.runAndWait()
            event_title = input("Event Title: ")

            engine.say("When is the event date? Please provide in the format 'YYYY-MM-DD'.")
            engine.runAndWait()
            event_date = input("Event Date (YYYY-MM-DD): ")

            engine.say("What is the event start time? Please provide in the format 'HH:MM AM/PM'.")
            engine.runAndWait()
            event_start_time = input("Event Start Time (HH:MM AM/PM): ")

            engine.say("What is the event end time? Please provide in the format 'HH:MM AM/PM'.")
            engine.runAndWait()
            event_end_time = input("Event End Time (HH:MM AM/PM): ")

            # Configure the Google Calendar API settings (replace 'credentials.json' with your credentials file)
            credentials_file = "credentials.json"
            credentials = service_account.Credentials.from_service_account_file(credentials_file)
            service = build("calendar", "v3", credentials=credentials)

            try:
                # Create the event start and end datetime objects
                event_start = datetime.datetime.strptime(event_date + " " + event_start_time, "%Y-%m-%d %I:%M %p")
                event_end = datetime.datetime.strptime(event_date + " " + event_end_time, "%Y-%m-%d %I:%M %p")

                # Convert the event start and end datetime objects to UTC timezone
                event_start = pytz.timezone("UTC").localize(event_start)
                event_end = pytz.timezone("UTC").localize(event_end)

                # Create the event body
                event = {
                    "summary": event_title,
                    "start": {"dateTime": event_start.isoformat()},
                    "end": {"dateTime": event_end.isoformat()},
                }

                # Insert the event into the user's calendar
                calendar_id = "primary"  # Use 'primary' for the primary calendar of the authenticated user
                service.events().insert(calendarId=calendar_id, body=event).execute()

                engine.say("Event scheduled successfully!")
                engine.runAndWait()

            except Exception as e:
                engine.say("Sorry, I encountered an error while scheduling the event.")
                print(str(e))

        else:
            pyttsx3.speak("I'm sorry, I couldn't understand your query.")

    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError:
        print("Sorry, I'm currently unavailable.")

# Function to handle the mic button click event
def mic_button_click():
    engine.say("Hi, how may I help you?")
    engine.runAndWait()
    process_query()

# Create the mic button
mic_button_img = tk.PhotoImage(file="mic.png")  # Replace "mic.png" with your mic button image file
mic_button = tk.Button(window, image=mic_button_img, command=mic_button_click)
mic_button.pack()

# Start the GUI event loop
window.mainloop()


