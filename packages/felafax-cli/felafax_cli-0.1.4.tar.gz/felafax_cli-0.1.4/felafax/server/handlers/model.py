from ...core.storage.base import StorageProvider
from typing import Dict, List, Optional
from ..models.model import ModelPaths
from ..handlers.base import ListMetadataHandler
from ..handlers.accelerator import AcceleratorHandler
from ..models.model import ModelMetadata
import httpx


class ModelHandler:
    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self.storage = storage_provider
        self.user_id = user_id
        self._metadata_handler = ListMetadataHandler(ModelMetadata, ModelPaths.metadata_path(user_id), "model_id", self.storage)
        self._accelerator_handler = AcceleratorHandler(self.storage, self.user_id)
    

    async def init_chat(self, model_id: str) -> str:
        """Initialize chat by starting the accelerator"""
        if not await self.check_model_exists(model_id):
            raise ValueError(f"Model {model_id} does not exist")
        
        model_path = ModelPaths.full_model_path(self.user_id, model_id)
        accelerator = await self._start_vllm_inference_accelerator(model_path)
        return accelerator.accelerator_id

    async def chat(self, accelerator_id: str, messages: List[Dict]) -> str:
        """Chat with a model using an existing accelerator"""
        ip_address = await self._accelerator_handler.get_ip_address(accelerator_id)
        return await self._vllm_chat(messages, ip_address)

    async def _start_vllm_inference_accelerator(self, model_path: str) -> None:
        """Start inference accelerator with specific config"""
        return await self._accelerator_handler.create_accelerator(
            provider="tpu",
            config={
                "accelerator_type": "v5p",
                "accelerator_core_count": 8,
                "zone": "us-east5-a",
                "attach_disk": True,
                "disk_size_gb": 500
            },
            docker_config={
                "image": "gcr.io/felafax-training/vllm:latest_v3",
                "env": {
                    "GCS_MODEL_PATH": model_path
                }
            },
            tags=["vllm-server"],
            wait_for_ready=True
        )
    
    async def _vllm_chat(self, messages: List[Dict], ip_address: str) -> str:
        """Chat with a model using VLLM"""
        url = f"http://{ip_address}:8000/v1/chat/completions"
        async with httpx.AsyncClient(timeout=300.0) as client:
            # TODO: currently model is always mounted at /mnt/persistent-disk/model
            # in future we should make this configurable
            response = await client.post(url, json={
                "model": "/mnt/persistent-disk/model", 
                "messages": messages
            })
            return response.json()["choices"][0]["message"]["content"]


    async def get_model_info(self, model_id: str) -> Dict:
        """Get model metadata"""
        return await self._metadata_handler.get_by_id(model_id)

    async def update_model_info(self, model_id: str, info: Dict) -> None:
        """Update model metadata"""
        metadata = await self._metadata_handler.get_by_id(model_id)
        metadata.update(info)
        await self._metadata_handler.update(metadata)
        
    async def get_download_url(self, model_id: str) -> str:
        """Get download URL for model weights"""
        return f"/download/{self.user_id}/models/{model_id}/weights"
    
    async def delete_model(self, model_id: str) -> None:
        """Delete a model"""
        await self._metadata_handler.remove(model_id)
        model_path = ModelPaths.model_path(self.user_id, model_id)
        await self.storage.delete_directory(model_path, convert_iterator=True)
        
    async def list_models(self) -> List[ModelMetadata]:
        """List all models"""
        return await self._metadata_handler.list()
    
    async def check_model_exists(self, model_id: str) -> bool:
        """Check if a model exists"""
        return await self._metadata_handler.get_by_id(model_id) is not None

