from fastapi import FastAPI
from .celery_worker import run_pipeline_task

app = FastAPI()

@app.post("/trigger-pipeline")
async def trigger_pipeline():
    """Triggers the API pipeline."""
    run_pipeline_task.delay()
    return {"message": "Pipeline task triggered successfully"}
