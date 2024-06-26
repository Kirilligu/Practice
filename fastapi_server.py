import os
import subprocess
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

running_processes = {}

@app.post("/start/{receiver_name}")
async def start_receiver(receiver_name: str):
    try:
        if receiver_name in running_processes:
            return {"status": "already running", "receiver": receiver_name}
        
        process = subprocess.Popen(["python3", "receiver_service.py", receiver_name])
        running_processes[receiver_name] = process
        return {"status": "started", "receiver": receiver_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/receivers")
async def list_receivers():
    try:
        receiver_dirs = os.listdir("rnx_files")
        return {"receivers": receiver_dirs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/running")
async def list_running_receivers():
    running_receiver_names = list(running_processes.keys())
    return {"running_receivers": running_receiver_names}

@app.post("/stop/{receiver_name}")
async def stop_receiver(receiver_name: str):
    try:
        if receiver_name not in running_processes:
            return {"status": "not running", "receiver": receiver_name}

        process = running_processes.pop(receiver_name)
        process.terminate()
        return {"status": "stopped", "receiver": receiver_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
