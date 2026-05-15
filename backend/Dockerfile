FROM python:3.10-slim

WORKDIR /app

# 先复制依赖清单，并配置国内镜像源以加速安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制后端的所有源代码
COPY . .

# 暴露 FastAPI 运行的 8000 端口
EXPOSE 8000

# 启动 uvicorn 服务
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
