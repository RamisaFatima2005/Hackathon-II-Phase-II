@echo off
.\venv312\Scripts\uvicorn.exe src.main:app --host 0.0.0.0 --port 8000 --reload > uvicorn.log 2> uvicorn.err
