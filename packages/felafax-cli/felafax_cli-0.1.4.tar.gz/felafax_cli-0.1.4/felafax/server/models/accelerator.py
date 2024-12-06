from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from ...core.accelerators.base import AcceleratorStatus


class AcceleratorMetadata(BaseModel):
    """Accelerator metadata schema"""

    accelerator_id: str
    name: str
    provider: str
    created_at: datetime
    updated_at: datetime
    ip_address: Optional[str] = None
    status: AcceleratorStatus
    config: Optional[Dict[str, Any]] = {}
    docker_config: Optional[Dict[str, Any]] = {}
    tags: List[str] = []

    class Config:
        arbitrary_types_allowed = True


class AcceleratorCommandResult(BaseModel):
    """Command execution result schema"""

    returncode: int
    stdout: str
    stderr: str


class AcceleratorStoragePaths:
    """Accelerator storage path generator"""

    @staticmethod
    def base_path(user_id: str) -> str:
        return f"users/{user_id}/accelerators"

    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/accelerators.json"

