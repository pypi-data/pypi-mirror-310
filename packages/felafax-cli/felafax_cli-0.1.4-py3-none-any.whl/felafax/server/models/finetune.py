from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class FinetuneStatus(BaseModel):
    tune_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    progress: Optional[float] = None

class FinetuneMetadata(BaseModel):
    """Tune metadata schema"""
    tune_id: str
    model_id: Optional[str] = None
    dataset_id: str
    base_model: str
    status: str
    accelerator_id: str
    created_at: datetime
    updated_at: datetime

class FineTuneRequest(BaseModel):
    model_name: str
    dataset_id: str
    config: dict

class FineTuneStoragePaths:
    """Fine-tune storage path generator"""
    
    @staticmethod
    def base_path(user_id: str) -> str:
        return f"users/{user_id}"
    
    @staticmethod
    def tune_path(user_id: str, tune_id: str) -> str:
        return f"{FineTuneStoragePaths.base_path(user_id)}/tune_jobs/{tune_id}"
    
    @staticmethod
    def config_path(user_id: str, tune_id: str) -> str:
        return f"{FineTuneStoragePaths.tune_path(user_id, tune_id)}/config.yml"
    
    @staticmethod
    def status_path(user_id: str, tune_id: str) -> str:
        return f"{FineTuneStoragePaths.tune_path(user_id, tune_id)}/status.json"

    @staticmethod
    def checkpoints_path(user_id: str, tune_id: str) -> str:
        return f"{FineTuneStoragePaths.tune_path(user_id, tune_id)}/checkpoints"

    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/finetunes.json"
    

# Configuration for fine-tuning

# class LoraConfig(BaseModel):
#     enabled: bool
#     r: int
#     alpha: int
#     dropout: float

# class HyperParameters(BaseModel):
#     learning_rate: float
#     batch_size: int
#     n_epochs: int
#     warmup_ratio: float

# class FinetuneConfig(BaseModel):
#     hyperparameters: HyperParameters
#     lora: LoraConfig
    

# class ExecutionConfig(BaseModel):
#     """Execution configuration for fine-tuning"""
#     # Use FinetuneConfig path
#     config_path: str
#     # Status path for job
#     status_path: str
#     # Log path to dump all stdout/stderr
#     log_path: str
#     # path on device for all exeuction storage
#     execution_dir: str

#     base_model_name: str
#     dataset_gcs_path: str
#     dataset_local_path: str
#     output_local_path: str
#     output_gcs_path: str
