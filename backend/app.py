from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from config import Config
from database.db_connection import DatabaseConnection
from services.csv_processor import CSVProcessor
from services.corrosion_calculator import CorrosionRateCalculator

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = DatabaseConnection()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Corrosion Rate API is running'})

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """Upload and process CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process CSV
            processor = CSVProcessor()
            processed_data = processor.process_corrosion_csv(filepath)
            
            # Save to database
            saved_count = 0
            for data in processed_data:
                try:
                    query = """
                        INSERT INTO corrosion_samples 
                        (sample_id, material, medium, nacl_percentage, temperature, ph,
                         corrosion_rate_mm_per_yr, corrosion_rate_mpy, method, source, notes)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (
                        data.get('sample_id'),
                        data.get('material'),
                        data.get('medium'),
                        data.get('nacl_percentage'),
                        data.get('temperature'),
                        data.get('ph'),
                        data.get('corrosion_rate_mm_per_yr'),
                        data.get('corrosion_rate_mpy'),
                        data.get('method'),
                        data.get('source'),
                        data.get('notes')
                    )
                    db.execute_query(query, params)
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving record: {e}")
                    continue
            
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'rows_processed': len(processed_data),
                'rows_saved': saved_count
            }), 200
        
        return jsonify({'error': 'Invalid file type. Please upload a CSV file'}), 400
        
    except Exception as e:
        logger.error(f"Error uploading CSV: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-corrosion-rate', methods=['POST'])
def calculate_corrosion_rate():
    """Calculate corrosion rate from input parameters"""
    try:
        data = request.json
        
        material = data.get('material')
        temperature = data.get('temperature')
        ph = data.get('ph')
        nacl_percentage = data.get('nacl_percentage')
        medium = data.get('medium')
        
        if not material or temperature is None:
            return jsonify({'error': 'Material and temperature are required'}), 400
        
        calculator = CorrosionRateCalculator()
        result = calculator.calculate_corrosion_rate(
            material=material,
            temperature=float(temperature),
            ph=float(ph) if ph is not None else 7.0,
            nacl_percentage=float(nacl_percentage) if nacl_percentage else None,
            medium=medium
        )
        
        # Save calculation to database
        try:
            query = """
                INSERT INTO calculated_corrosion_rates
                (material, medium, temperature, ph, nacl_percentage,
                 calculated_rate_mm_per_yr, calculated_rate_mpy, equation_used, input_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            import json
            params = (
                material,
                medium,
                temperature,
                ph,
                nacl_percentage,
                result['corrosion_rate_mm_per_yr'],
                result['corrosion_rate_mpy'],
                result['equation_used'],
                json.dumps(data)
            )
            db.execute_query(query, params)
        except Exception as e:
            logger.error(f"Error saving calculation: {e}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error calculating corrosion rate: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/samples', methods=['GET'])
def get_samples():
    """Get all corrosion samples with optional filters"""
    try:
        material = request.args.get('material')
        min_temp = request.args.get('min_temp')
        max_temp = request.args.get('max_temp')
        min_ph = request.args.get('min_ph')
        max_ph = request.args.get('max_ph')
        medium = request.args.get('medium')
        
        query = "SELECT * FROM corrosion_samples WHERE 1=1"
        params = []
        
        if material:
            query += " AND material LIKE %s"
            params.append(f"%{material}%")
        
        if min_temp:
            query += " AND temperature >= %s"
            params.append(float(min_temp))
        
        if max_temp:
            query += " AND temperature <= %s"
            params.append(float(max_temp))
        
        if min_ph:
            query += " AND ph >= %s"
            params.append(float(min_ph))
        
        if max_ph:
            query += " AND ph <= %s"
            params.append(float(max_ph))
        
        if medium:
            query += " AND medium LIKE %s"
            params.append(f"%{medium}%")
        
        query += " ORDER BY created_at DESC LIMIT 1000"
        
        try:
            results = db.execute_query(query, tuple(params) if params else None)
            
            # Convert Decimal to float for JSON serialization
            import decimal
            for row in results:
                for key, value in row.items():
                    if isinstance(value, decimal.Decimal):
                        row[key] = float(value)
        except Exception as db_error:
            logger.error(f"Database error in get_samples: {db_error}")
            # Check if table exists
            try:
                test_query = "SELECT COUNT(*) as count FROM corrosion_samples"
                db.execute_query(test_query)
            except Exception as table_error:
                logger.error(f"Table might not exist: {table_error}")
                return jsonify({
                    'error': 'Database table not found. Please run the database setup script.',
                    'details': str(table_error)
                }), 500
            raise db_error
        
        return jsonify({'samples': results}), 200
        
    except Exception as e:
        logger.error(f"Error fetching samples: {e}", exc_info=True)
        return jsonify({
            'error': str(e),
            'message': 'Failed to fetch samples from database'
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics for visualization"""
    try:
        # Corrosion rate vs pH
        ph_query = """
            SELECT ph, AVG(corrosion_rate_mm_per_yr) as avg_rate
            FROM corrosion_samples
            WHERE ph IS NOT NULL AND corrosion_rate_mm_per_yr IS NOT NULL
            GROUP BY ph
            ORDER BY ph
        """
        ph_data = db.execute_query(ph_query)
        
        # Corrosion rate vs Temperature
        temp_query = """
            SELECT temperature, AVG(corrosion_rate_mm_per_yr) as avg_rate
            FROM corrosion_samples
            WHERE temperature IS NOT NULL AND corrosion_rate_mm_per_yr IS NOT NULL
            GROUP BY temperature
            ORDER BY temperature
        """
        temp_data = db.execute_query(temp_query)
        
        # Corrosion rate vs Medium
        medium_query = """
            SELECT medium, AVG(corrosion_rate_mm_per_yr) as avg_rate, COUNT(*) as count
            FROM corrosion_samples
            WHERE medium IS NOT NULL AND corrosion_rate_mm_per_yr IS NOT NULL
            GROUP BY medium
            ORDER BY avg_rate DESC
        """
        medium_data = db.execute_query(medium_query)
        
        # Material comparison
        material_query = """
            SELECT material, AVG(corrosion_rate_mm_per_yr) as avg_rate, COUNT(*) as count
            FROM corrosion_samples
            WHERE material IS NOT NULL AND corrosion_rate_mm_per_yr IS NOT NULL
            GROUP BY material
            ORDER BY avg_rate DESC
        """
        material_data = db.execute_query(material_query)
        
        return jsonify({
            'ph_vs_rate': ph_data,
            'temperature_vs_rate': temp_data,
            'medium_vs_rate': medium_data,
            'material_comparison': material_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get list of available materials"""
    try:
        query = "SELECT DISTINCT material FROM corrosion_samples WHERE material IS NOT NULL"
        results = db.execute_query(query)
        materials = [r['material'] for r in results]
        return jsonify({'materials': materials}), 200
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mediums', methods=['GET'])
def get_mediums():
    """Get list of available mediums"""
    try:
        query = "SELECT DISTINCT medium FROM corrosion_samples WHERE medium IS NOT NULL"
        results = db.execute_query(query)
        mediums = [r['medium'] for r in results if r['medium']]
        return jsonify({'mediums': mediums}), 200
    except Exception as e:
        logger.error(f"Error fetching mediums: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Serve dashboard HTML page"""
    return send_from_directory('static', 'dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.FLASK_PORT, debug=(Config.FLASK_ENV == 'development'))

