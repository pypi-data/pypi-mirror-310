from pydantic import ConfigDict
from abc import ABC, abstractmethod
import numpy as np
from fasr.utils.base import ModelScopeMixin, SerializableMixin


class BaseAudioPreprocessor(SerializableMixin, ABC):
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True
    )

    @abstractmethod
    def process_waveform(self, waveform: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class MSAudioPreprocessor(ModelScopeMixin, BaseAudioPreprocessor):
    @classmethod
    def from_checkpoint(cls, checkpoint_dir: str, **kwargs):
        raise NotImplementedError

    def download_checkpoint(self, checkpoint_dir: str, **kwargs):
        raise NotImplementedError
