@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo =====================================
echo   SOAR 平台 - 一键启动脚本
echo =====================================
echo.

REM 获取当前目录
set BASE_DIR=%cd%

echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo [ OK ] Python 环境正常

echo.
echo [2/5] 创建 Python 虚拟环境...
if not exist "backend\venv" (
    cd backend
    python -m venv venv
    cd ..
    echo [ OK ] 虚拟环境创建成功
) else (
    echo [ OK ] 虚拟环境已存在
)

echo.
echo [3/5] 安装后端依赖 (请耐心等待)...
cd backend
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [错误] 后端依赖安装失败！请检查上面的错误信息。
    pause
    exit /b 1
)
cd ..
echo [ OK ] 后端依赖安装完成

echo.
echo [3.5/5] 检查环境配置...
if not exist "backend\.env" (
    echo [WARN] 未检测到 backend\.env，正在从模板创建...
    copy backend\.env.example backend\.env >nul
    echo [ OK ] 已创建 backend\.env
    echo.
    echo [WARN] ==============================================
    echo [WARN] 智能助手需要 DeepSeek API Key 才能使用！
    echo [WARN] 请编辑 backend\.env 文件，将 your-api-key-here
    echo [WARN] 替换为你的真实 API Key。
    echo [WARN] 或者：打开前端后点击智能助手齿轮图标直接填入
    echo [WARN] ==============================================
    echo.
) else (
    echo [ OK ] 环境配置已就绪
)

echo.
echo [4/5] 启动 FastAPI 后端服务...
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo *** 请勿关闭此窗口！这是后端服务 ***
echo.
cd backend
call venv\Scripts\activate.bat
start "SOAR Backend" cmd /k "cd /d %cd% && call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
cd ..

echo 等待后端启动 (5秒)...
timeout /t 5 /nobreak >nul

echo 验证后端是否就绪...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [WARN] 后端可能未成功启动，请检查 "SOAR Backend" 窗口中的错误信息
    echo        如果报 ModuleNotFoundError，说明依赖安装不完整
) else (
    echo [ OK ] 后端服务运行正常
)

echo.
echo [5/5] 启动 Vue3 前端服务...
echo 前端地址: http://localhost:5173
echo.
echo 检查 npm...
call npm.cmd --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 npm，请先安装 Node.js
    pause
    exit /b 1
)

cd frontend
if not exist "node_modules" (
    echo 首次安装依赖，请稍候...
    call npm.cmd install
)
start "SOAR Frontend" cmd /k "npm.cmd run dev"
cd ..

echo.
echo =====================================
echo [ OK ] 系统启动完成！
echo =====================================
echo.
echo 重要信息：
echo    - 后端服务: http://localhost:8000
echo    - 前端应用: http://localhost:5173
echo    - API 文档: http://localhost:8000/docs
echo    - 连接诊断: http://localhost:8000/api/agent/test-connection
echo.
echo 如果智能助手无法使用，请先访问上面的连接诊断地址
echo 查看哪一步出了问题。
echo.
pause
