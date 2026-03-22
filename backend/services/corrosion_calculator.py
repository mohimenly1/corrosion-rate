import json
import os
from typing import Dict, Optional

import numpy as np

try:
    from services.model_trainer import CorrosionModelTrainer
except ModuleNotFoundError:
    from backend.services.model_trainer import CorrosionModelTrainer

class CorrosionRateCalculator:
    """
    Calculator for corrosion rates based on various parameters
    Uses empirical equations and machine learning models
    """
    
    MODEL_PATH = CorrosionModelTrainer.default_model_path()

    @classmethod
    def calculate_corrosion_rate(
        cls,
        material: str,
        temperature: float,
        ph: float,
        nacl_percentage: Optional[float] = None,
        medium: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate corrosion rate based on input parameters
        
        Args:
            material: Material type (e.g., 'API-5L X65', 'Carbon steel')
            temperature: Temperature in Celsius
            ph: pH value
            nacl_percentage: NaCl percentage (optional)
            medium: Medium type (optional)
        
        Returns:
            Dictionary with calculated corrosion rates in mm/yr and mpy
        """
        learned_model = cls._load_or_train_model()

        if learned_model and nacl_percentage is not None and nacl_percentage > 0:
            corrosion_rate_mm_per_yr = cls._predict_with_learned_model(
                temperature=temperature,
                ph=ph,
                nacl_percentage=nacl_percentage,
                parameters=learned_model["parameters"],
            )
            corrosion_rate_mpy = corrosion_rate_mm_per_yr * 39.37

            return {
                'corrosion_rate_mm_per_yr': round(corrosion_rate_mm_per_yr, 4),
                'corrosion_rate_mpy': round(corrosion_rate_mpy, 2),
                'equation_used': learned_model.get('equation', 'Arrhenius power-law model'),
                'model_name': learned_model.get('model_name'),
                'fit_method': learned_model.get('fit_method'),
                'model_metrics': learned_model.get('metrics', {}).get('test', {})
            }

        fallback_result = cls._calculate_legacy_empirical_rate(
            material=material,
            temperature=temperature,
            ph=ph,
            nacl_percentage=nacl_percentage,
            medium=medium,
        )
        fallback_result['equation_used'] = (
            'Legacy empirical multi-factor model '
            '(used when trained NaCl model is unavailable or NaCl input is missing)'
        )
        return fallback_result

    @classmethod
    def _load_or_train_model(cls) -> Optional[Dict]:
        if os.path.exists(cls.MODEL_PATH):
            try:
                with open(cls.MODEL_PATH, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                pass

        try:
            return CorrosionModelTrainer.train_from_csv()
        except Exception:
            return None

    @staticmethod
    def _predict_with_learned_model(
        temperature: float,
        ph: float,
        nacl_percentage: float,
        parameters: Dict[str, float],
    ) -> float:
        temperature_k = temperature + 273.15
        predicted = CorrosionModelTrainer.predict(
            chloride=nacl_percentage,
            temperature_k=temperature_k,
            ph=ph,
            parameters=parameters,
        )
        return float(np.asarray(predicted).reshape(-1)[0])

    @staticmethod
    def _calculate_legacy_empirical_rate(
        material: str,
        temperature: float,
        ph: float,
        nacl_percentage: Optional[float] = None,
        medium: Optional[str] = None
    ) -> Dict[str, float]:
        base_rate = 0.1
        temp_factor = np.exp((temperature - 25) / 30)

        if ph < 7:
            ph_factor = 1 + (7 - ph) * 0.3
        elif ph > 8:
            ph_factor = 1 + (ph - 8) * 0.15
        else:
            ph_factor = 1.0

        if nacl_percentage is not None:
            nacl_factor = 1 + (nacl_percentage / 3.5) * 0.5
        else:
            nacl_factor = 1.0

        if 'X65' in material.upper() or 'API' in material.upper():
            material_factor = 0.8
        elif 'carbon' in material.lower():
            material_factor = 1.2
        else:
            material_factor = 1.0

        medium_factor = 1.0
        if medium:
            medium_lower = medium.lower()
            if 'seawater' in medium_lower or 'sea' in medium_lower:
                medium_factor = 1.3
            elif 'acid' in medium_lower or 'h2so4' in medium_lower:
                medium_factor = 2.5
            elif 'co2' in medium_lower:
                medium_factor = 1.8
            elif 'fresh' in medium_lower or 'water' in medium_lower:
                medium_factor = 0.7

        corrosion_rate_mm_per_yr = (
            base_rate *
            temp_factor *
            ph_factor *
            nacl_factor *
            material_factor *
            medium_factor
        )
        corrosion_rate_mpy = corrosion_rate_mm_per_yr * 39.37

        return {
            'corrosion_rate_mm_per_yr': round(corrosion_rate_mm_per_yr, 4),
            'corrosion_rate_mpy': round(corrosion_rate_mpy, 2),
        }
    
    @staticmethod
    def calculate_using_linear_model(
        material: str,
        temperature: float,
        ph: float,
        nacl_percentage: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Alternative calculation using linear regression model
        Based on empirical data patterns
        """
        
        # Coefficients derived from data analysis
        intercept = 0.05
        temp_coef = 0.002
        ph_coef = -0.01
        nacl_coef = 0.01 if nacl_percentage else 0
        
        # Material coefficients
        if 'X65' in material.upper():
            material_coef = -0.02
        else:
            material_coef = 0.0
        
        corrosion_rate_mm_per_yr = (
            intercept +
            temp_coef * temperature +
            ph_coef * ph +
            nacl_coef * (nacl_percentage or 0) +
            material_coef
        )
        
        # Ensure non-negative
        corrosion_rate_mm_per_yr = max(0.001, corrosion_rate_mm_per_yr)
        
        corrosion_rate_mpy = corrosion_rate_mm_per_yr * 39.37
        
        return {
            'corrosion_rate_mm_per_yr': round(corrosion_rate_mm_per_yr, 4),
            'corrosion_rate_mpy': round(corrosion_rate_mpy, 2),
            'equation_used': 'Linear regression model'
        }
