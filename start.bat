@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo =====================================
echo 🛡️  SOAR 平台 - 一键启动脚本
echo =====================================
echo.

REM 获取当前目录
set BASE_DIR=%cd%

echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python 环境正常

echo.
echo [2/5] 创建 Python 虚拟环境...
if not exist "backend\venv" (
    cd backend
    python -m venv venv
    cd ..
    echo ✅ 虚拟环境创建成功
) else (
    echo ✅ 虚拟环境已存在
)

echo.
echo [3/5] 安装后端依赖...
cd backend
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
cd ..
echo ✅ 后端依赖安装完成

echo.
echo [4/5] 启动 FastAPI 后端服务...
echo 📍 后端地址: http://localhost:8000
echo 📍 API 文档: http://localhost:8000/docs
start cmd /k "cd backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 /nobreak

echo.
echo [5/5] 启动 Vue3 前端服务...
echo 📍 前端地址: http://localhost:5173
echo.
echo 检查 npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 npm，请先安装 Node.js
    pause
    exit /b 1
)

cd frontend
if not exist "node_modules" (
    echo 首次安装依赖，请稍候...
    call npm install
) else (
    echo 依赖已准备就绪
)
start cmd /k "npm run dev"

echo.
echo =====================================
echo ✅ 系统启动完成！
echo =====================================
echo.
echo 📌 重要信息：
echo    • 后端服务: http://localhost:8000
echo    • 前端应用: http://localhost:5173
echo    • API文档: http://localhost:8000/docs
echo.
echo 💡 演示步骤：
echo    1. 打开浏览器访问 http://localhost:5173
echo    2. 进入"剧本执行"页面
echo    3. 提交测试告警或通过 API 提交
echo    4. 选择剧本后点击"执行"
echo    5. 查看工单和报告
echo.
echo 🎬 测试告警 API 命令：
echo.
echo    curl -X POST "http://localhost:8000/api/alert" ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"type\": \"phishing\", \"source\": \"email_gateway\", \"user\": \"test@company.com\", \"ioc\": \"http://fake-login-portal.com\", \"severity\": \"high\"}"
echo.
echo =====================================
echo.
pause
