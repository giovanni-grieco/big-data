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

-- Use the TRANSFORM function with MapReduce syntax
SELECT 
    t.city,
    t.year,
    t.price_range,
    t.num_cars,
    t.avg_daysonmarket,
    transformed.top_words AS top_3_words
FROM (
    SELECT 
        city, 
        year, 
        price_range, 
        num_cars, 
        avg_daysonmarket, 
        descriptions
    FROM aggregated_data
) t
LATERAL VIEW 
TRANSFORM(t.descriptions) AS top_words
USING 'python extract_top_words.py';

-- Clean up temporary tables
DROP TABLE categorized_cars;
DROP TABLE aggregated_data;
DROP TABLE used_cars;