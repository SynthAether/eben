""" Python script to train EBEN model """

import torch
from pytorch_lightning import LightningDataModule, LightningModule, Trainer
from src.discriminator import DiscriminatorEBENMultiScales
from src.eben import EBEN
from src.generator import GeneratorEBEN
from src.librispeech_datamodule import CustomLibriSpeechDM


def train():
    """actual training function"""

    # Instantiate datamodule
    datamodule: LightningDataModule = CustomLibriSpeechDM(
        path_to_dataset="./mls_french",
        sr_standard=16000,
        bs_train=16,
        len_seconds_train=2,
        num_workers=4,
    )

    # Instantiate EBEN
    generator: torch.nn.Module = GeneratorEBEN(
        m=4, # total number of bands, (= decimation factor of PQMF)
        n=32,  # PQMF kernel size
        p=1   # number of informative bands fed to generator
    )  

    discriminator: torch.nn.Module = DiscriminatorEBENMultiScales(
        q=3  # number of bands refined by PQMF discriminators
    )  

    eben: LightningModule = EBEN(
        generator=generator, discriminator=discriminator, lr=0.0003, betas=(0.5, 0.9)
    )

    trainer: Trainer = Trainer(
        gpus=1,
        max_epochs=13,
        enable_checkpointing=False,
        logger=False,
        limit_val_batches=0,
    )

    # Fit
    trainer.fit(model=eben, datamodule=datamodule)


if __name__ == "__main__":
    train()
