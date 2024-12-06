import pandas as pd
from typing import List, Tuple, Union
from chemprop import data, featurizers, models, nn
from lightning import pytorch as pl
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import DataLoader
import numpy as np
import multiprocessing

import asyncio


def make_model(scaler: StandardScaler) -> models.MPNN:
    mp = nn.BondMessagePassing()

    agg = nn.MeanAggregation()

    output_transform = nn.UnscaleTransform.from_standard_scaler(scaler)
    ffn = nn.RegressionFFN(output_transform=output_transform)
    batch_norm = True
    metric_list = [
        nn.metrics.RMSEMetric(),
        nn.metrics.MAEMetric(),
    ]  # Only the first metric is used for training and early stopping
    mpnn = models.MPNN(mp, agg, ffn, batch_norm, metric_list)
    return mpnn


def make_data(
    df: pd.DataFrame,
    smiles_column: str,
    target_columns: Union[str, List[str]],
    split=(0.8, 0.1, 0.1),
) -> Tuple[
    DataLoader,
    DataLoader,
    DataLoader,
    StandardScaler,
]:
    num_workers = 0
    if isinstance(target_columns, str):
        target_columns = [target_columns]
    smis = df.loc[:, smiles_column].values
    ys = df.loc[:, target_columns].values
    all_data = [data.MoleculeDatapoint.from_smi(smi, y) for smi, y in zip(smis, ys)]
    mols = [
        d.mol for d in all_data
    ]  # RDkit Mol objects are use for structure based splits

    train_indices, val_indices, test_indices = data.make_split_indices(
        mols, "random", split
    )
    train_data, val_data, test_data = data.split_data_by_indices(
        all_data, train_indices, val_indices, test_indices
    )

    featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
    train_dset = data.MoleculeDataset(train_data, featurizer)
    scaler = train_dset.normalize_targets()

    val_dset = data.MoleculeDataset(val_data, featurizer)
    val_dset.normalize_targets(scaler)

    test_dset = data.MoleculeDataset(test_data, featurizer)

    train_loader = data.build_dataloader(train_dset, num_workers=num_workers)

    val_loader = data.build_dataloader(val_dset, num_workers=num_workers, shuffle=False)
    test_loader = data.build_dataloader(
        test_dset, num_workers=num_workers, shuffle=False
    )

    return train_loader, val_loader, test_loader, scaler


class MetricCallback(pl.Callback):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def log_metrics2queue(self, trainer):
        metrics = trainer.callback_metrics
        # convert tensors to scalars
        metrics = {k: v.item() for k, v in metrics.items()}
        metrics["epoch"] = trainer.current_epoch
        self.queue.put(metrics)

    def on_train_epoch_end(
        self,
        trainer,
        pl_module,
    ):
        self.log_metrics2queue(trainer)

    def on_test_epoch_end(
        self, trainer: pl.Trainer, pl_module: pl.LightningModule
    ) -> None:
        self.log_metrics2queue(trainer)


def train(
    model: models.MPNN,
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: DataLoader,
    max_epochs=20,
    queue=None,
) -> Tuple[models.MPNN, dict]:
    callbacks = [MetricCallback(queue)] if queue else []
    trainer = pl.Trainer(
        logger=False,
        enable_checkpointing=True,  # Use `True` if you want to save model checkpoints.
        # The checkpoints will be saved in the `checkpoints` folder.
        enable_progress_bar=True,
        accelerator="auto",
        devices=1,
        max_epochs=max_epochs,  # number of epochs to train for
        callbacks=callbacks,
    )

    trainer.fit(model, train_loader, val_loader)

    results = trainer.test(model, test_loader)
    return model, results


def _train_in_subprocess_entry(
    model,
    train_loader,
    val_loader,
    test_loader,
    max_epochs,
    return_dict,
    queue: multiprocessing.Queue,
):
    model, results = train(
        model,
        train_loader,
        val_loader,
        test_loader,
        max_epochs,
        queue,
    )
    return_dict["model"] = model
    return_dict["results"] = results


async def train_in_subprocess(
    model: models.MPNN,
    train_loader: DataLoader,
    val_loader: DataLoader,
    test_loader: DataLoader,
    max_epochs=20,
) -> Tuple[models.MPNN, dict]:
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    queue = manager.Queue()

    p = multiprocessing.Process(
        target=_train_in_subprocess_entry,
        args=(
            model,
            train_loader,
            val_loader,
            test_loader,
            max_epochs,
            return_dict,
            queue,
        ),
    )
    p.start()

    async def metric_generator(queue):
        while p.is_alive():
            try:
                metrics = queue.get_nowait()
                yield metrics
            except Exception:
                await asyncio.sleep(0.1)

    metrics_generator = metric_generator(queue)
    async for metrics in metrics_generator:
        yield metrics
    p.join()
    yield return_dict["model"], return_dict["results"]


def predict(model: models.MPNN, smis: List[str]) -> np.ndarray:
    test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in smis]
    featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
    test_dset = data.MoleculeDataset(test_data, featurizer=featurizer)
    test_loader = data.build_dataloader(test_dset, shuffle=False)
    with torch.inference_mode():
        trainer = pl.Trainer(
            logger=None, enable_progress_bar=True, accelerator="cpu", devices=1
        )
        test_preds = trainer.predict(model, test_loader)
    test_preds = np.concatenate(test_preds, axis=0)
    return test_preds
