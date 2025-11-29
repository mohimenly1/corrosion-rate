-- Corrosion Rate Database Schema
CREATE DATABASE IF NOT EXISTS corrosion_db;
USE corrosion_db;

-- Table for storing corrosion data samples
CREATE TABLE IF NOT EXISTS corrosion_samples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id VARCHAR(100),
    material VARCHAR(100) NOT NULL,
    medium VARCHAR(100),
    nacl_percentage DECIMAL(10, 2),
    temperature DECIMAL(10, 2) NOT NULL,
    ph DECIMAL(10, 2),
    corrosion_rate_mm_per_yr DECIMAL(10, 4),
    corrosion_rate_mpy DECIMAL(10, 4),
    method VARCHAR(255),
    source VARCHAR(500),
    environment_description TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_material (material),
    INDEX idx_temperature (temperature),
    INDEX idx_ph (ph),
    INDEX idx_medium (medium)
);

-- Table for storing calculated corrosion rates
CREATE TABLE IF NOT EXISTS calculated_corrosion_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id INT,
    material VARCHAR(100) NOT NULL,
    medium VARCHAR(100),
    temperature DECIMAL(10, 2) NOT NULL,
    ph DECIMAL(10, 2),
    nacl_percentage DECIMAL(10, 2),
    calculated_rate_mm_per_yr DECIMAL(10, 4),
    calculated_rate_mpy DECIMAL(10, 4),
    equation_used VARCHAR(255),
    input_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sample_id) REFERENCES corrosion_samples(id) ON DELETE CASCADE,
    INDEX idx_calc_material (material),
    INDEX idx_calc_temperature (temperature),
    INDEX idx_calc_ph (ph)
);

-- Table for storing uploaded CSV files metadata
CREATE TABLE IF NOT EXISTS csv_uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    rows_imported INT DEFAULT 0,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);

