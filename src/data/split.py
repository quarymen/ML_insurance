from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def load_config(config_path: str | Path = "configs/split.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def split_dataset(
    df: pd.DataFrame,
    target_column: str,
    test_size: int,
    val_fraction: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    if not isinstance(test_size, int) or test_size <= 0:
        raise ValueError("test_size должен быть положительным целым числом")
    if not 0 < val_fraction < 1:
        raise ValueError("val_fraction должен быть в интервале (0, 1)")
    if test_size >= len(df):
        raise ValueError(
            f"test_size={test_size} больше или равен размеру датасета ({len(df)})"
        )
    if target_column not in df.columns:
        raise KeyError(f"Колонка '{target_column}' не найдена в датафрейме")

    test = df.iloc[-test_size:].copy()
    remaining = df.iloc[:-test_size].copy()

    stratify = remaining[target_column] if remaining[target_column].nunique() > 1 else None
    train, val = train_test_split(
        remaining,
        test_size=val_fraction,
        random_state=seed,
        stratify=stratify,
        shuffle=True,
    )

    logger.info(
        "Разбиение готово: train=%d, val=%d, test=%d (всего %d)",
        len(train), len(val), len(test), len(df),
    )
    return train, val, test


def save_splits(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    output_dir: str | Path,
) -> None:

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train.index.to_series().to_csv(output_dir / "train_idx.csv", index=False, header=["idx"])
    val.index.to_series().to_csv(output_dir / "val_idx.csv", index=False, header=["idx"])
    test.index.to_series().to_csv(output_dir / "test_idx.csv", index=False, header=["idx"])

    train.to_csv(output_dir / "train.csv", index=False)
    val.to_csv(output_dir / "val.csv", index=False)
    test.to_csv(output_dir / "test.csv", index=False)

    logger.info("Разбиения сохранены в %s", output_dir)


def main(config_path: str | Path = "configs/split.yaml") -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(config_path)

    df = pd.read_csv(cfg["data_path"])
    logger.info("Загружено %d строк из %s", len(df), cfg["data_path"])

    train, val, test = split_dataset(
        df=df,
        target_column=cfg["target_column"],
        test_size=int(cfg["test_size"]),
        val_fraction=float(cfg["val_fraction"]),
        seed=int(cfg["seed"]),
    )
    save_splits(train, val, test, cfg["output_dir"])


if __name__ == "__main__":
    main()