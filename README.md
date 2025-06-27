# 🌾 Agricultural Sensor Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![DuckDB](https://img.shields.io/badge/DuckDB-Latest-yellow.svg)](https://duckdb.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌐 Live Demo

### 📊 Interactive Dashboard

Experience the pipeline in action with our **live Streamlit dashboard**:

🔗 **[View Live Dashboard - https://satsure-datapipeline-processing-dashboard-nishant0363.streamlit.app/](https://satsure-datapipeline-processing-dashboard-nishant0363.streamlit.app/)**

![Dashboard Preview](https://drive.google.com/uc?export=view&id=16KQYwiTn8qwS1-JvFTxC_3gvOq6eeyRf)

### 🎯 Dashboard Features

- **Real-time data visualization** of sensor readings
- **Interactive charts** for temperature, humidity, and soil moisture
- **Anomaly detection alerts** with visual indicators  
- **Data quality metrics** and pipeline status
- **Historical trend analysis** with date range selection
- **Export functionality** for processed datasets

### 🚀 Try It Yourself

1. Visit the [live dashboard](https://satsure-datapipeline-processing-dashboard-nishant0363.streamlit.app/)
2. Upload your own sensor data files
3. View real-time processing results
4. Download quality reports and visualizations

---

## 🚀 Overview

A **production-grade data pipeline** for processing agricultural IoT sensor data. This system ingests, transforms, validates, and stores environmental data from farm sensors, delivering clean, enriched datasets optimized for analytics and machine learning applications.

### 📊 What It Does

Our agricultural monitoring system processes sensor data tracking:
- 🌡️ **Temperature & Humidity**
- 💧 **Soil Moisture**
- ☀️ **Light Intensity** 
- 🔋 **Battery Levels**

The pipeline ensures data quality through automated validation, anomaly detection, and statistical enrichment.

---

## 📁 Project Structure

```
agri_pipeline/
├── data/
│   ├── raw/                    # Input Parquet files (daily)
│   │   ├── 2023-06-01.parquet
│   │   ├── 2023-06-02.parquet
│   │   └── 2023-06-03.parquet
│   └── processed/              # Output cleaned & enriched data
├── src/
│   ├── __init__.py
│   ├── ingestion.py           # Data ingestion & validation
│   ├── transformation.py      # Data cleaning & enrichment
│   ├── validation.py          # Quality checks with DuckDB
│   ├── loader.py             # Parquet output with partitioning
│   └── utils.py              # Shared utilities
├── tests/
│   ├── test_transformation.py # Unit tests for transformations
│   ├── test_validation.py     # Unit tests for validation
│   └── test_ingestion.py      # Unit tests for ingestion
├── main.py                    # Pipeline entry point
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🔧 Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agri-pipeline.git
   cd agri-pipeline
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline**
   ```bash
   python main.py
   ```

### 🐳 Docker Setup

```bash
# Build the image
docker build -t agri-pipeline .

# Run the pipeline
docker run --rm -v $(pwd)/data:/app/data agri-pipeline
```

---

## 🧩 Pipeline Architecture

### 1. 📥 **Ingestion** (`src/ingestion.py`)

**Responsibilities:**
- Reads daily Parquet files from `data/raw/`
- Validates schema using DuckDB
- Handles corrupt/malformed files gracefully
- Logs ingestion statistics

**Key Features:**
- ✅ Schema validation for required columns: `sensor_id`, `timestamp`, `reading_type`, `value`, `battery_level`
- ✅ Incremental loading support
- ✅ Robust error handling
- ✅ DuckDB-powered file inspection

**Example Usage:**
```python
from src.ingestion import ingest_files
df = ingest_files("data/raw/")
```

### 2. 🔄 **Transformation** (`src/transformation.py`)

**Data Cleaning:**
- Removes duplicate records
- Handles missing values (drops rows with null critical fields)
- Detects outliers using z-score (|z| > 3)

**Feature Engineering:**
- **Daily averages** per sensor and reading type
- **7-day rolling averages** for trend analysis
- **Timestamp normalization** to UTC+05:30 (IST)
- **Sensor calibration** with type-specific parameters

**Calibration Parameters:**
| Reading Type | Multiplier | Offset | Formula |
|--------------|------------|--------|---------|
| Temperature  | 1.02       | -0.5   | `value = raw_value * 1.02 - 0.5` |
| Humidity     | 0.98       | +1.0   | `value = raw_value * 0.98 + 1.0` |

**Anomaly Detection:**
| Reading Type | Expected Range | Action |
|--------------|----------------|--------|
| Temperature  | 0°C to 60°C    | Flag as `anomalous_reading = True` |
| Humidity     | 0% to 100%     | Flag as `anomalous_reading = True` |

### 3. 📊 **Validation** (`src/validation.py`)

**DuckDB-Powered Quality Checks:**
- Validates data types and formats
- Checks value ranges per reading type
- Detects temporal gaps in hourly data
- Generates comprehensive data quality reports

**Output:** `data/data_quality_report.csv`

**Sample Quality Report:**
| reading_type | total_records | anomaly_pct | missing_pct |
|--------------|---------------|-------------|-------------|
| temperature  | 12,000        | 1.2%        | 0.0%        |
| humidity     | 11,500        | 2.0%        | 0.1%        |
| soil_moisture| 10,800        | 0.8%        | 0.3%        |

### 4. 💾 **Loading** (`src/loader.py`)

**Optimized Storage:**
- Parquet format with Snappy compression
- Date-based partitioning for efficient querying
- Columnar storage for analytics workloads

**Output Structure:**
```
data/processed/
├── 2023-06-01.parquet
├── 2023-06-02.parquet
└── 2023-06-03.parquet
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_transformation.py -v
```

**Test Coverage:**
- ✅ Data preprocessing logic
- ✅ Feature engineering functions
- ✅ Validation and profiling
- ✅ Schema validation
- ✅ Anomaly detection algorithms

---

## 📋 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RAW_DATA_PATH` | Path to raw Parquet files | `data/raw/` |
| `PROCESSED_DATA_PATH` | Output path for processed data | `data/processed/` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Customizing Calibration

Edit calibration parameters in `src/transformation.py`:

```python
calibration_params = {
    'temperature': (1.02, -0.5),    # (multiplier, offset)
    'humidity': (0.98, 1.0),
    'soil_moisture': (1.0, 0.0)     
}
```

### Adjusting Anomaly Thresholds

Modify expected ranges in `src/transformation.py`:

```python
expected_ranges = {
    'temperature': (0, 60),      # Celsius
    'humidity': (0, 100),        # Percentage
    'soil_moisture': (0, 50)     # Custom range
}
```

---

## 📈 Sample Data

The repository includes sample data for testing:

- **3 days** of synthetic sensor data (June 1-3, 2023)
- **Multiple sensor types** with realistic value distributions
- **Intentional anomalies** for validation testing

Access the sample dataset: [Download Sample Data](https://drive.google.com/file/d/1JzvmQU1ETr4MBgOzTYbpjEm43QVOwXIW/view?usp=sharing)

---

## 🔍 Example Queries

After running the pipeline, query your data with DuckDB:

```python
import duckdb

# Connect to processed data
con = duckdb.connect()

# Daily temperature averages
result = con.execute("""
    SELECT 
        DATE_TRUNC('day', timestamp) as date,
        AVG(value) as avg_temp
    FROM read_parquet('data/processed/*.parquet')
    WHERE reading_type = 'temperature'
    GROUP BY date
    ORDER BY date
""").fetchdf()

# Anomaly summary
anomalies = con.execute("""
    SELECT 
        reading_type,
        COUNT(*) as total_anomalies,
        AVG(value) as avg_anomalous_value
    FROM read_parquet('data/processed/*.parquet')
    WHERE anomalous_reading = true
    GROUP BY reading_type
""").fetchdf()
```

## 🛠️ Dependencies

Key libraries used:

```
pandas>=1.5.0          # Data manipulation
duckdb>=0.8.0          # Fast analytical database
pyarrow>=12.0.0        # Parquet I/O
numpy>=1.24.0          # Numerical computing
pytest>=7.0.0          # Testing framework
```

See `requirements.txt` for complete dependency list.

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run linting
flake8 src/ tests/

# Format code
black src/ tests/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact
**Email:** [nishant0363@gmail.com](mailto:nishant0363@gmail.com)
