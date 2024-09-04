import pyttsx3
import speech_recognition as sr
from twilio.rest import Client
import geocoder

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init("sapi5")

def get_current_location():
    # Fetch the current location based on the IP address
    location = geocoder.ip('me')
    if location:
        return f"Latitude: {location.latlng[0]}, Longitude: {location.latlng[1]}"
    return "Location not available"

def send_sms_alert(message, to_phone):
    account_sid = ''
    auth_token = ''
    from_phone = ''

    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=from_phone,
        to=to_phone
    )

while True:
    try:
        with sr.Microphone() as mic:
            # Adjust for ambient noise to improve recognition accuracy
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            print("Listening: ")

            recognizer.pause_threshold = 1

            # Listen to the audio input
            audio = recognizer.listen(mic)

            # Recognize speech using Google's API
            text = recognizer.recognize_google(audio, language='en-in')
            text = text.lower()

            print(f"Recognized: {text}")

            if "help" in text or "sos" in text:
                # Get the current location
                location = get_current_location()

                # Prepare the alert message
                alert_message = f"Alert: Need Help!\nLocation: {location}"

                # Send the alert SMS
                send_sms_alert(alert_message, "+917042028851")
                print("Alert sent!")

    except sr.UnknownValueError:
        # Handle case where speech is unintelligible
        print("Sorry, I didn't catch that. Could you please repeat?")

    except sr.RequestError:
        # Handle errors in the recognition request, such as network issues
        print("There was an issue with the request; please check your internet connection.")
        break

    except KeyboardInterrupt:
        # Gracefully exit the loop on a keyboard interrupt (Ctrl+C)
        print("Exiting the program.")
        break
