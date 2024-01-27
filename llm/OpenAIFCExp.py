# OpenAI 的 Function Call 示例程序

# 欢迎图案
welcome_art = """
————————————————————————————————————————————————————————————————————————
 ____            _           _        _    _ _         _     _ 
|  _ \\ _ __ ___ (_) ___  ___| |_     / \\  | | | ____ _(_) __| |
| |_) | '__/ _ \\| |/ _ \\/ __| __|   / _ \\ | | |/ / _` | |/ _` |
|  __/| | | (_) | |  __/ (__| |_   / ___ \\| |   < (_| | | (_| |
|_|   |_|  \\___// |\\___|\\___|\\__| /_/   \\_\\_|_|\\_\\__,_|_|\\__,_|
              |__/
————————————————————————————————————————————————————————————————————————
Function Call Example
————————————————————————————————————————————————————————————————————————
"""    

import os
import datetime
import httpx
from openai import OpenAI
from OpenAISetting import OPENAI_API_BASE, OPENAI_API_KEY
import json

class ChatWithOpenAI:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE,
            http_client=httpx.Client(
                base_url=OPENAI_API_BASE,
                follow_redirects=True,
            ),
        )
        self.messages = []
        self.saved_message_count = 0  # 追踪已保存的消息数
        # 准备计算器函数信息
        self.calculator_function_info = {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform a calculation using a simple single-step calculator function.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                        "operand1": {"type": "number"},
                        "operand2": {"type": "number"},
                    },
                    "required": ["operation", "operand1", "operand2"],
                },
            },
        }
        
    # 计算器Function
    def function_call_calculator(self, operation, operand1, operand2):
        """
        Simple calculator function. Single-step computation is supported only.

        Parameters:
        - operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide').
        - operand1 (float): The first operand.
        - operand2 (float): The second operand.

        Returns:
        - tuple: (result, error_message)
        - result (float): The result of the specified operation on the operands.
        - error_message (str): Error message if an error occurs, else an empty string.
        """
        result = 0.0
        error_message = ""

        if operation == 'add':
            result = operand1 + operand2
        elif operation == 'subtract':
            result = operand1 - operand2
        elif operation == 'multiply':
            result = operand1 * operand2
        elif operation == 'divide':
            if operand2 != 0:
                result = operand1 / operand2
            else:
                result = 0
                error_message = "Error: Division by zero is not allowed."

        return result, error_message

    def add_user_message(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

    def get_assistant_reply(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            tools=[self.calculator_function_info],
        )
        
        # Extract the assistant's reply
        assistant_reply = response.choices[0].message.content
        # Add assistant's reply to messages
        self.messages.append(response.choices[0].message)

        # Parse and handle function calls
        self.parse_function_call_response(response)

        # Check if a second_response is needed
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            # If there are function calls, create a second_response to get the model's reaction
            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
            )

            # Extract the assistant's reply
            assistant_reply_second = second_response.choices[0].message.content
            # Add assistant's reply to messages
            self.messages.append(second_response.choices[0].message)
            return assistant_reply_second
        else:
            # If no function calls, return the assistant's reply
            return assistant_reply

    def parse_function_call_response(self, response):
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            # 遍历每个函数调用
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_arguments = json.loads(tool_call.function.arguments)

                # 在这里，你可以根据函数的名称调用相应的函数，并传递参数
                if function_name == "calculator":
                    result = self.handle_calculator_function(function_arguments)

                # 如果有其他函数，继续添加相应的处理逻辑
                    
                # 将工具调用的消息添加到对话历史中
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })

    def handle_calculator_function(self, arguments):
        # 在这里，你可以编写处理 calculator 函数的逻辑
        operation = arguments.get("operation")
        operand1 = arguments.get("operand1")
        operand2 = arguments.get("operand2")

        # 执行计算逻辑，并处理结果
        result, error_message = self.function_call_calculator(operation, operand1, operand2)
        print(json.dumps({"result": result}))
        return json.dumps({"result": result})
    
    def save_chat_to_file(self, file_path):
        mode = 'a' if os.path.exists(file_path) else 'w'

        with open(file_path, mode, encoding="utf-8") as file:
            # 保存新增的对话内容
            new_messages = self.messages[self.saved_message_count:]
            for message in new_messages:
                if isinstance(message, dict):
                    role = message['role']
                    content = message['content']
                else:
                    role = message.role
                    content = message.content

                file.write(f"{role}: {content}\n")

            # 更新已保存的消息数
            self.saved_message_count = len(self.messages)

# 创建ChatWithOpenAI实例
chat_instance = ChatWithOpenAI()  

# 输出欢迎图案
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