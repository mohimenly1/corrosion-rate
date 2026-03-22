#!/usr/bin/env python3
"""Train the Arrhenius power-law corrosion model and print a compact summary."""

from services.model_trainer import CorrosionModelTrainer


def main():
    model = CorrosionModelTrainer.train_from_csv()
    params = model["parameters"]
    metrics = model["metrics"]["test"]

    print("Model training completed")
    print(f"Fit method: {model['fit_method']}")
    print(
        "Parameters: "
        f"A={params['A']:.6f}, "
        f"b={params['b']:.6f}, "
        f"K={params['K']:.6f}, "
        f"c={params['c']:.6f}"
    )
    print(
        "Test metrics: "
        f"R2={metrics['r2']:.4f}, "
        f"RMSE={metrics['rmse']:.4f}, "
        f"MAE={metrics['mae']:.4f}"
    )


if __name__ == "__main__":
    main()
