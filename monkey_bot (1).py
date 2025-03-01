import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk
import random
import pyttsx3
import speech_recognition as sr
import math
import threading
import pyjokes

# Function to install required libraries
def install_libraries(libs):
    for lib in libs:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"Successfully installed {lib}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {lib}")

# Install required libraries
install_libraries(['Pillow', 'pyttsx3', 'speechrecognition', 'pyjokes'])

# --- Swinging Monkey Animation ---
class SwingingMonkeyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swinging Monkey Bot")
        self.root.geometry("400x400")
        
        # Load monkey image
        self.monkey_image = Image.open("monkey.png")  # Ensure you have an image named monkey.png
        self.monkey_image = self.monkey_image.resize((100, 100))  # Resize to fit inside the box
        self.monkey = ImageTk.PhotoImage(self.monkey_image)

        # Create canvas to place the image
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack()

        # Place the monkey at the starting position
        self.monkey_id = self.canvas.create_image(200, 200, image=self.monkey)

        # Animation parameters
        self.angle = 0
        self.swing_speed = 5  # Speed of the swing
        self.amplitude = 80  # How wide the swing is

        # Start the animation
        self.animate()

    def animate(self):
        # Calculate new x position based on angle for the swing
        x_offset = self.amplitude * math.sin(math.radians(self.angle))

        # Move the monkey image
        self.canvas.coords(self.monkey_id, 200 + x_offset, 200)

        # Increase the angle to make the monkey swing back and forth
        self.angle += self.swing_speed
        if self.angle > 30 or self.angle < -30:
            self.swing_speed = -self.swing_speed

        # Call the animate function every 20ms (to make it look smooth)
        self.root.after(20, self.animate)

# --- Bot Functionality ---
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to make the bot speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is not working right now.")
        return None

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to tell a fun fact
def tell_fact():
    facts = [
        "Did you know that honey never spoils?",
        "The Eiffel Tower can be 15 cm taller during the summer.",
        "A day on Venus is longer than a year on Venus.",
        "Octopuses have three hearts!",
        "Bananas are berries, but strawberries aren't."
    ]
    fact = random.choice(facts)
    speak(fact)

# Main bot function
def run_bot():
    speak("Hello! I'm your friendly bot. How can I assist you today?")
    while True:
        command = listen()
        if command:
            if 'joke' in command:
                tell_joke()
            elif 'fact' in command:
                tell_fact()
            elif 'stop' in command or 'goodbye' in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("Sorry, I didn't understand that. Please ask for a joke or a fact.")

# --- Main Program ---
def start_bot():
    # Start the bot in a separate thread to avoid blocking the GUI
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SwingingMonkeyApp(root)
    start_bot()  # Start the bot in a separate thread
    root.mainloop()
