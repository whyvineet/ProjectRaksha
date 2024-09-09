import tkinter as tk
from tkinter import ttk, messagebox
import threading
import speech_recognition as sr
import pyttsx3
import geocoder
from twilio.rest import Client


class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Voice-Activated SOS System")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.create_widgets()

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.alert_word = ""
        self.contact = ""

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Voice-Activated SOS System", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Alert Word:").pack(side=tk.LEFT, padx=5)
        self.alert_word_entry = ttk.Entry(input_frame, width=20)
        self.alert_word_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Emergency Contact:").pack(side=tk.LEFT, padx=5)
        self.contact_entry = ttk.Entry(input_frame, width=20)
        self.contact_entry.pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(button_frame, text="Start Listening for Trigger", command=self.start_listening)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.listen_keyword_button = ttk.Button(button_frame, text="Set Alert Word via Voice", command=self.listen_for_alert_word)
        self.listen_keyword_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(button_frame, text="Stop Listening", command=self.stop_listening,
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(main_frame, text="System is inactive", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.location_label = ttk.Label(main_frame, text="Location: Not available", font=("Helvetica", 12))
        self.location_label.pack(pady=10)

        self.log_text = tk.Text(main_frame, height=10, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=10)

    def start_listening(self):
        self.contact = self.contact_entry.get()
        if not self.contact:
            messagebox.showerror("Error", "Please enter an emergency contact.")
            return
        if not self.alert_word:
            messagebox.showerror("Error", "Please set an alert word first.")
            return

        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Listening for the alert word...")

        self.update_location()

        threading.Thread(target=self.listen_for_trigger_word, daemon=True).start()

    def stop_listening(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="System is inactive")

    def listen_for_alert_word(self):
        threading.Thread(target=self.voice_alert_word_selection, daemon=True).start()

    def voice_alert_word_selection(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.log("Please say the alert word...")
                audio = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio).lower()
            self.log(f"Recognized: {text}")

            if messagebox.askyesno("Confirmation", f"Is '{text}' your alert word?"):
                self.alert_word = text
                self.alert_word_entry.delete(0, tk.END)  # Clear the entry box
                self.alert_word_entry.insert(0, text)  # Set the alert word in the entry box
                self.log(f"Alert word set to: {self.alert_word}")
            else:
                self.log("Alert word confirmation rejected.")

        except sr.UnknownValueError:
            self.log("Could not understand audio")
        except sr.RequestError:
            self.log("Could not request results; check your internet connection")

    def listen_for_trigger_word(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source)

                text = self.recognizer.recognize_google(audio).lower()
                self.log(f"Recognized: {text}")

                if self.alert_word in text:
                    self.trigger_alert()
                    break

            except sr.UnknownValueError:
                self.log("Could not understand audio")
            except sr.RequestError:
                self.log("Could not request results; check your internet connection")

        self.stop_listening()

    def trigger_alert(self):
        self.log("Alert word detected! Sending SOS...")
        self.status_label.config(text="Alert triggered! Sending SOS...")

        location = self.get_location()
        if self.contact:
            message = f"SOS Alert! Need help! Location: {location}"
            self.send_sms(message)
        else:
            self.log("No emergency contact provided. Unable to send SMS.")

        messagebox.showinfo("Alert Triggered", f"SOS alert sent!\nLocation: {location}")

    def update_location(self):
        location = self.get_location()
        self.location_label.config(text=f"Location: {location}")

    def get_location(self):
        location = geocoder.ip('me')
        if location:
            return f"Latitude: {location.latlng[0]}, Longitude: {location.latlng[1]}"
        return "Not available"

    def send_sms(self, message):
        # Replace with your Twilio credentials
        account_sid = 'account_sid'
        auth_token = 'auth_token'
        from_number = 'phone_no'

        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=message,
                from_=from_number,
                to=self.contact
            )
            self.log(f"SMS sent to {self.contact}")
        except Exception as e:
            self.log(f"Failed to send SMS: {str(e)}")

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()
