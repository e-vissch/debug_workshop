from datetime import datetime
from pathlib import Path

import typer
import torch

from ser.train import train as run_train
from ser.constants import RESULTS_DIR
from ser.data import train_dataloader, val_dataloader, test_dataloader
from ser.infer import infer as run_infer
from ser.params import Params, save_params, load_params
from ser.transforms import transforms, normalize, flip

main = typer.Typer()


@main.command()
def train(
    name: str = typer.Option(
        ..., "-n", "--name", help="Name of experiment to save under."
    ),
    epochs: int = typer.Option(
        5, "-e", "--epochs", help="Number of epochs to run for."
    ),
    batch_size: int = typer.Option(
        1000, "-b", "--batch-size", help="Batch size for dataloader."
    ),
    learning_rate: float = typer.Option(
        0.01, "-l", "--learning-rate", help="Learning rate for the model."
    ),
):
    """Run the training algorithm."""


    # wraps the passed in parameters
    params = Params(name, epochs, batch_size, learning_rate)

    # setup device to run on
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # setup run
    fmt = "%Y-%m-%dT%H-%M"
    timestamp = datetime.strftime(datetime.utcnow(), fmt)
    run_path = RESULTS_DIR / name / timestamp
    run_path.mkdir(parents=True, exist_ok=True)

    # Save parameters for the run
    save_params(run_path, params)

    # Train!
    run_train(
        run_path,
        params,
        train_dataloader(params.batch_size, transforms(normalize)),
        val_dataloader(params.batch_size, transforms(normalize)),
        device,
    )


@main.command()
def infer(
    run_path: Path = typer.Option(
        ..., "-p", "--path", help="Path to run from which you want to infer."
    ),
    label: int = typer.Option(
        6, "-l", "--label", help="Label of image to show to the model"
    ),
    include_flip: bool = typer.Option(
        False, "-f", "--flip", help="Include flip transform"
    ),
):
    """Run the inference code"""
    params = load_params(run_path)
    model = torch.load(run_path / "model.pt")
    model.to("cpu")
    image = _select_test_image(label, include_flip)
    run_infer(params, model, image, label, include_flip)


def _select_test_image(label, include_flip):
    ts = [normalize]
    if include_flip:
        ts.append(flip)
    dataloader = test_dataloader(1, transforms(*ts))
    images, labels = next(iter(dataloader))
    while labels[0].item() != label:
        images, labels = next(iter(dataloader))
    return images
