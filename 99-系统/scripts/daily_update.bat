@echo off
setlocal
chcp 65001 >nul

REM ==========================================================
REM  风电行业数据库 —— 每日自动更新（方案 B：Claude Code + 任务计划）
REM
REM  ⛔ 本脚本已于 2026-08-02 停用。
REM
REM  原因：每日更新已改由 Claude 桌面端（Cowork）的定时任务
REM        `wind-industry-db-daily` 全程执行，含检索、写笔记、
REM        重建表格、导出 Excel、生成看板、git 推送。
REM        两套流程同时跑会争抢 .git 锁文件，导致 commit/push 失败。
REM
REM  原脚本内容完整保留在同目录的 daily_update.bat.disabled，
REM  需要恢复时把它复制回 daily_update.bat 即可。
REM
REM  ⚠ 恢复前必须先停掉 Cowork 侧的定时任务，二者只能选一套。
REM ==========================================================

echo.
echo ============================================================
echo  daily_update.bat 已停用（2026-08-02）
echo ============================================================
echo.
echo  每日更新现由 Claude 桌面端定时任务 wind-industry-db-daily 执行，
echo  涵盖：检索 - 写笔记 - 重建表格 - 导出 Excel - 生成看板 - git 推送。
echo.
echo  本脚本若与之同时运行，会争抢 .git 锁文件导致推送失败。
echo.
echo  需要恢复方案 B 时：
echo    1. 先在 Claude 桌面端 Scheduled 面板停用 wind-industry-db-daily
echo    2. copy daily_update.bat.disabled daily_update.bat
echo.
echo  另需删除已注册的计划任务，否则它会继续调用本脚本：
echo    schtasks /Delete /TN "风电行业数据库每日更新" /F
echo.
echo ============================================================
echo.

REM 不执行任何更新动作，直接以非零码退出，
REM 使残留的计划任务在历史记录里留下明显的失败标记，便于发现未清理。
endlocal
exit /b 1
