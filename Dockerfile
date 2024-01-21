# 使用官方Python基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /usr/src/app

# 将本地文件拷贝到容器中
COPY . .

# 安装程序所需的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量，使 Python 以交互模式运行
ENV PYTHONUNBUFFERED 1

# 运行你的Python程序
CMD python llm/OpenAIChatExp.py
