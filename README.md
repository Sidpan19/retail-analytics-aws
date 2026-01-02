# Scalable Retail Analytics Pipeline on AWS

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PySpark](https://img.shields.io/badge/PySpark-3.5-orange)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3%20%7C%20SageMaker-yellow)

## 🎯 Project Overview

End-to-end Big Data analytics pipeline built on AWS cloud infrastructure to process and analyze 1M+ retail transactions. Leverages Apache Spark for distributed computing, AWS services for scalable storage and ML, and Power BI for business intelligence dashboards.

**Built as part of:** Big Data Applications Course (Indiana University, Fall 2025)

---

## 🚀 Key Technologies

**Big Data & Processing:**
- Apache Spark 3.5 / PySpark
- Distributed computing on AWS EC2
- ETL pipeline automation

**Cloud Infrastructure (AWS):**
- **S3:** Data Lake architecture (raw/processed separation)
- **EC2:** t2.micro instance (Ubuntu 22.04) for Spark processing
- **SageMaker Canvas:** No-code ML model training
- **IAM:** Role-based security for S3 access
- **Boto3:** AWS SDK for Python

**Analytics & Visualization:**
- Spark SQL for distributed queries
- Power BI for interactive dashboards
- Statistical aggregation and trend analysis

---

## 📊 Business Impact

✅ **Processed 1,067,371 transaction records** across 38 countries (2009-2011)  
✅ **Analyzed £14M+ in revenue**, identifying UK as dominant market (80%+ share)  
✅ **Discovered 300% sales spike** in November for inventory optimization  
✅ **Reduced analysis time** from manual Excel workflows (hours) → automated Spark pipeline (minutes)  
✅ **Identified top-selling products** driving 100K+ unit sales  

---

## 🏗️ Architecture
```
┌─────────────────┐
│   Raw CSV Data  │
│   (UCI Dataset) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       AWS S3 (Data Lake)            │
│  ┌─────────────┐  ┌──────────────┐  │
│  │  raw_data/  │  │processed_data/│ │
│  └─────────────┘  └──────────────┘  │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│     AWS EC2 (Ubuntu 22.04)          │
│   ┌─────────────────────────────┐   │
│   │   Apache Spark 3.5          │   │
│   │   - PySpark ETL Pipeline    │   │
│   │   - Data Cleaning           │   │
│   │   - Feature Engineering     │   │
│   │   - Aggregation & Metrics   │   │
│   └─────────────────────────────┘   │
└──────────┬──────────────────────────┘
           │
           ├──────────────────┐
           ▼                  ▼
┌──────────────────┐  ┌─────────────────┐
│  AWS SageMaker   │  │    Power BI     │
│     Canvas       │  │   Dashboard     │
│  (ML Prediction) │  │ (Visualization) │
└──────────────────┘  └─────────────────┘
```

---

## 🔧 Technical Implementation

### 1️⃣ Data Ingestion & Storage
- **Dataset:** Online Retail II from UCI ML Repository (1.06M rows, 8 attributes)
- **Storage Pattern:** Download from S3 → Process locally on EC2 → Upload results to S3
- **Security:** IAM role-based authentication (no hardcoded API keys)

### 2️⃣ ETL Pipeline (PySpark)

**Data Cleaning Steps:**
```python
# Remove cancellations (Invoice starting with 'C')
df_clean = df.filter(~col("Invoice").startswith("C"))

# Type casting and null handling
df_clean = df_clean.withColumn("Quantity", col("Quantity").cast("int")) \
                   .withColumn("Price", col("Price").cast("double")) \
                   .dropna(subset=['Description', 'Customer ID'])

# Feature engineering
df_processed = df_clean.withColumn("TotalLinePrice", 
                                   col("Quantity") * col("Price"))
```

**Result:** 800,000+ valid transactions after cleaning (75% of raw data)

### 3️⃣ Business Metrics & Aggregation

**Key Queries Implemented:**
```python
# Top selling products
df_processed.groupBy("Description") \
    .agg(_sum("Quantity").alias("Total_Sold")) \
    .orderBy(desc("Total_Sold")).limit(5)

# Revenue by country
df_processed.groupBy("Country") \
    .agg(_sum("TotalLinePrice").alias("Total_Revenue")) \
    .orderBy(desc("Total_Revenue"))

# Monthly sales trends (seasonality analysis)
df_processed.groupBy("Year", "Month") \
    .agg(_sum("TotalLinePrice").alias("Sales")) \
    .orderBy("Year", "Month")
```

### 4️⃣ Machine Learning (AWS SageMaker Canvas)
- **Model Type:** Regression (Quick Build)
- **Target Variable:** `TotalLinePrice` (transaction value prediction)
- **Key Finding:** `Quantity` identified as strongest predictor (aligns with retail logic)

### 5️⃣ Visualization (Power BI)
- **Geospatial map** showing revenue distribution across 38 countries
- **Time-series trends** highlighting November sales spike (seasonal pattern)
- **Product ranking** bar chart for top 5 performing items
- **KPI cards** displaying total revenue, transaction count

**📊 View Dashboard:** [Google Drive Link](https://drive.google.com/file/d/1KF3S7Xy0qlM-uMY9rnP_5KwRXbgw_k0q/view?usp=sharing)  
*(Download .pbix file to view in Power BI Desktop)*

---

## 📈 Key Insights Discovered

### Market Analysis
- **United Kingdom:** £14M+ revenue (80%+ of total sales)
- **International Growth Opportunity:** EIRE, Netherlands, Germany show potential but underserved

### Product Performance
- **Top Seller:** "WORLD WAR 2 GLIDERS ASSTD DESIGNS" (100K+ units)
- **Strategy:** Mix of low-cost high-volume novelty items + premium home decor

### Seasonality
- **November Spike:** 300% increase in sales (pre-Christmas shopping behavior)
- **Actionable:** Optimize inventory and staffing for Q4

### Customer Segmentation
- **Wholesale Focus:** Many customers are B2B wholesalers (bulk purchases)
- **Opportunity:** Develop targeted loyalty programs for top customers

---

## 🖼️ Sample Outputs

### Spark Processing (Terminal Output)
```
--- 1. Ingesting Data from local_data.csv ---
Total Rows Loaded: 1067371

--- 2. Cleaning & Processing ---
Valid Clean Transactions: 801857

--- Aggregation Metrics ---
1. Top Selling Products:
+------------------------------------------+----------+
|Description                               |Total_Sold|
+------------------------------------------+----------+
|WORLD WAR 2 GLIDERS ASSTD DESIGNS         |102942    |
|JUMBO BAG RED RETROSPOT                   |88280     |
|ASSORTED COLOUR BIRD ORNAMENT             |81416     |
|WHITE HANGING HEART T-LIGHT HOLDER        |79819     |
|PACK OF 72 RETROSPOT CAKE CASES           |70988     |
+------------------------------------------+----------+

2. Revenue by Country:
+--------------+------------------+
|Country       |Total_Revenue     |
+--------------+------------------+
|United Kingdom|14382877.59       |
|EIRE          |789094.82         |
|Netherlands   |284861.33         |
|Germany       |281697.84         |
|France        |211892.41         |
+--------------+------------------+
```

### Power BI Dashboard Preview
![Dashboard](screenshots/powerbi_dashboard.png)
*Interactive dashboard showing geospatial revenue map, monthly trends, and product rankings*

---

## 🚦 How to Run Locally

### Prerequisites
```bash
# System requirements
- Python 3.10+
- Java 17 (OpenJDK)
- 4GB+ RAM recommended

# Install dependencies
pip install -r requirements.txt
```

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/yourusername/retail-analytics-aws.git
cd retail-analytics-aws

# 2. Download sample dataset
# Place CSV file in project root as 'local_data.csv'

# 3. Configure AWS credentials (if using S3)
aws configure
# Enter your AWS Access Key ID, Secret Key, and region

# 4. Run pipeline
python pipeline.py
```

### Expected Output
- Cleaned data saved to `processed_output/` directory
- Aggregated metrics printed to console
- (Optional) Processed data uploaded to S3 bucket

---

## 📁 Project Structure
```
retail-analytics-aws/
│
├── README.md                 # This file
├── pipeline.py               # Main ETL script (PySpark)
├── requirements.txt          # Python dependencies
├── local_data.csv            # Sample dataset (not included - too large)
│
├── processed_output/         # Generated after running pipeline
│   └── final_data.csv        # Cleaned and processed transactions
│
├── screenshots/              # Visual documentation
│   ├── powerbi_dashboard.png
│   ├── spark_execution.png
│   └── sagemaker_model.png
│
└── docs/                     # Additional documentation
    └── project-report.pdf    # Full technical report
```

---

## 🧩 Challenges & Solutions

### Challenge 1: S3A Connector Compatibility
**Problem:** `NumberFormatException: "60s"` when reading directly from S3 using `spark.read.csv("s3a://...")`  
**Root Cause:** Hadoop-AWS connector incompatibility with Java 21 on Ubuntu  
**Solution:** Implemented "Download-Process-Upload" pattern using Boto3 for reliable S3 interaction

### Challenge 2: Free Tier Memory Constraints
**Problem:** t2.micro instance (1GB RAM) caused `MemoryError` during package installation  
**Solution:** Used `pip install --no-cache-dir` and OpenJDK-headless to minimize memory footprint

### Challenge 3: Data Quality Issues
**Problem:** Negative quantities (cancellations) and null Customer IDs skewed metrics  
**Solution:** Implemented rigorous filtering logic to exclude invalid records (25% data reduction)

---

## 📚 Dataset Information

**Source:** UCI Machine Learning Repository  
**Name:** Online Retail II Data Set  
**Period:** December 1, 2009 - December 9, 2011  
**Business:** UK-based online gift retailer (B2B and B2C)  

**Attributes:**
- `InvoiceNo`: Transaction ID (6-digit, 'C' prefix = cancellation)
- `StockCode`: Product ID (5-digit)
- `Description`: Product name
- `Quantity`: Items per transaction
- `InvoiceDate`: Timestamp
- `UnitPrice`: Price in GBP (£)
- `CustomerID`: Customer identifier (5-digit)
- `Country`: Customer location

**Citation:**  
Chen, D. (2015). *Online Retail II Data Set*. UCI Machine Learning Repository.  
https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

---

## 🎓 Learning Outcomes

- Designed and deployed scalable cloud-based data pipelines on AWS
- Processed large-scale datasets using distributed computing (Apache Spark)
- Implemented ETL workflows with data quality checks and feature engineering
- Built predictive models using AWS SageMaker for business forecasting
- Created interactive dashboards for stakeholder communication
- Applied IAM security best practices for cloud resource access

---

## 🔗 Additional Resources

- **Full Project Report:** [View PDF](docs/project_report.pdf)
- **Power BI Dashboard:** [Download .pbix](https://drive.google.com/file/d/1KF3S7Xy0qlM-uMY9rnP_5KwRXbgw_k0q/view?usp=sharing)
- **Demo Video:** [Watch on Google Drive](https://drive.google.com/file/d/1m9lbA3doBeAkluqEgM88n3W_NJ8CEv33/view?usp=sharing)

---

## 👨‍💻 Author

**Siddhesh Pande**  
MS Data Science, Indiana University  
[LinkedIn](https://linkedin.com/in/siddhesh-pande) | [GitHub](https://github.com/sidpan19)

---

## 📝 License

This project is for educational purposes. Dataset used under UCI ML Repository terms.

---

## 🙏 Acknowledgments

- **Course:** Big Data Applications (Indiana University)
- **Dataset:** UCI Machine Learning Repository
- **Cloud Credits:** AWS Educate Free Tier
