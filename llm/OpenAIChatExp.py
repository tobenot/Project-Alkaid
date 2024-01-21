import os
import datetime
from openai import OpenAI
from OpenAISetting import OPENAI_API_BASE, OPENAI_API_KEY

class ChatWithOpenAI:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        self.messages = []

    def add_user_message(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    def get_assistant_reply(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # Add assistant's reply to messages
        self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    
    def save_chat_to_file(self, file_path):
        mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode) as file:
            # 只保存新增的对话内容
            new_messages = self.messages[len(self.messages) - 1:]
            for message in new_messages:
                role = message["role"]
                content = message["content"]
                file.write(f"{role}: {content}\n")

# 创建ChatWithOpenAI实例
chat_instance = ChatWithOpenAI()

# 输出欢迎图案
welcome_art = """
————————————————————————————————————————————————————————————————————————
 ____            _           _        _    _ _         _     _ 
|  _ \\ _ __ ___ (_) ___  ___| |_     / \\  | | | ____ _(_) __| |
| |_) | '__/ _ \\| |/ _ \\/ __| __|   / _ \\ | | |/ / _` | |/ _` |
|  __/| | | (_) | |  __/ (__| |_   / ___ \\| |   < (_| | | (_| |
|_|   |_|  \\___// |\\___|\\___|\\__| /_/   \\_\\_|_|\\_\\__,_|_|\\__,_|
              |__/
————————————————————————————————————————————————————————————————————————
Chat Example
————————————————————————————————————————————————————————————————————————
"""                    

print(welcome_art)

# 输出用户提示
user_prompt = "You can ask me anything, or type 'exit' to end the conversation."
print(user_prompt)


# 设置文件名为当前时间
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
directory = "saved/chatHistory"
os.makedirs(directory, exist_ok=True)
file_path = os.path.join(directory, f"chat_history_{current_time}.txt")

while True:
    # 获取用户输入
    user_input = input("User: ")

    # 如果用户输入"exit"，退出循环
    if user_input.lower() == "exit":
        print(f"Chat history saved to {file_path}")
        break

    # 将用户输入添加到对话历史
    chat_instance.add_user_message(user_input)

    # 保存最新一句对话历史到文件
    chat_instance.save_chat_to_file(file_path)

    # 获取助手回复
    assistant_reply = chat_instance.get_assistant_reply()

    # 打印助手回复
    print("Assistant:", assistant_reply)

    # 保存最新一句对话历史到文件
    chat_instance.save_chat_to_file(file_path)