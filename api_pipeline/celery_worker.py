from celery import Celery
from . import pipeline

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def run_pipeline_task():
    """Celery task to run the pipeline."""
    import asyncio
    asyncio.run(pipeline.run_pipeline())
