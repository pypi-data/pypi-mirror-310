from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from openmapflow.engineer import process_test_file

try:
    import torch

    TORCH_INSTALLED = True
except ImportError:
    TORCH_INSTALLED = False


class Inference:
    """
    Class for running inference on a single tif file using an sklearn or
    pytorch model (including jit).
    """

    def __init__(
        self,
        model,
        normalizing_dict: Optional[Dict[str, np.ndarray]],
        device=None,
        batch_size: int = 64,
    ):
        self.model = model
        self.device = device
        self.normalizing_dict = normalizing_dict
        self.batch_size: int = batch_size

        if hasattr(self.model, "predict_proba"):
            self.model_type = "sklearn"
        elif TORCH_INSTALLED:
            self.model_type = "pytorch"
        else:
            raise ModuleNotFoundError(
                "Using PyTorch model but PyTorch is not installed. Please pip install torch"
            )

    @staticmethod
    def _combine_predictions(
        flat_lat: np.ndarray, flat_lon: np.ndarray, batch_predictions: List[np.ndarray]
    ) -> pd.DataFrame:
        all_preds = np.concatenate(batch_predictions, axis=0)
        if len(all_preds.shape) == 1:
            all_preds = np.expand_dims(all_preds, axis=-1)

        data_dict: Dict[str, np.ndarray] = {"lat": flat_lat, "lon": flat_lon}
        for i in range(all_preds.shape[1]):
            prediction_label = f"prediction_{i}"
            data_dict[prediction_label] = all_preds[:, i]
        return pd.DataFrame(data=data_dict).set_index(["lat", "lon"])

    def _on_single_batch(self, batch_x_np: np.ndarray) -> np.ndarray:
        if self.model_type == "sklearn":
            flattened_batch = batch_x_np.reshape(batch_x_np.shape[0], -1)
            return self.model.predict_proba(flattened_batch)[:, 1]
        elif self.model_type == "pytorch":
            batch_x = torch.from_numpy(batch_x_np).float()
            if self.device is not None:
                batch_x = batch_x.to(self.device)
            with torch.no_grad():
                preds = self.model(batch_x)
            return preds.cpu().numpy()
        else:
            # This code should never be reached
            raise ValueError(f"Unknown model type {self.model_type}")

    def run(
        self,
        local_path: Path,
        dest_path: Optional[Path] = None,
    ) -> pd.DataFrame:
        """Runs inference on a single tif file."""
        x_np, flat_lat, flat_lon = process_test_file(local_path)

        if self.normalizing_dict is not None:
            x_np = (x_np - self.normalizing_dict["mean"]) / self.normalizing_dict["std"]

        batches = [
            x_np[i : i + self.batch_size]  # noqa: E203
            for i in range(0, x_np.shape[0], self.batch_size)
        ]
        batch_predictions = [self._on_single_batch(b) for b in batches]
        combined_pred = self._combine_predictions(flat_lat, flat_lon, batch_predictions)
        if dest_path is not None:
            combined_pred.to_xarray().to_netcdf(dest_path)
        return combined_pred
