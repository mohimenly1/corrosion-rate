import json
import math
import os
from typing import Dict, Tuple

import numpy as np
import pandas as pd


class CorrosionModelTrainer:
    """Train and persist a data-driven Arrhenius power-law corrosion model."""

    DATASET_COLUMNS = {
        "chloride": "NaCl (wt%)",
        "temperature_c": "Temperature (°C)",
        "ph": "pH",
        "corrosion_rate": "Estimated Corrosion Rate (mm/yr)",
    }

    @staticmethod
    def _project_root() -> str:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    @classmethod
    def default_dataset_path(cls) -> str:
        return os.path.join(
            cls._project_root(), "NaCl_50samples_corrosion_table_with_sources.csv"
        )

    @classmethod
    def default_model_path(cls) -> str:
        return os.path.join(
            cls._project_root(), "backend", "model_data", "arrhenius_power_law_model.json"
        )

    @classmethod
    def train_from_csv(
        cls,
        csv_path: str | None = None,
        model_output_path: str | None = None,
        test_ratio: float = 0.4,
        random_seed: int = 42,
    ) -> Dict:
        """Train the model from CSV and save learned parameters."""
        csv_path = csv_path or cls.default_dataset_path()
        model_output_path = model_output_path or cls.default_model_path()

        df = cls._load_training_dataframe(csv_path)
        model_data = cls._fit_model(df, test_ratio=test_ratio, random_seed=random_seed)
        model_data["training_data"] = {
            "csv_path": csv_path,
            "rows_used": int(len(df)),
        }

        os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
        with open(model_output_path, "w", encoding="utf-8") as file:
            json.dump(model_data, file, indent=2)

        return model_data

    @classmethod
    def _load_training_dataframe(cls, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        required_columns = list(cls.DATASET_COLUMNS.values())
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in training CSV: {missing_columns}")

        cleaned = df[required_columns].copy()
        cleaned = cleaned.apply(pd.to_numeric, errors="coerce")
        cleaned = cleaned.dropna()

        # Log-domain model requires strictly positive chloride and corrosion rate.
        cleaned = cleaned[
            (cleaned[cls.DATASET_COLUMNS["chloride"]] > 0)
            & (cleaned[cls.DATASET_COLUMNS["corrosion_rate"]] > 0)
        ].reset_index(drop=True)

        if len(cleaned) < 10:
            raise ValueError("Training dataset is too small after cleaning.")

        return cleaned

    @classmethod
    def _fit_model(
        cls,
        df: pd.DataFrame,
        test_ratio: float,
        random_seed: int,
    ) -> Dict:
        chloride = df[cls.DATASET_COLUMNS["chloride"]].to_numpy(dtype=float)
        temperature_c = df[cls.DATASET_COLUMNS["temperature_c"]].to_numpy(dtype=float)
        temperature_k = temperature_c + 273.15
        ph = df[cls.DATASET_COLUMNS["ph"]].to_numpy(dtype=float)
        corrosion_rate = df[cls.DATASET_COLUMNS["corrosion_rate"]].to_numpy(dtype=float)

        train_idx, test_idx = cls._split_indices(len(df), test_ratio, random_seed)

        linear_params = cls._fit_linearized_parameters(
            chloride[train_idx],
            temperature_k[train_idx],
            ph[train_idx],
            corrosion_rate[train_idx],
        )
        linear_train_predictions = cls.predict(
            chloride[train_idx], temperature_k[train_idx], ph[train_idx], linear_params
        )
        linear_test_predictions = cls.predict(
            chloride[test_idx], temperature_k[test_idx], ph[test_idx], linear_params
        )
        linear_all_predictions = cls.predict(chloride, temperature_k, ph, linear_params)
        linear_metrics = {
            "train": cls._build_metrics(corrosion_rate[train_idx], linear_train_predictions),
            "test": cls._build_metrics(corrosion_rate[test_idx], linear_test_predictions),
            "all_data": cls._build_metrics(corrosion_rate, linear_all_predictions),
        }

        fitted_params, fit_method = cls._maybe_refine_nonlinear_parameters(
            linear_params,
            chloride[train_idx],
            temperature_k[train_idx],
            ph[train_idx],
            corrosion_rate[train_idx],
        )

        train_predictions = cls.predict(
            chloride[train_idx], temperature_k[train_idx], ph[train_idx], fitted_params
        )
        test_predictions = cls.predict(
            chloride[test_idx], temperature_k[test_idx], ph[test_idx], fitted_params
        )
        all_predictions = cls.predict(chloride, temperature_k, ph, fitted_params)

        nonlinear_metrics = {
            "train": cls._build_metrics(corrosion_rate[train_idx], train_predictions),
            "test": cls._build_metrics(corrosion_rate[test_idx], test_predictions),
            "all_data": cls._build_metrics(corrosion_rate, all_predictions),
        }

        selected_key = "nonlinear"
        selected_params = fitted_params
        selected_fit_method = fit_method
        selected_metrics = nonlinear_metrics

        if nonlinear_metrics["test"]["rmse"] > linear_metrics["test"]["rmse"]:
            selected_key = "linearized"
            selected_params = linear_params
            selected_fit_method = "linearized_ols"
            selected_metrics = linear_metrics

        candidate_models = {
            "linearized": {
                "fit_method": "linearized_ols",
                "parameters": linear_params,
                "metrics": linear_metrics,
            },
            "nonlinear": {
                "fit_method": fit_method,
                "parameters": fitted_params,
                "metrics": nonlinear_metrics,
            },
        }

        return {
            "model_name": "Arrhenius Power Law with Exponential pH",
            "equation": "CR = A * [Cl-]^b * exp(-K / Tk) * exp(c * pH)",
            "fit_method": selected_fit_method,
            "random_seed": random_seed,
            "train_size": int(len(train_idx)),
            "test_size": int(len(test_idx)),
            "parameters": selected_params,
            "initial_linearized_parameters": linear_params,
            "linearized_regression_summary": cls._build_linearized_summary(
                chloride[train_idx],
                temperature_k[train_idx],
                ph[train_idx],
                corrosion_rate[train_idx],
            ),
            "metrics": selected_metrics,
            "candidate_models": candidate_models,
            "selected_model_key": selected_key,
            "model_selection_reason": (
                "Selected the model with the lower test RMSE on the unseen split."
            ),
            "outlier_handling": (
                "High-corrosion observations such as aggressive-condition samples "
                "were retained in training and validation and were not removed as outliers."
            ),
        }

    @staticmethod
    def _split_indices(row_count: int, test_ratio: float, random_seed: int) -> Tuple[np.ndarray, np.ndarray]:
        shuffled = np.arange(row_count)
        rng = np.random.default_rng(random_seed)
        rng.shuffle(shuffled)
        split_at = max(1, int(round(row_count * (1 - test_ratio))))
        split_at = min(split_at, row_count - 1)
        return shuffled[:split_at], shuffled[split_at:]

    @staticmethod
    def _fit_linearized_parameters(
        chloride: np.ndarray,
        temperature_k: np.ndarray,
        ph: np.ndarray,
        corrosion_rate: np.ndarray,
    ) -> Dict[str, float]:
        X = np.column_stack(
            [
                np.ones(len(chloride)),
                np.log(chloride),
                1.0 / temperature_k,
                ph,
            ]
        )
        y = np.log(corrosion_rate)
        coefficients, *_ = np.linalg.lstsq(X, y, rcond=None)

        intercept, b, inverse_temp_coef, c = coefficients
        return {
            "A": float(np.exp(intercept)),
            "b": float(b),
            "K": float(-inverse_temp_coef),
            "c": float(c),
        }

    @classmethod
    def _build_linearized_summary(
        cls,
        chloride: np.ndarray,
        temperature_k: np.ndarray,
        ph: np.ndarray,
        corrosion_rate: np.ndarray,
    ) -> Dict:
        X = np.column_stack(
            [
                np.ones(len(chloride)),
                np.log(chloride),
                1.0 / temperature_k,
                ph,
            ]
        )
        y = np.log(corrosion_rate)
        coefficients, *_ = np.linalg.lstsq(X, y, rcond=None)

        n_obs = X.shape[0]
        n_params = X.shape[1]
        degrees_of_freedom = max(1, n_obs - n_params)
        residuals = y - X @ coefficients
        mse = float(np.sum(np.square(residuals)) / degrees_of_freedom)
        xtx_inv = np.linalg.inv(X.T @ X)
        standard_errors = np.sqrt(np.diag(mse * xtx_inv))
        t_stats = coefficients / standard_errors
        p_values = [cls._two_tailed_p_value(float(t)) for t in t_stats]

        feature_rows = []
        feature_names = ["ln(A)", "b for ln([Cl-])", "-K for (1/Tk)", "c for pH"]

        for name, coefficient, std_err, t_stat, p_value in zip(
            feature_names, coefficients, standard_errors, t_stats, p_values
        ):
            feature_rows.append(
                {
                    "term": name,
                    "coefficient": round(float(coefficient), 6),
                    "std_error": round(float(std_err), 6),
                    "t_stat": round(float(t_stat), 4),
                    "p_value": round(float(p_value), 6),
                }
            )

        return {
            "equation": "ln(CR) = ln(A) + b*ln([Cl-]) - K*(1/Tk) + c*pH",
            "degrees_of_freedom": int(degrees_of_freedom),
            "coefficients": feature_rows,
        }

    @staticmethod
    def _maybe_refine_nonlinear_parameters(
        initial_params: Dict[str, float],
        chloride: np.ndarray,
        temperature_k: np.ndarray,
        ph: np.ndarray,
        corrosion_rate: np.ndarray,
    ) -> Tuple[Dict[str, float], str]:
        try:
            from scipy.optimize import curve_fit
        except Exception:
            return CorrosionModelTrainer._fit_custom_nonlinear_parameters(
                initial_params,
                chloride,
                temperature_k,
                ph,
                corrosion_rate,
            )

        def model(inputs, A, b, K, c):
            cl_values, tk_values, ph_values = inputs
            return (
                A
                * np.power(cl_values, b)
                * np.exp(-K / tk_values)
                * np.exp(c * ph_values)
            )

        p0 = [
            initial_params["A"],
            initial_params["b"],
            initial_params["K"],
            initial_params["c"],
        ]

        try:
            optimized, _ = curve_fit(
                model,
                (chloride, temperature_k, ph),
                corrosion_rate,
                p0=p0,
                maxfev=20000,
            )
        except Exception:
            return initial_params, "linearized_ols"

        return (
            {
                "A": float(optimized[0]),
                "b": float(optimized[1]),
                "K": float(optimized[2]),
                "c": float(optimized[3]),
            },
            "nonlinear_least_squares",
        )

    @staticmethod
    def _fit_custom_nonlinear_parameters(
        initial_params: Dict[str, float],
        chloride: np.ndarray,
        temperature_k: np.ndarray,
        ph: np.ndarray,
        corrosion_rate: np.ndarray,
    ) -> Tuple[Dict[str, float], str]:
        parameters = np.array(
            [
                math.log(initial_params["A"]),
                initial_params["b"],
                initial_params["K"],
                initial_params["c"],
            ],
            dtype=float,
        )

        def evaluate(param_vector: np.ndarray) -> np.ndarray:
            log_a, b, k_value, c_value = param_vector
            return (
                np.exp(log_a)
                * np.power(chloride, b)
                * np.exp(-k_value / temperature_k)
                * np.exp(c_value * ph)
            )

        damping = 1e-2
        best_predictions = evaluate(parameters)
        best_sse = float(np.sum(np.square(corrosion_rate - best_predictions)))

        for _ in range(250):
            jacobian = CorrosionModelTrainer._numerical_jacobian(
                evaluate,
                parameters,
                best_predictions,
            )
            residuals = corrosion_rate - best_predictions
            lhs = jacobian.T @ jacobian + damping * np.eye(len(parameters))
            rhs = jacobian.T @ residuals

            try:
                delta = np.linalg.solve(lhs, rhs)
            except np.linalg.LinAlgError:
                damping *= 10
                continue

            candidate = parameters + delta
            candidate_predictions = evaluate(candidate)
            candidate_sse = float(
                np.sum(np.square(corrosion_rate - candidate_predictions))
            )

            if np.isfinite(candidate_sse) and candidate_sse < best_sse:
                improvement = best_sse - candidate_sse
                parameters = candidate
                best_predictions = candidate_predictions
                best_sse = candidate_sse
                damping = max(damping / 2, 1e-7)
                if improvement < 1e-10:
                    break
            else:
                damping = min(damping * 5, 1e12)

        return (
            {
                "A": float(np.exp(parameters[0])),
                "b": float(parameters[1]),
                "K": float(parameters[2]),
                "c": float(parameters[3]),
            },
            "nonlinear_least_squares_custom",
        )

    @staticmethod
    def _numerical_jacobian(
        evaluate,
        parameters: np.ndarray,
        base_predictions: np.ndarray,
        epsilon: float = 1e-6,
    ) -> np.ndarray:
        jacobian = np.zeros((len(base_predictions), len(parameters)))
        for index in range(len(parameters)):
            step = epsilon * max(1.0, abs(parameters[index]))
            shifted = parameters.copy()
            shifted[index] += step
            jacobian[:, index] = (evaluate(shifted) - base_predictions) / step
        return jacobian

    @staticmethod
    def _two_tailed_p_value(t_stat: float) -> float:
        absolute_t = abs(t_stat)
        try:
            from scipy.stats import t as student_t

            return float(2 * (1 - student_t.cdf(absolute_t, df=1_000_000)))
        except Exception:
            # Normal approximation fallback when scipy is unavailable.
            normal_cdf = 0.5 * (1 + math.erf(absolute_t / math.sqrt(2)))
            return float(2 * (1 - normal_cdf))

    @staticmethod
    def predict(
        chloride: np.ndarray | float,
        temperature_k: np.ndarray | float,
        ph: np.ndarray | float,
        parameters: Dict[str, float],
    ) -> np.ndarray:
        chloride_array = np.asarray(chloride, dtype=float)
        temperature_array = np.asarray(temperature_k, dtype=float)
        ph_array = np.asarray(ph, dtype=float)

        predictions = (
            parameters["A"]
            * np.power(chloride_array, parameters["b"])
            * np.exp(-parameters["K"] / temperature_array)
            * np.exp(parameters["c"] * ph_array)
        )
        return np.maximum(predictions, 1e-6)

    @staticmethod
    def _build_metrics(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
        residual_sum = float(np.sum(np.square(actual - predicted)))
        total_sum = float(np.sum(np.square(actual - np.mean(actual))))
        r_squared = 1.0 - (residual_sum / total_sum) if total_sum else 1.0
        rmse = float(np.sqrt(np.mean(np.square(actual - predicted))))
        mae = float(np.mean(np.abs(actual - predicted)))
        return {
            "r2": round(r_squared, 4),
            "rmse": round(rmse, 4),
            "mae": round(mae, 4),
        }
