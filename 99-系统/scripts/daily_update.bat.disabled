@echo off
setlocal
chcp 65001 >nul

REM ==========================================================
REM  风电行业数据库 —— 每日自动更新（Claude Code 版）
REM  供 Windows 任务计划程序调用，无需 Claude 桌面端开着
REM
REM  前置条件：
REM    1. 已安装 Node.js
REM    2. npm install -g @anthropic-ai/claude-code
REM    3. 在本目录跑过一次 `claude` 完成登录授权
REM    4. 已安装 Python 3（python 命令可用）
REM ==========================================================

set "VAULT=D:\works\2026\亚太区工作\风电行业数据库\风电行业数据库"
set "LOGDIR=%VAULT%\99-系统\日志"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

for /f "tokens=1-3 delims=/- " %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "TODAY=%%a"
set "LOG=%LOGDIR%\%TODAY%.log"

echo ============================================ >> "%LOG%"
echo [%DATE% %TIME%] 开始每日更新 >> "%LOG%"

cd /d "%VAULT%"

REM ---- 第 1 步：让 Claude Code 检索资讯并写入笔记 ----
call claude -p "@99-系统/每日更新指令.md 请严格按该文件执行今天的更新。" ^
  --permission-mode acceptEdits ^
  >> "%LOG%" 2>&1

if errorlevel 1 (
  echo [%DATE% %TIME%] !! Claude Code 执行返回非零退出码 >> "%LOG%"
)

REM ---- 第 2 步：重建静态表格（即便上一步失败也执行，保证表格与笔记一致）----
python "%VAULT%\99-系统\scripts\rebuild_tables.py" "%VAULT%" >> "%LOG%" 2>&1

if errorlevel 1 (
  echo [%DATE% %TIME%] !! 表格重建失败 >> "%LOG%"
  goto :end
)

REM ---- 第 3 步：导出 Excel 快照 ----
python "%VAULT%\99-系统\scripts\export_excel.py" "%VAULT%" "%VAULT%\风电行业数据库_最新.xlsx" >> "%LOG%" 2>&1

if errorlevel 1 echo [%DATE% %TIME%] !! Excel 导出失败 >> "%LOG%"

REM ---- 第 3.5 步：生成本地看板（双击 看板.html 即可离线浏览）----
REM 站上的看板由 GitHub Actions 单独构建，这里生成的只供本机预览。
REM 含 07-战略判断：本地版加 --with-strategy，线上版不加。
python "%VAULT%\99-系统\scripts\build_dashboard.py" "%VAULT%" -o "%VAULT%\看板.html" --with-strategy >> "%LOG%" 2>&1

if errorlevel 1 echo [%DATE% %TIME%] !! 看板生成失败 >> "%LOG%"

echo [%DATE% %TIME%] 完成 >> "%LOG%"

:end
REM ---- 第 4 步：推送到 GitHub，触发站点自动构建 ----
if exist "%VAULT%\.git" (
  git -C "%VAULT%" add -A >> "%LOG%" 2>&1
  git -C "%VAULT%" commit -m "auto: 每日更新 %TODAY%" >> "%LOG%" 2>&1
  git -C "%VAULT%" push origin main >> "%LOG%" 2>&1
  if errorlevel 1 (
    echo [%DATE% %TIME%] !! git push 失败，站点未更新 >> "%LOG%"
  ) else (
    echo [%DATE% %TIME%] 已推送，GitHub Actions 将在数分钟内重建站点 >> "%LOG%"
  )
)

endlocal
