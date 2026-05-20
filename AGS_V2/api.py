from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from sqlmodel import Session, select
import asyncio
from core.db import engine, DAGTask
from typing import AsyncGenerator

app = FastAPI(title="AGS Observability API")

async def task_stream_generator() -> AsyncGenerator[dict, None]:
    """Yields DAG task state changes out to the NextJS frontend."""
    last_checksum = None
    
    while True:
        with Session(engine) as session:
            tasks = session.exec(select(DAGTask)).all()
            
            # Simple string hash logic to only push data when state changes
            current_state = str([(t.id, t.status) for t in tasks])
            if current_state != last_checksum:
                last_checksum = current_state
                
                payload = [
                    {
                        "id": str(t.id),
                        "description": t.description,
                        "status": t.status,
                        "persona": t.assigned_persona
                    } for t in tasks
                ]
                
                yield {
                    "event": "dag_update",
                    "data": payload
                }
                
        await asyncio.sleep(2)

@app.get("/stream")
async def sse_endpoint(request: Request):
    """Next.js Dashboard connects here for Server-Sent Events."""
    return EventSourceResponse(task_stream_generator())

if __name__ == "__main__":
    import uvicorn
    # Launch on 8000 for local proxy
    uvicorn.run(app, host="0.0.0.0", port=8000)
