import os
import requests

from pydantic import BaseModel, Field
from fooocusapi.utils.logger import logger

class RunpodStatus(BaseModel):
    pod_id: str = Field(..., title="Pod ID")
    pod_ip: str = Field(..., title="Pod IP")
    pod_url: str = Field(..., title="Pod URL")


async def send_runpod_details():
    try:
        headers = {"Authorization": f"Bearer {os.getenv('API_AUTH_TOKEN', '')}"}
        runpod_status = RunpodStatus(
            pod_id=os.getenv("RUNPOD_POD_ID"),
            pod_ip=os.getenv("RUNPOD_PUBLIC_IP"),
            pod_url=os.getenv("RUNPOD_PUBLIC_URL"),
        )

        requests.post(os.getenv("RUNPOD_STATUS_URL"), headers=headers, json=runpod_status.model_dump())
    except Exception as e:
        logger.std_error(f"Failed to send runpod details to remote server: {e}")


async def startup_event():
    """Trigger request on FastAPI startup event"""
    await send_runpod_details()
