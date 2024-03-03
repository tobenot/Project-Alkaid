# OpenAI 的 Embedding Search 示例程序

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
Embedding Search Example
————————————————————————————————————————————————————————————————————————
"""    

from openai import OpenAI
from OpenAISetting import OPENAI_API_BASE, OPENAI_API_KEY
import pickle
from scipy.spatial.distance import cosine
import numpy as np

class OpenAIEmbedSearch:
    def __init__(self, model_name="text-embedding-ada-002"):
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        self.model_name = model_name
        self.embeddings = []

    def create_embeddings(self, sentences):
        for sentence in sentences:
            response = self.client.embeddings.create(
                model = self.model_name,
                input = sentence
            )
            self.embeddings.append((sentence, response.data[0].embedding))
        
        with open('embeddings_database.pkl', 'wb') as f:
            pickle.dump(self.embeddings, f)

    def load_embeddings(self):
        with open('embeddings_database.pkl', 'rb') as f:
            self.embeddings = pickle.load(f)

    def search(self, sentence):
        query_embedding = self.client.embeddings.create(
            model = self.model_name,
            input = sentence
        ).data[0].embedding
        similarities = []

        for idx, embed in enumerate(self.embeddings):
            similarity = 1 - cosine(query_embedding, embed[1])
            similarities.append((idx, embed[0], similarity))

        # 将相似度列表按相似度从高到低排序
        similarities.sort(key=lambda x: x[2], reverse=True)

        # 输出排序后的列表
        for similarity in similarities:
            print(f"Embedding {similarity[0]+1}, Sentence: \"{similarity[1]}\", Similarity: {similarity[2]}")

        # 返回相似度最高的句子
        index = similarities[0][0]
        return self.embeddings[index]

if __name__ == "__main__":
    print(welcome_art)

    option = input("Enter 1 to create a database or 2 to search in the database: ")
    instance = OpenAIEmbedSearch()
    
    if option == '1':
        print("Enter your sentences, each on a new line, end with a line containing 'END':")
        sentences = []
        while True:
            sentence = input()
            if sentence == 'END':
                break
            sentences.append(sentence)
        instance.create_embeddings(sentences)
        print("Embeddings have been saved to 'embeddings_database.pkl'.")
    elif option == '2':
        instance.load_embeddings()
        sentence = input("Enter your search sentence: ")
        result = instance.search(sentence)
        print(f"The most similar sentence in the database is \"{result[0]}\", with a similarity score of {1 - cosine(result[1], instance.client.embeddings.create(model = instance.model_name, input = sentence).data[0].embedding)}.")
    else:
        instance.load_embeddings()
        sentence = option
        result = instance.search(sentence)
        print(f"The most similar sentence in the database is \"{result[0]}\", with a similarity score of {1 - cosine(result[1], instance.client.embeddings.create(model = instance.model_name, input = sentence).data[0].embedding)}.")