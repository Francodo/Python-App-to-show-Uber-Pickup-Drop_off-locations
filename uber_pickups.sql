This is the sql schema for processing the data for 'uber_pickups.py'

    1. Create a database
    2. Create schema
    3. Create a stage
    4. Upload Uber data (Raw) to the stage
    5. Create a file format
    6. Create a table in the database
    7. Copy the Uber data into the table
    8. Explore the data and be familiar with column objects.

uber-raw-data-sep14.csv
use role sysadmin;

CREATE OR REPLACE FILE FORMAT UBER_DATA.PUBLIC.ff_standard_csv
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 0
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', '')
    TRIM_SPACE = TRUE
    EMPTY_FIELD_AS_NULL = TRUE;


SELECT 
    $1 AS col1, 
    $2 AS col2, 
    $3 AS col3, 
    $4 AS col4
FROM @uber_data.public.temp_staging/uber-raw-data-sep14.csv
(file_format => 'UBER_DATA.PUBLIC.ff_standard_csv')
LIMIT 10;

use role sysadmin;

-- 1. Create the table with exact naming using double quotes
CREATE OR REPLACE TABLE UBER_DATA.PUBLIC.uber_raw_data_sep14 (
    "Date/Time" TIMESTAMP_NTZ,
    Lat FLOAT,
    Lon FLOAT,
    Base VARCHAR(50)
);

-- 2. Load the data from the staging area into the new table
COPY INTO UBER_DATA.PUBLIC.uber_raw_data_sep14
FROM @uber_data.public.temp_staging/uber-raw-data-sep14.csv
FILE_FORMAT = (FORMAT_NAME = 'UBER_DATA.PUBLIC.ff_standard_csv')
ON_ERROR = 'CONTINUE';



select * from UBER_DATA.PUBLIC.uber_raw_data_sep14;

