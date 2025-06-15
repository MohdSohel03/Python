import datetime
import random

def get_response(user_input):
    user_input = user_input.lower()

    greetings = ['hello', 'hi', 'hey']
    farewells = ['bye', 'exit', 'goodbye']
    gratitude = ['thanks', 'thank you']

    if any(word in user_input for word in greetings):
        return random.choice(["Hi there! 😊", "Hello! How can I help you?", "Hey! Need anything?"])

    elif any(word in user_input for word in farewells):
        return random.choice(["Goodbye! 👋", "Take care!", "Bye! Have a nice day!"])

    elif 'your name' in user_input:
        return "I’m PyBot 🤖, your friendly chatbot!"

    elif 'how are you' in user_input:
        return "I'm doing great! Thanks for asking 😄"

    elif 'time' in user_input:
        now = datetime.datetime.now()
        return f"⏰ The current time is {now.strftime('%H:%M:%S')}"

    elif 'date' in user_input:
        today = datetime.date.today()
        return f"📅 Today's date is {today.strftime('%B %d, %Y')}"

    elif 'creator' in user_input or 'who made you' in user_input:
        return "I was created by Mohd Sohel, a Python developer! 👨‍💻"

    elif 'weather' in user_input:
        return "I can't fetch real weather yet, but it's always sunny in Python! ☀️"

    elif any(word in user_input for word in gratitude):
        return "You're welcome! 😊"

    else:
        return "I'm not sure how to respond to that. Can you try something else?"

def run_chatbot():
    print("🤖 PyBot at your service! (Type 'bye' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'exit']:
            print("Bot:", get_response(user_input))
            break
        response = get_response(user_input)
        print("Bot:", response)

run_chatbot()
