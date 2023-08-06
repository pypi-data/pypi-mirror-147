from typing import Any, Dict

import torch
import torch.nn.functional as F
from fairseq.checkpoint_utils import load_model_ensemble_and_task
from torch import nn
from torch.optim import SGD, Adam, RMSprop

from ._base import SimpleClassificationModel


class Model(SimpleClassificationModel):
    def __init__(
        self,
        ckpt: str,
        n_classes: int,
        n_features: int = 1,
        opt: str = "sgd",
        lr: float = 0.1,
        opt_params: Dict[str, Any] = {},
    ) -> None:
        super().__init__(n_classes=n_classes, n_features=1)

        [model], args, task = load_model_ensemble_and_task([ckpt])
        self.wav2vec = model
        self.w2v_args = args
        # self.w2v_task = task

        # Needed for multi-GPU training because of
        # https://github.com/pytorch/fairseq/issues/3482
        self.w2v_cfg = dict(task.cfg)
        if "text_compression_level" in self.w2v_cfg:
            self.w2v_cfg["text_compression_level"] = str(
                self.w2v_cfg["text_compression_level"]
            )

        self.lr = lr
        self.opt = opt
        self.opt_params = dict(opt_params)
        self.save_hyperparameters("ckpt", "lr", "opt", "opt_params")

        self.final = nn.Linear(512, n_classes)

    def forward(self, x):
        x = x.squeeze(-1)
        x = self.wav2vec.feature_extractor(x)
        if self.wav2vec.vector_quantizer is not None:
            x, _ = self.wav2vec.vector_quantizer.forward_idx(x)
        x = x.mean(-1)
        x = self.final(x)
        return x

    def configure_optimizers(self):
        opt_cls = {"adam": Adam, "rmsprop": RMSprop, "sgd": SGD}[self.opt]
        return opt_cls(self.parameters(), lr=self.lr, **self.opt_params)

    def preprocess_input(self, x: torch.Tensor) -> torch.Tensor:
        if self.w2v_cfg["normalize"]:
            with torch.no_grad():
                x = F.layer_norm(x, x.shape)
        return x
