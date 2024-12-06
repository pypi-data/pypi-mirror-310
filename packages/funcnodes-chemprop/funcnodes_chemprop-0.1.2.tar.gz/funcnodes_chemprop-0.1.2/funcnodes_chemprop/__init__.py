import pandas as pd
from typing import List, Tuple, Union
from chemprop import models
from sklearn.preprocessing import StandardScaler

from torch.utils.data import DataLoader
import numpy as np
import funcnodes as fn
from . import functions as f
import copy
import asyncio


@fn.NodeDecorator(
    id="chemprop.make_model",
    name="Make Model",
    description="Create a Chemprop model",
    outputs=[{"name": "model"}],
)
def make_model(scaler: StandardScaler) -> models.MPNN:
    mpnn = f.make_model(scaler)
    return mpnn


class MakeDataNode(fn.Node):
    node_id = "chemprop.make_data"
    node_name = "Make Data"
    description = "Create Chemprop data loaders"

    df = fn.NodeInput(uuid="df", type=pd.DataFrame)
    smiles_column = fn.NodeInput(uuid="smiles_column", type=str)
    target_columns = fn.NodeInput(uuid="target_columns", type=str)
    split = fn.NodeInput(
        uuid="split", type=Tuple[float, float, float], default=(0.8, 0.1, 0.1)
    )

    train_loader = fn.NodeOutput(uuid="train_loader", type=DataLoader)
    val_loader = fn.NodeOutput(uuid="val_loader", type=DataLoader)
    test_loader = fn.NodeOutput(uuid="test_loader", type=DataLoader)
    scaler = fn.NodeOutput(uuid="scaler", type=StandardScaler)

    def __init__(self):
        super().__init__()
        self.get_input("df").on("after_set_value", self._update_columns)

    def _update_columns(self, **kwargs):
        try:
            df = self.get_input("df").value
            smiles_column = self.get_input("smiles_column")
            target_columns = self.get_input("target_columns")
        except KeyError:
            return
        try:
            smiles_column.update_value_options(options=list(df.columns))
            target_columns.update_value_options(options=list(df.columns))
        except Exception:
            smiles_column.update_value_options(options=[])
            target_columns.update_value_options(options=[])

    async def func(self, df, smiles_column, target_columns, split):
        train_loader, val_loader, test_loader, scaler = f.make_data(
            df, smiles_column, target_columns, split
        )

        self.outputs["train_loader"].value = train_loader
        self.outputs["val_loader"].value = val_loader
        self.outputs["test_loader"].value = test_loader
        self.outputs["scaler"].value = scaler


# @fn.NodeDecorator(
#     id="chemprop.train",
#     name="Train",
#     description="Train a Chemprop model",
#     outputs=[{"name": "trained model"}, {"name": "results"}],
#     default_io_options={
#         "model": {"does_trigger": False},
#         "train_loader": {"does_trigger": False},
#         "val_loader": {"does_trigger": False},
#         "test_loader": {"does_trigger": False},
#         "max_epochs": {"does_trigger": False},
#     },
# )
# async def train(
#     model: models.MPNN,
#     train_loader: DataLoader,
#     val_loader: DataLoader,
#     test_loader: DataLoader,
#     max_epochs: int = 20,
# ) -> Tuple[models.MPNN, dict, pd.DataFrame]:
#     model_copy = copy.deepcopy(model)
#     metrics_df = None

#     async for metrics in f.train_in_subprocess(
#         model_copy, train_loader, val_loader, test_loader, max_epochs
#     ):
#         if isinstance(metrics, dict):
#             if metrics_df is None:
#                 metrics_df = pd.DataFrame([metrics])
#             else:
#                 metrics_df = pd.concat([metrics_df, pd.DataFrame([metrics])])
#         print(f"Received metrics: {metrics}")

#     return (*metrics, metrics_df)


class TrainNode(fn.Node):
    node_id = "chemprop.train"
    node_name = "Train"
    description = "Train a Chemprop model"

    model = fn.NodeInput(uuid="model", type=models.MPNN, does_trigger=False)
    train_loader = fn.NodeInput(
        uuid="train_loader", type=DataLoader, does_trigger=False
    )
    val_loader = fn.NodeInput(uuid="val_loader", type=DataLoader, does_trigger=False)
    test_loader = fn.NodeInput(uuid="test_loader", type=DataLoader, does_trigger=False)
    max_epochs = fn.NodeInput(
        uuid="max_epochs", type=int, default=20, does_trigger=False
    )

    trained_model = fn.NodeOutput(uuid="trained_model", type=models.MPNN)
    results = fn.NodeOutput(uuid="results", type=dict)
    metrics = fn.NodeOutput(uuid="metrics", type=pd.DataFrame)

    async def func(self, model, train_loader, val_loader, test_loader, max_epochs):
        model_copy = copy.deepcopy(model)

        metrics_df = None
        collected_metrics = []
        running = True

        async def metrics_publisher():
            last_published = 0
            while running:
                if len(collected_metrics) > last_published:
                    self.outputs["metrics"].value = pd.DataFrame(collected_metrics)
                    last_published = len(collected_metrics)
                await asyncio.sleep(1)

        # def metrics_publisher():
        #     last_published = 0
        #     last_len = 0

        #     while running:
        #         if (
        #             len(collected_metrics) > last_len
        #             and time.time() - last_published > 1
        #         ):
        #             last_published = time.time()
        #             last_len = len(collected_metrics)
        #             self.outputs["metrics"].value = collected_metrics
        #         time.sleep(0.1)

        # publish_thread = threading.Thread(target=metrics_publisher, daemon=True)
        # publish_thread.start()

        publish_task = asyncio.create_task(metrics_publisher())

        async for metrics in f.train_in_subprocess(
            model_copy, train_loader, val_loader, test_loader, max_epochs
        ):
            if isinstance(metrics, dict):
                ep = metrics["epoch"]
                del metrics["epoch"]
                converted_metrics = [
                    {"epoch": ep, "type": k, "value": v} for k, v in metrics.items()
                ]
                collected_metrics.extend(converted_metrics)

        running = False
        await publish_task
        # publish_thread.join()

        trained_model, results = metrics
        self.outputs["trained_model"].value = trained_model
        self.outputs["results"].value = results

        return trained_model, results, metrics_df


@fn.NodeDecorator(
    id="chemprop.predict",
    name="Predict",
    description="Predict using a Chemprop model",
    outputs=[{"name": "preds"}],
)
def predict(model: models.MPNN, smis: Union[str, List[str]]) -> np.ndarray:
    if isinstance(smis, str):
        smis = [smis]
    return f.predict(model, smis)


NODE_SHELF = fn.Shelf(
    name="Chemprop",
    description="Chemprop nodes",
    nodes=[make_model, MakeDataNode, TrainNode, predict],
    subshelves=[],
)
