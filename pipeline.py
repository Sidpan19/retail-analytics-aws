import sys
import boto3
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, month, year, sum as _sum, desc, count, lit  # [web:1][web:3]

# --- CONFIG ---
# We use LOCAL paths now
INPUT_FILE = "local_data.csv"
OUTPUT_DIR = "processed_output"
BUCKET_NAME = "bda-miniproject-sipande"

# --- INIT SPARK (No S3 config needed now!) ---
spark = SparkSession.builder \
    .appName("Retail_Local_Process") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print(f"--- 1. Ingesting Data from {INPUT_FILE} ---")
# NOW we can use the proper CSV reader because local file system is safe
df = spark.read.csv(INPUT_FILE, header=True, inferSchema=True)  # [web:6][web:9]
print(f"Total Rows Loaded: {df.count()}")

print("\n--- 2. Cleaning & Processing ---")

# 1. Remove Cancellations
df_clean = df.filter(~col("Invoice").startswith("C"))

# 2. Type Casting & Cleaning
df_clean = (
    df_clean
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("Price", col("Price").cast("double"))
    .dropna(subset=["Description", "Customer ID"])
)

# 3. Calculate Total
df_processed = df_clean.withColumn(
    "TotalLinePrice",
    col("Quantity") * col("Price")
)

# 4. Parse Date
df_processed = (
    df_processed
    .withColumn(
        "timestamp_obj",
        to_timestamp(col("InvoiceDate"), "yyyy-MM-dd HH:mm:ss")
    )
    .withColumn("Year", year("timestamp_obj"))
    .withColumn("Month", month("timestamp_obj"))
)

print(f"Valid Clean Transactions: {df_processed.count()}")

# --- AGGREGATION (Task 2) ---
print("\n--- Aggregation Metrics ---")

print("1. Top Selling Products:")
df_processed.groupBy("Description") \
    .agg(_sum("Quantity").alias("Total_Sold")) \
    .orderBy(desc("Total_Sold")) \
    .limit(5) \
    .show(truncate=False)

print("2. Revenue by Country:")
df_processed.groupBy("Country") \
    .agg(_sum("TotalLinePrice").alias("Total_Revenue")) \
    .orderBy(desc("Total_Revenue")) \
    .limit(5) \
    .show()

print("3. Monthly Sales:")
df_processed.groupBy("Year", "Month") \
    .agg(_sum("TotalLinePrice").alias("Sales")) \
    .orderBy("Year", "Month") \
    .show()

# --- WRITE TO LOCAL DISK (Task 3) ---
print("\n--- 3. Writing Processed Data ---")
df_final = df_processed.drop("timestamp_obj")
df_final.coalesce(1) \
    .write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(OUTPUT_DIR)  # [web:6][web:9]

print(f"Data saved locally to {OUTPUT_DIR}")

# --- MANUAL UPLOAD TO S3 (Boto3) ---
print("\n--- 4. Uploading to S3 ---")
# Find the CSV part file inside the directory
local_path = None
for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".csv"):
        local_path = os.path.join(OUTPUT_DIR, file)
        break

if local_path is None:
    raise FileNotFoundError("No CSV file found in output directory to upload.")

s3_key = "processed_data/retail_processed/final_data.csv"
print(f"Uploading {local_path} to s3://{BUCKET_NAME}/{s3_key}...")

s3 = boto3.client("s3")
s3.upload_file(local_path, BUCKET_NAME, s3_key)  # [web:7][web:10]
print("Upload Success!")

spark.stop()
