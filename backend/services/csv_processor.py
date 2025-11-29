import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CSVProcessor:
    """Process CSV files and extract corrosion data"""
    
    @staticmethod
    def process_corrosion_csv(file_path: str) -> List[Dict]:
        """
        Process corrosion CSV file and return standardized data
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            List of dictionaries with standardized corrosion data
        """
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded CSV with {len(df)} rows")
            
            processed_data = []
            
            for idx, row in df.iterrows():
                data = CSVProcessor._extract_row_data(row, df.columns)
                if data:
                    processed_data.append(data)
            
            logger.info(f"Processed {len(processed_data)} valid records")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            raise
    
    @staticmethod
    def _extract_row_data(row: pd.Series, columns: pd.Index) -> Optional[Dict]:
        """Extract and standardize data from a CSV row"""
        
        data = {}
        
        # Material
        material_cols = ['Material', 'material', 'MATERIAL']
        for col in material_cols:
            if col in columns and pd.notna(row.get(col)):
                data['material'] = str(row[col]).strip()
                break
        
        # Temperature
        temp_cols = ['Temp (°C)', 'Temperature (°C)', 'temperature', 'Temperature', 'Temp']
        for col in temp_cols:
            if col in columns and pd.notna(row.get(col)):
                try:
                    temp_str = str(row[col]).replace('°C', '').strip()
                    # Handle ranges like "25-30"
                    if '-' in temp_str:
                        temp_str = temp_str.split('-')[0]
                    data['temperature'] = float(temp_str)
                except:
                    pass
                break
        
        # pH
        ph_cols = ['pH', 'ph', 'PH']
        for col in ph_cols:
            if col in columns and pd.notna(row.get(col)):
                try:
                    ph_val = str(row[col]).replace('~', '').strip()
                    if ph_val:
                        data['ph'] = float(ph_val)
                except:
                    pass
                break
        
        # NaCl percentage
        nacl_cols = ['NaCl (%)', 'NaCl (wt%)', 'NaCl', 'nacl_percentage']
        for col in nacl_cols:
            if col in columns and pd.notna(row.get(col)):
                try:
                    nacl_val = str(row[col]).strip()
                    if nacl_val and nacl_val.lower() not in ['n/a', 'na', 'variable', 'sea', '']:
                        # Handle ranges
                        if '-' in nacl_val:
                            nacl_val = nacl_val.split('-')[0]
                        data['nacl_percentage'] = float(nacl_val)
                except:
                    pass
                break
        
        # Medium/Environment
        medium_cols = ['Environment', 'environment', 'Medium', 'medium']
        for col in medium_cols:
            if col in columns and pd.notna(row.get(col)):
                data['medium'] = str(row[col]).strip()
                break
        
        # Corrosion rate (mm/yr)
        cr_mm_cols = ['Corrosion_mm_per_yr', 'Estimated Corrosion Rate (mm/yr)', 
                      'Corrosion Rate (mm/yr)', 'corrosion_rate_mm_per_yr']
        for col in cr_mm_cols:
            if col in columns and pd.notna(row.get(col)):
                try:
                    data['corrosion_rate_mm_per_yr'] = float(row[col])
                except:
                    pass
                break
        
        # Corrosion rate (mpy)
        cr_mpy_cols = ['Corrosion_mpy', 'Estimated Corrosion Rate (mpy)', 
                       'Corrosion Rate (mpy)', 'corrosion_rate_mpy']
        for col in cr_mpy_cols:
            if col in columns and pd.notna(row.get(col)):
                try:
                    data['corrosion_rate_mpy'] = float(row[col])
                except:
                    pass
                break
        
        # Sample ID
        id_cols = ['Sample ID', 'sample_id', '#', 'ID']
        for col in id_cols:
            if col in columns and pd.notna(row.get(col)):
                data['sample_id'] = str(row[col]).strip()
                break
        
        # Source
        source_cols = ['Source', 'source']
        for col in source_cols:
            if col in columns and pd.notna(row.get(col)):
                data['source'] = str(row[col]).strip()
                break
        
        # Method
        method_cols = ['Method', 'method']
        for col in method_cols:
            if col in columns and pd.notna(row.get(col)):
                data['method'] = str(row[col]).strip()
                break
        
        # Notes
        notes_cols = ['Notes', 'notes']
        for col in notes_cols:
            if col in columns and pd.notna(row.get(col)):
                data['notes'] = str(row[col]).strip()
                break
        
        # Validate required fields
        if 'material' in data and 'temperature' in data:
            return data
        
        return None

