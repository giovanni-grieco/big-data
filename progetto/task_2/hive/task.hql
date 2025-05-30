DROP TABLE IF EXISTS used_cars;
CREATE TABLE used_cars (
    city STRING, 
    daysonmarket INT,
    description STRING,
    engine_displacement FLOAT,
    horsepower FLOAT,
    make_name STRING,
    model_name STRING,
    price FLOAT,
    year INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH '${hivevar:input_path}' OVERWRITE INTO TABLE used_cars;

-- Create a temporary table to categorize cars into price ranges
CREATE TABLE IF NOT EXISTS categorized_cars AS
SELECT 
    city,
    year,
    CASE 
        WHEN price > 50000 THEN 'alto'
        WHEN price BETWEEN 20000 AND 50000 THEN 'medio'
        ELSE 'basso'
    END AS price_range,
    daysonmarket,
    description
FROM used_cars;

-- Aggregate data for each city, year, and price range
CREATE TABLE IF NOT EXISTS aggregated_data AS
SELECT 
    city,
    year,
    price_range,
    COUNT(*) AS num_cars,
    AVG(daysonmarket) AS avg_daysonmarket,
    CONCAT_WS('|||', COLLECT_LIST(description)) AS descriptions
FROM categorized_cars
GROUP BY city, year, price_range;

-- Use ADD FILE to make the Python script available to the cluster
ADD FILE /home/giovanni/Projects/big-data/progetto/task_2/hive/extract_top_words.py;

-- Create a final table with the results using the correct TRANSFORM syntax
CREATE TABLE IF NOT EXISTS report 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
AS
SELECT
  TRANSFORM(city, year, price_range, num_cars, avg_daysonmarket, descriptions)
  USING 'python extract_top_words.py'
  AS city, year, price_range, num_cars, avg_daysonmarket, top_3_words
FROM aggregated_data;

-- Output the final report
SELECT * FROM report;

-- Clean up temporary tables
DROP TABLE categorized_cars;
DROP TABLE aggregated_data;
DROP TABLE used_cars;
DROP TABLE report;