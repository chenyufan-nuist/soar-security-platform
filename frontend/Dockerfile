# 阶段 1：构建阶段
FROM node:22-alpine AS builder

WORKDIR /app

# 复制 package 文件并安装依赖（利用 Docker 缓存机制）
COPY package*.json ./
RUN npm install

# 复制源代码并进行打包构建
COPY . .
RUN npm run build

# 阶段 2：运行阶段（使用 Nginx 提供前端网页服务，体积小速度快）
FROM nginx:alpine

# 将构建得到的产物复制到 nginx 静态资源目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
