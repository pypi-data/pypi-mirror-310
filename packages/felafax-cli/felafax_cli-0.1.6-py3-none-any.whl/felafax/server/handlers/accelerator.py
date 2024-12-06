from typing import Dict, Any, Optional, List
import uuid
import asyncio
from datetime import datetime
from ...config import Config
from ...core.accelerators.base import AcceleratorProvider, AcceleratorStatus
from ...core.accelerators.tpu import TPUProvider
from ...core.storage.base import StorageProvider
from ..models.accelerator import AcceleratorMetadata, AcceleratorStoragePaths
from ..handlers.base import ListMetadataHandler
from ..common import generate_vm_name
from dataclasses import dataclass

@dataclass
class AcceleratorSpec:
    provider: str
    config: Dict[str, Any]
    docker_config: Optional[Dict[str, Any]] = None

class AcceleratorHandler:
    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self.storage_provider = storage_provider
        self.user_id = user_id
        self._provider_map = {
            "tpu": TPUProvider
        }
        self._metadata_handler = ListMetadataHandler(
            AcceleratorMetadata, 
            AcceleratorStoragePaths.metadata_path(self.user_id), 
            "accelerator_id", 
            self.storage_provider
        )

    async def create_accelerator(
        self,
        provider: str,
        config: Dict[str, Any],
        docker_config: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        wait_for_ready: bool = False
    ) -> AcceleratorMetadata:
        """Create and start a new accelerator
        
        Args:
            provider: Provider type (e.g., 'tpu')
            config: Hardware configuration
            docker_config: Optional docker settings (image, env vars)
            tags: Optional list of tags
        """
        # Merge with base config
        full_config = {
            "project_id": Config.GCS_PROJECT_ID,
            **config
        }

        # Add docker configuration if provided
        if docker_config:
            full_config["docker_image"] = docker_config.get("image")
            full_config["docker_env"] = docker_config.get("env", {})
            full_config["tags"] = tags or []

        # Generate IDs
        accelerator_id = f"acc_{uuid.uuid4().hex[:8]}"
        full_config["name"] = generate_vm_name()

        # Create provider instance
        provider_class = self._provider_map.get(provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider}")
        
        provider_instance = provider_class()
        await provider_instance.initialize(full_config)
        
        # Create metadata
        current_time = datetime.utcnow()
        metadata = AcceleratorMetadata(
            accelerator_id=accelerator_id,
            name=full_config["name"],
            provider=provider,
            created_at=current_time,
            updated_at=current_time,
            status=AcceleratorStatus.PROVISIONING,
            config=full_config,
            docker_config=docker_config,
            tags=tags or []
        )

        # Save catalog entry
        await self._metadata_handler.add(metadata)

        if wait_for_ready:
            await provider_instance.start()
        else:
            # Start the accelerator asynchronously
            asyncio.create_task(provider_instance.start())

        return metadata

    async def stop_accelerator(self, accelerator_id: str) -> None:
        """Stop and cleanup an accelerator"""
        # Get accelerator metadata
        metadata = await self._metadata_handler.get_by_id(accelerator_id)
        if not metadata:
            raise ValueError(f"Accelerator {accelerator_id} not found")
        
        # Initialize provider
        provider_class = self._provider_map.get(metadata.provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {metadata.provider}")
            
        provider = provider_class()
        await provider.initialize(metadata.config)

        # Stop the accelerator asynchronously
        asyncio.create_task(provider.stop())

        # Update metadata
        metadata.status = AcceleratorStatus.TERMINATED
        metadata.updated_at = datetime.utcnow()
        await self._metadata_handler.update(metadata)
    
    async def get_ip_address(self, accelerator_id: str) -> str:
        """Get the IP address of an accelerator"""
        metadata = await self._metadata_handler.get_by_id(accelerator_id)
        if metadata.ip_address is None:
            # let's use the provider to get the IP address
            provider_class = self._provider_map.get(metadata.provider)
            if not provider_class:
                raise ValueError(f"Unsupported provider: {metadata.provider}")
            
            provider = provider_class()
            await provider.initialize(metadata.config)
            metadata.ip_address = await provider.get_ip_address()
            await self._metadata_handler.update(metadata)

        return metadata.ip_address

