class Chat:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append({message})

    def get_messages(self):
        return self.messages

if __name__ == "__main__":
    chat = Chat()
    
    while True:
        message = input("Enter your message: ")
        chat.add_message(message)
        
        print("\nChat History:")
        for msg in chat.get_messages():
            print(msg)
        print("\n")