# 1. Project Requirements
## Step 1 - Load The Original Dataset
You have a set of data. The dataset includes tables store, product, inventory, sales and calendar. These are the tables from operational databases.
![image](https://github.com/RoshnaKU/weclouddata-bootcamp-exercises/assets/125311073/fabfe515-4ac6-4345-986c-791ccdb0ac34)
You need to download the dataset from this [link](https://s3.amazonaws.com/weclouddata/data/walmart%20raw%20data.zip) and load the data into a schema of the Snowflake data warehouse. (It is easier to load the csv files from DBeaver)

You can use this [script](https://s3.amazonaws.com/weclouddata/data/data/build_os_db.sql) to build the schema for the original system dataset tables.

## Step 2 - Read and Understand the Business Requirements and data model
We have create the data model. You need to populate the data from the original schema to the data model schema.

First of all, The data model has **3 dimensions : store, date, product.**

For the fact table, we need **2 fact tables:**

***Daily fact table***: On the daily level, the row grain is date + store + product. In the daily fact table, in addition to the existing columns from the sales and inventory tables, in the fact table we need one more column called "low_stock_flg". This flag is True when sales_qty in the sales table lower than the stock_on_hand_qty in the inventory at that date.
***Weekly fact table***: We need the second fact table on weekly base. This week table contains all the aggregate values from the daily fact table and also includes some new columns:
eop_stock_on_hand_qty: This is the on hand stock qty at the end of week (Saturday), which means the on hand stock qty of the last day in the week. So you can't simply aggregate it.
eop_stock_on_order_qty: This is the on order stock qty at the end of week (Saturday).
out_of_stock_times: During one week, how many times when the out_of_stock_flg is True.
in_of_stock_times: During one week, how many times when the in_of_stock_flg is True.
low_stock_times: During one week, how many times when the low_stock_flg is True.
So to wrap up, the data model of the project has 3 dimension tables and 2 fact tables (one for daily, one for weekly). The data model can be found from here.


## Step 3 - Create data model in Snowflake schema and Populate data in the data model for the first time.
Create a schema on Snowflake.
Create physical data model tables in the schema.
Create ETL script to populate data from the original dataset to the data model.
Be aware of your ETL scripts, make sure they are also available for the later Delta data loading.

## Step 4 - Update the original dataset with the following scripts.
**Update FACT raw tables**

      INSERT INTO walmart.SALES
      VALUES
      (302836,540260,3220,'2012-12-31',18,37.80,3.58,129.42,0.01,300.72,-150.37,5.47),
      (312076,399912,3220,'2013-01-01',7,29.00,145.45,3773.59,0.02,3486.71,731.32,17.85),
      (337584,135665,1104,'2013-01-02',18,11.00,41.32,447.09,0.09,365.40,89.03,8.66);


      INSERT INTO walmart.INVENTORY
      VALUES
      ('2012-12-31',1103,540260,26.46,75.60,1,0.00,'FALSE','2012-12-31'),
      ('2012-12-31',1103,904715,27.09,21.07,0,1.00,'FALSE','2012-12-31'),
      ('2013-01-01',1104,135665,11.00,14.30,1,0.00,'FALSE','2012-12-31'),
      ('2013-01-01',1104,200147,6.72,5.88,0,0.00,'TRUE','2012-12-31'),
      ('2013-01-02',1104,399912,7.83,46.98,1,1.00,'TRUE','2012-12-31');

**Update DIM table product**
      UPDATE walmart.PRODUCT SET PROD_NAME='CHANGE-1' WHERE PROD_KEY=657768;
      UPDATE walmart.PRODUCT SET PROD_NAME='CHANGE-2' WHERE PROD_KEY=293693;
      INSERT INTO walmart.PRODUCT VALUES (999999,'ADD-1',2.22, 88.88, 'brand-999', 1, 'active', 4, 'category-4', 1, 'subcategory-1');
      
## Step 5 - Check if the raw data has been updated.

## Step 6 - Run script again to load data from the original dataset to the data model tables. Check the result sample with the following queries:

      SELECT min(cal_Dt), MAX(cal_dt) FROM walmart_anl.sales_inv_store_dy;
      SELECT * FROM walmart_anl.product_dim WHERE PROD_KEY=657768;

