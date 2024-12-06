
from datetime import timedelta, datetime
from datetime import datetime
from pyspark.sql import Window
from pyspark.sql import functions as f
from pyspark.sql.types import *
import pandas as pd
import sys

__version__ = '0.0.8'
class spark_functions():
    def __init__(self, spark=None, health_table_name = None) -> None:
        self.spark = spark
        self.health_table_name = health_table_name
    def sample_function(self):
        print("Sample is working")
        pass

    def get_top_duplicates(self,df,col='customer_hash',n=2):
        return (df.groupBy(col)
                .agg(f.count(col).alias('count'))
                .orderBy(f.col('count').desc_nulls_last())
                .limit(n))

    def sdf_to_dwh(self,sdf,table_address,mode,mergeSchema = "true"):
        (sdf.write.mode(mode)
            .option("mergeSchema", mergeSchema)
            .saveAsTable(table_address))

    def sdf_fillDown(self,sdf,groupCol,orderCol,cols_to_fill):   
        window_spec = Window.partitionBy(groupCol).orderBy(orderCol)
        
        for column in cols_to_fill:
            # sdf = sdf.withColumn(column, f.last(f.col(column),ignorenulls=True).over(window))
            sdf = (sdf
                .withColumn(column,
                            f.last(column, ignorenulls=True).over(window_spec))
                )
        return sdf
    
    def sdf_fillUp(self,sdf,groupCol,orderCol,cols_to_fill):
        window_spec = Window.partitionBy(groupCol).orderBy(f.col(orderCol).desc_nulls_last())
        
        for column in cols_to_fill:
            # sdf = sdf.withColumn(column, f.last(f.col(column),ignorenulls=True).over(window))
            sdf = (sdf
                .withColumn(column,
                            f.last(column, ignorenulls=True).over(window_spec))
                )
        return sdf
    
    def sdf_fill_gaps(self,sdf,groupCol,orderCol,cols_to_fill,direction='both'):
        if direction == 'up':
            sdf = self.sdf_fillUp(sdf,groupCol,orderCol,cols_to_fill)
        elif direction == 'down':
            sdf = self.sdf_fillDown(sdf,groupCol,orderCol,cols_to_fill)
        else:
            sdf = self.sdf_fillDown(sdf,groupCol,orderCol,cols_to_fill)
            sdf = self.sdf_fillUp(sdf,groupCol,orderCol,cols_to_fill)
        return sdf
    
    def single_value_expr(partition_col, order_col, value_col, ascending=False):
        windowSpec = Window.partitionBy(partition_col).orderBy(order_col)
        if ascending:
            return f.first(f.when(f.col(order_col) == f.min(order_col).over(windowSpec), f.col(value_col)), True)
        else:
            return f.first(f.when(f.col(order_col) == f.max(order_col).over(windowSpec), f.col(value_col)), True)

    def read_dwh_table(self,table_name, last_update_column=None, save_health=True):
        sdf = self.spark.table(table_name)
        if save_health:
            try:
                last_update = sdf\
                                .filter(
                                f.col(last_update_column).cast('timestamp') < \
                                    (datetime.today()+timedelta(days=1)).strftime('%Y-%m-%d'))\
                                .select(f.max(f.col(last_update_column).cast('timestamp')).alias('last_update'))\
                                .collect()[0]['last_update']
                health_data = {'table_name': [table_name], 'last_update': [last_update]}
                health_sdf =  self.spark.createDataFrame(pd.DataFrame(data=health_data))
                self.sdf_to_dwh(health_sdf,self.health_table_name,'append')
            except: 
                pass
        return (sdf)

    def remove_duplicates_keep_latest(self,sdf, partition_col: str, order_col: str):
        """
        Removes duplicate rows based on the partition_col, keeping only the row with the highest value in order_col.

        Parameters:
        - df (DataFrame): The Spark DataFrame to process.
        - partition_col (str): The name of the column to partition the data (e.g., 'customer_hash').
        - order_col (str): The name of the column to order data within each partition (e.g., 'created_at').

        Returns:
        - DataFrame: A new DataFrame with duplicates removed based on partition_col, keeping only the latest record based on order_col.
        """
        # Define the window specification
        windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).desc_nulls_last())

        # Rank rows within each partition and filter to keep only the top-ranked row
        filtered_df = sdf.withColumn("row_number", f.row_number().over(windowSpec)) \
                        .filter(f.col("row_number") == 1) \
                        .drop("row_number")

        return filtered_df
    def remove_duplicates(self,sdf, partition_col: str, order_col: str, ascending = False):
        """
        Removes duplicate rows based on the partition_col, keeping only the row with the single value in order_col. 
        Ordering will beased on ascending variable.

        Parameters:
        - df (DataFrame): The Spark DataFrame to process.
        - partition_col (str): The name of the column to partition the data (e.g., 'customer_hash').
        - order_col (str): The name of the column to order data within each partition (e.g., 'created_at').
        - ascending (int): 1 means ascending order, 0 means descending order

        Returns:
        - DataFrame: A new DataFrame with duplicates removed based on partition_col, keeping only the latest record based on order_col.
        """
        # Define the window specification
        if ascending:
            windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).asc_nulls_last())
        else:
            windowSpec = Window.partitionBy(partition_col).orderBy(f.col(order_col).desc_nulls_last())

        # Rank rows within each partition and filter to keep only the top-ranked row
        filtered_df = sdf.withColumn("row_number", f.row_number().over(windowSpec)) \
                        .filter(f.col("row_number") == 1) \
                        .drop("row_number")

        return filtered_df
    
    def attribute_applications(
        applications_sdf, 
        attribution_sdf,
        attribution_columns,
        application_date_col, 
        attribution_date_col, 
        attribution_window_days = 60, 
        attribution_method='first_touch'
    ):
        """
        Perform attribution of applications to an attribution table based on specified criteria.

        Parameters:
        ----------
        applications_sdf : pyspark.sql.DataFrame
            The DataFrame containing application data.
        attribution_sdf : pyspark.sql.DataFrame
            The DataFrame containing attribution data.
        application_date_col : str
            Column name in `applications_sdf` representing the application date.
        attribution_date_col : str
            Column name in `attribution_sdf` representing the attribution date.
        attribution_window : int, optional (default=60)
            The maximum number of days allowed between application and attribution.
        attribution_method : str, optional (default='first_touch')
            The type of attribution ('first_touch' or 'last_touch').

        Returns:
        -------
        pyspark.sql.DataFrame
            Applications DataFrame with attributed data merged.
        """
        # Step 1: Filter and slim down the applications DataFrame to necessary columns
        applications_slim = applications_sdf.select(*attribution_columns, application_date_col)
        
        # Step 2: Join applications with attribution data and calculate time differences
        joined_df = (
            applications_slim
            .join(attribution_sdf, on=attribution_columns, how='left')
            .withColumn(
                'time_difference_seconds',
                (f.unix_timestamp(f.col(attribution_date_col)) - 
                f.unix_timestamp(f.col(application_date_col)))
            )
            # Filter records to stay within the attribution window and ensure no negative differences
            .filter((f.col('time_difference_seconds') >= 0) & 
                    (f.col('time_difference_seconds') <= attribution_window_days * 24 * 60 * 60))
            .drop('time_difference_seconds')
        )

        # Step 3: Determine sort order for deduplication based on attribution method
        order_ascending = False if attribution_method == 'last_touch' else True

        # Step 4: Deduplicate to retain only the best attribution for each application
        deduplicated_attributions = self.remove_duplicates(
            sdf=joined_df, 
            partition_col=attribution_columns, 
            order_col=attribution_date_col, 
            ascending=order_ascending
        )

        # Step 5: Identify applications that could not be attributed
        unattributed_applications = (
            applications_slim
            .join(deduplicated_attributions, on=attribution_columns, how='left_anti')
        )

        # Step 6: Combine attributed and unattributed applications
        combined_applications = (
            deduplicated_attributions
            .unionByName(unattributed_applications, allowMissingColumns=True)
            .drop(application_date_col, attribution_date_col)
        )

        # Step 7: Merge the combined results back into the original applications DataFrame
        final_applications = applications_sdf.join(combined_applications, on=attribution_columns, how='left')

        return final_applications

    
    