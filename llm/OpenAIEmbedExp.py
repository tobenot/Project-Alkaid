# OpenAI 的 Embedding 两个句子的嵌入向量 比较 示例程序

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
Embedding Compare Example
————————————————————————————————————————————————————————————————————————
"""    

import os
import datetime
from openai import OpenAI
from OpenAISetting import OPENAI_API_BASE, OPENAI_API_KEY
import traceback
from scipy.spatial.distance import cosine

class ChatWithOpenAI:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        self.messages = []

    def get_assistant_reply_object(self, user_input):
        response = self.client.embeddings.create(
            model = "text-embedding-ada-002",
            input= user_input
        )
        # Extract the assistant's reply and other fields
        assistant_reply = response.data[0].embedding
        assistant_index = response.data[0].index
        assistant_model = response.model
        assistant_object = response.object

        return {
            "embedding": assistant_reply,
            "index": assistant_index,
            "model": assistant_model,
            "object": assistant_object
        }

    # 新增计算两个嵌入向量余弦相似度的函数
    def calculate_similarity(self, vec1, vec2):
        similarity = 1 - cosine(vec1, vec2)
        return similarity

if __name__ == "__main__":
    try:
        # 创建ChatWithOpenAI实例
        chat_instance = ChatWithOpenAI()

        # 输出欢迎图案
        print(welcome_art)

        # 获取第一个句子输入
        print("Enter the first sentence:")
        first_sentence = input("First Sentence: ")

        # 获取第一个句子的嵌入
        first_embedding = chat_instance.get_assistant_reply_object(first_sentence)['embedding']

        # 获取第二个句子输入
        print("Enter the second sentence:")
        second_sentence = input("Second Sentence: ")

        # 获取第二个句子的嵌入
        second_embedding = chat_instance.get_assistant_reply_object(second_sentence)['embedding']

        # 计算这两个嵌入的相似度
        similarity = chat_instance.calculate_similarity(first_embedding, second_embedding)
        print(f"The similarity between the two sentences is: {similarity}")
                    
    except Exception as e:
        # 捕获整个程序的异常
        error_message = f"An unexpected error occurred: {str(e)}"
        traceback.print_exc()  # 打印完整的异常信息

