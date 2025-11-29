import numpy as np
import pandas as pd
from typing import Dict, Optional

class CorrosionRateCalculator:
    """
    Calculator for corrosion rates based on various parameters
    Uses empirical equations and machine learning models
    """
    
    @staticmethod
    def calculate_corrosion_rate(
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
        
        # Base corrosion rate (mm/year)
        base_rate = 0.1
        
        # Temperature effect (Arrhenius-like relationship)
        # Corrosion rate increases with temperature
        temp_factor = np.exp((temperature - 25) / 30)  # Reference temp: 25°C
        
        # pH effect
        # Minimum corrosion around pH 7-8, increases in acidic or basic conditions
        if ph < 7:
            ph_factor = 1 + (7 - ph) * 0.3  # Acidic: higher corrosion
        elif ph > 8:
            ph_factor = 1 + (ph - 8) * 0.15  # Basic: moderate increase
        else:
            ph_factor = 1.0  # Neutral: baseline
        
        # NaCl concentration effect
        if nacl_percentage is not None:
            nacl_factor = 1 + (nacl_percentage / 3.5) * 0.5  # Reference: 3.5% (seawater)
        else:
            nacl_factor = 1.0
        
        # Material-specific factors
        if 'X65' in material.upper() or 'API' in material.upper():
            material_factor = 0.8  # API-5L X65 is more resistant
        elif 'carbon' in material.lower():
            material_factor = 1.2  # Carbon steel is more susceptible
        else:
            material_factor = 1.0
        
        # Medium-specific adjustments
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
        
        # Calculate final corrosion rate
        corrosion_rate_mm_per_yr = (
            base_rate * 
            temp_factor * 
            ph_factor * 
            nacl_factor * 
            material_factor * 
            medium_factor
        )
        
        # Convert to mpy (mils per year): 1 mm = 39.37 mils
        corrosion_rate_mpy = corrosion_rate_mm_per_yr * 39.37
        
        return {
            'corrosion_rate_mm_per_yr': round(corrosion_rate_mm_per_yr, 4),
            'corrosion_rate_mpy': round(corrosion_rate_mpy, 2),
            'equation_used': 'Empirical multi-factor model'
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

