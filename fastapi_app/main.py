from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI()

@app.post("/process/{satellite_name}")
async def process_satellite(satellite_name: str):
    try:
        result = subprocess.run(
            ["python", "data_downloader/uploading_files.py", satellite_name],
            check=True,
            capture_output=True,
            text=True
        )
        return {"status": "success", "message": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error processing satellite data: {e.stderr}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

