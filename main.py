import discord
import os
from groq import Groq

client_groq = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),  
)

SYSTEM_PROMPT = """You are PEC Bot, an AI assistant created by students of Punjab Engineering College (PEC). 
You are knowledgeable, friendly, and helpful in answering questions related to PEC, academics, coding, and general topics. 
Keep your responses concise, engaging, and student-friendly."""

def load_knowledge():
    try:
        with open("info.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No additional PEC knowledge available."

PEC_KNOWLEDGE = load_knowledge()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if self.user in message.mentions and message.author != self.user:
            try:
                user_message = message.content.replace(f'<@{self.user.id}>', '').strip()

                final_prompt = f"{SYSTEM_PROMPT}\n\nHere is some PEC-related information you should use:\n{PEC_KNOWLEDGE}\n\nUser: {user_message}\nPEC Bot:"

                chat_completion = client_groq.chat.completions.create(
                    messages=[
                        {"role": "user", "content": final_prompt}
                    ],
                    model="llama3-8b-8192",  
                )
                message_to_send = chat_completion.choices[0].message.content.strip()

                await message.channel.send(message_to_send)

            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("Sorry, I encountered an error while processing your request.")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
token = os.getenv("SECRET_KEY")

if token is None:
    print("SECRET_KEY environment variable not set. Exiting.")
    exit()

client.run(token)
