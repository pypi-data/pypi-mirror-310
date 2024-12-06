def program(exp):
    if exp == 1:
        print('''
----------- Experiment 1 --------------

# Install PySpark
!pip install pyspark

# Create SparkSession
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[6]").appName("SparkByExamp1s.com").getOrCreate()

# Basic RDD operations
sc = spark.sparkContext
data = [10, 20, 30, 40, 50]
rdd = sc.parallelize(data)
print(rdd.count())
print(rdd.collect())
print(rdd.first())

# Take operation
from pyspark import SparkContext
sc = SparkContext.getOrCreate()
data = [10, 20, 30, 40, 50]
rdd = sc.parallelize(data)
print(rdd.take(3))

# Reduce operation
data = [5, 6, 7, 8, 9]
rdd = sc.parallelize(data)
print(rdd.reduce(lambda x, y: x + y))

reduce_rdd = sc.parallelize([1, 2, 3, 4, 5])
print(reduce_rdd.reduce(lambda x, y: x + y))

# Save as text file
save_rdd = sc.parallelize([9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 22, 33, 44, 55, 66, 77, 88])
save_rdd.saveAsTextFile('file79.txt')

save_rdd = sc.parallelize([9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 22, 33, 44, 55, 66, 77, 88], numSlices=4)
save_rdd.saveAsTextFile('file78.txt')

# Sampling
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
sample_with_replacement = rdd.takeSample(withReplacement=True, num=6, seed=42)
print("Sample with replacement:", sample_with_replacement)
sample_without_replacement = rdd.takeSample(withReplacement=False, num=6, seed=42)
print("Sample without replacement:", sample_without_replacement)
spark.stop()

# TakeOrdered operation
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
smallest_five = rdd.takeOrdered(5)
print("Smallest 5 elements:", smallest_five)
largest_five = rdd.takeOrdered(5, key=lambda x: -x)
print("Largest 5 elements:", largest_five)
spark.stop()

# Save as sequence file
rdd = spark.sparkContext.parallelize([("key1", 3), ("key2", 4), ("key3", 5), ("key4", 6)])
rdd.saveAsSequenceFile("sequence_file-2")
spark.stop()

# Read sequence file
spark.conf.set("dfs.checksum.enabled", "false")
rdd = spark.sparkContext.sequenceFile("sequence_file-2")
print(rdd.collect())

# Save as pickle file
rdd = spark.sparkContext.parallelize([("key1", 1), ("key2", 2), ("key3", 3), ("key4", 4), ("key5", 5)])
rdd.saveAsPickleFile("pickle-file10")
spark.stop()

# Read pickle file
rdd = spark.sparkContext.pickleFile("pickle-file10")
print(rdd.collect())
spark.stop()

# Count by key and value
rdd = spark.sparkContext.parallelize([("a", 1), ("b", 4), ("a", 2), ("b", 3), ("b", 4), ("a", 6), ("b", 8)])
counts_key = rdd.countByKey()
counts_value = rdd.countByValue()
print(counts_key)
print(counts_value)
spark.stop()

# Foreach
rdd = spark.sparkContext.parallelize([11, 22, 33, 44, 55])
for element in rdd.collect():
    print(f"Element: {element}")
rdd.foreach(lambda x: print(f"Element: {x}"))
spark.stop()

# Map and filter
my_rdd = sc.parallelize([11, 12, 13, 14, 15])
print(my_rdd.map(lambda x: x + 10).collect())

filter_rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(filter_rdd.filter(lambda x: x % 2 == 0).collect())

filter_rdd_2 = sc.parallelize(['Rahul', 'Swati', 'Rohan', 'Shreya', 'Priya', 'Shruthi'])
print(filter_rdd_2.filter(lambda x: x.startswith('S')).collect())

# Union and intersection
union_inp = sc.parallelize([11, 22, 33, 12, 14, 15, 16, 17, 18])
union_rdd_1 = union_inp.filter(lambda x: x % 2 == 0)
union_rdd_2 = union_inp.filter(lambda x: x % 3 == 0)
print(union_rdd_1.union(union_rdd_2).collect())

inp = sc.parallelize([10, 20, 30, 40, 50, 60, 70, 80, 90, 1, 2, 3, 4, 5, 6, 7, 8])
rdd_1 = inp.filter(lambda x: x % 2 == 0)
rdd_2 = inp.filter(lambda x: x % 3 == 0)
print(rdd_1.intersection(rdd_2).collect())

# Subtraction
inp = sc.parallelize([1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
rdd_1 = inp.filter(lambda x: x % 2 == 0)
rdd_2 = inp.filter(lambda x: x % 3 == 0)
print(rdd_1.subtract(rdd_2).collect())

# FlatMap
flatmap_rdd = sc.parallelize(["Hey there", "This is BDA Lab"])
print(flatmap_rdd.flatMap(lambda x: x.split(" ")).collect())

# Pair RDD operations
pair_rdd = sc.parallelize([(1, 'apple'), (2, 'banana'), (1, 'orange'), (2, 'grape'), (1, 'mango')])
def append_fruit(value):
    return value + " fruit"
modified_rdd = pair_rdd.mapValues(append_fruit)
print(modified_rdd.collect())

# Reduce by key
marks_rdd = sc.parallelize([('Rahul', 27), ('Swati', 29), ('Shreya', 22), ('Abhay', 29), ('Rohan', 22)])
print(marks_rdd.reduceByKey(lambda x, y: x + y).collect())

# Sort by key
marks_rdd = sc.parallelize([('Rahul', 27), ('Swati', 29), ('Shreya', 22), ('Abhay', 29), ('Rohan', 22)])
print(marks_rdd.sortByKey(ascending=True).collect())

# Group by key
marks_rdd = sc.parallelize([('Rahul', 27), ('Swati', 29), ('Shreya', 22), ('Abhay', 29), ('Rohan', 22)])
dict_rdd = marks_rdd.groupByKey().collect()
for key, value in dict_rdd:
    print(key, list(value))

# Count by key
marks_rdd = sc.parallelize([('Rahul', 25), ('Swati', 26), ('Rohan', 22), ('Rahul', 23)])
dict_rdd = marks_rdd.countByKey().items()
for key, value in dict_rdd:
    print(key, value)
''')

    elif exp == 2:
        print('''
                
    ------------ Experiment 2 -----------
                
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("Data Processing Pipeline").getOrCreate()
                
    # Read data from CSV file
    df = spark.read.csv("healthcare_dataset.csv", header=True, inferSchema=False)
    df.show()

    df.select(df['Name'], df['Age']).show(n=15)
    print("The datatype of columns is:")
    print(df.dtypes)

    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    # Define schema with StructType
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("address", StructType([
            StructField("street", StringType(), True),
            StructField("city", StringType(), True),
            StructField("zip", StringType(), True)
        ]), True)
    ])

    # Create data
    data = [
        (1, "Alice", ("123 Main St", "Springfield", "12345")),
        (2, "Bob", ("456 Elm St", "Shelbyville", "67890"))
    ]

    # Create DataFrame
    df = spark.createDataFrame(data, schema)
    df.show(truncate=False)  # Full content display
    df.show()
    print(df.dtypes)

    # Define schema with nullable and non-nullable fields
    schema_nullable = StructType([
        StructField("id", IntegerType(), True),  # Nullable field
        StructField("name", StringType(), True)  # Nullable field
    ])
    schema_non_nullable = StructType([
        StructField("id", IntegerType(), False),  # Non-nullable field
        StructField("name", StringType(), True)  # Nullable field
    ])

    # Create data with some null values
    data_nullable = [
        (1, "Alice"),
        (2, None),  # Name is None (nullable field)
        (3, "Charlie")
    ]
    data_non_nullable = [
        (1, "Alice"),
        (2, "Bob"),  # Name is not None
        (3, "Charlie")
    ]

    # Create DataFrames
    df_nullable = spark.createDataFrame(data_nullable, schema_nullable)
    df_non_nullable = spark.createDataFrame(data_non_nullable, schema_non_nullable)

    # Show results
    print("DataFrame with Nullable Field:")
    df_nullable.show()

    print("\nDataFrame with Non-Nullable Field:")
    df_non_nullable.show()

    # Read CSV file with | as separator
    df = spark.read.csv("csv_seperator_file.csv", sep='|', header=True, inferSchema=True)
    df.show()

    # Write DataFrame to CSV
    df.write.csv("processing1.csv")
    df.write.format("csv").mode('overwrite').save("/content/res")

    # Read a text file
    df2 = spark.read.text("/content/drive/MyDrive/BDA Lab/sample-1.txt")
    print(type(df2))
    df2.show(truncate=True)

    # Read JSON file into DataFrame
    json_path = "/content/sample_data/anscombe.json"
    df = spark.read.json(json_path)
    df.printSchema()

    # Read another CSV and drop columns
    df = spark.read.csv("/content/London.csv", header=True, inferSchema=True)
    cols_to_drop = ['Postal Code']
    df = df.drop(*cols_to_drop)  # Ensure reassignment after dropping
    df.show()

    # Count rows in the DataFrame
    print(df.count())

    # Select specific columns
    df.select(df["date"], df["area"]).show(n=5)

    # Filter rows based on conditions
    df.filter(df["median_salary"] == "21236").show()
    df.filter(
        (df["date"] == "1999-12-01") &
        (df["median_salary"] == "25000") &
        (df["mean_salary"] == "28555")
    ).show()

    # Order by specific columns
    df.orderBy(df["population_size"].asc(), df["area"].desc()).show(n=5, truncate=False)

    # Show data types
    print(df.dtypes)

    # Group by and perform aggregations
    df.groupBy("date").sum("population_size").show()
    df.groupBy("mean_salary").count().show(n=50)
        ''')
        
    elif exp == 3:
        print('''
    ---------- Experiment 3 ----------

    !pip install pyspark
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("sparkdataframes").getOrCreate()

    # Employee DataFrame
    data = [
        (1, "Anu", "DataAnalyst", 28000, "Ravi"),
        (2, "Balu", "Scientist", 22000, "Velu"),
        (3, "Clenie", "Manager", 35000, "Suresh"),
        (4, "Rythm", "Manager", 35000, "Ruhi"),
        (5, "Harish", "Manager", 35000, "Assan"),
        (6, "Devi", "Engineer", 3000, "Nalini")
    ]
    columns = ["Empid", "EMP_NAME", "POSITION", "SALARY", "Manager"]
    df = spark.createDataFrame(data, columns)
    df.show()
    df.printSchema()
    df.show(n=2, truncate=25)
    df.show(n=3, truncate=2)

    # Select all columns
    df.select("*").show()
    df.select(df.columns[1:4]).show(3)

    # Collect data
    datacollect = df.collect()
    print(datacollect)
    df.collect()

    # Filtering examples
    df.filter(df.Manager == "Suresh").show(truncate=False)
    df.filter(~(df.Manager == "Suresh")).show(truncate=False)
    df.filter(df.Manager != "Rythm").show()
    df.filter("Manager<>'Rythm'").show()
    df.filter((df.POSITION == "Manager") & (df.Empid == 4)).show()
    df.filter((df.POSITION == "Manager") | (df.Empid == 4)).show()

    # Filter with `isin`
    list1 = ["Nalini", "Ravi", "Velu"]
    df.filter(df.Manager.isin(list1)).show()
    list2 = ["Nalini", "Ravi"]
    df.filter(df.Manager.isin(list2)).show(truncate=3)
    df.filter(df.Manager.isin(list1) == False).show()
    df.filter(df.Manager.isin(list1) == True).show()

    # String operations
    df.filter(df.EMP_NAME.startswith("B")).show()
    df.filter(df.EMP_NAME.endswith("u")).show()
    df.filter(df.EMP_NAME.contains("h")).show()
    df.filter(df.POSITION.like("%r%")).show()

    # Sorting examples
    df.sort("EMP_NAME").show()
    df.sort("Empid", "EMP_NAME").show()
    df.orderBy("SALARY", "Empid").show()
    df.sort(df.POSITION.asc(), df.Manager.asc()).show()
    df.sort(df.POSITION.desc(), df.Manager.asc()).show()

    # Customer DataFrame
    customerdata = [
        (1, "ABi", 9089078901, "Tamilnadu", 18, 3245),
        (2, "william", 889078901, "Kerala", 28, 111),
        (3, "xavier", 789078901, "Karnataka", 38, 121),
        (4, "john", 9012078901, "Tamilnadu", 48, 123),
        (5, "chitu", 9089078934, "Andhra", 58, 111),
        (6, "saran", 9089078661, "Madya", 18, 444),
        (7, "prave", 96789000001, "Jammu", 23, 555),
        (8, "parvathy", 9089700901, "Goa", 24, 666),
        (9, "xena", 90780078901, "Punjab", 33, 777),
        (10, "Haier", 912349078901, "Srilanka", 36, 8888),
        (11, "UUII", 9089078901, "Rajasthan", 17, 9000),
        (12, "Zenith", 9089078901, "Kerala", 16, 1234),
        (13, "ABirami", 9089078901, "Uttra Pradesh", 10, 1112),
        (14, "preetha", 9089078901, "Tamilnadu", 8, 3245)
    ]
    schema = ["Id", "Name", "Phone", "state", "age", "cost"]
    df = spark.createDataFrame(data=customerdata, schema=schema)
    df.printSchema()
    df.show(truncate=False)

    # GroupBy and Aggregations
    df.groupBy("state").sum("cost").show()
    df.groupBy("state").count().show()
    df.groupBy("state").min("cost").show()
    df.groupBy("state").max("cost").show()
    df.groupBy("state").avg("cost").show()
    df.groupBy("state").mean("cost").show()
    df.groupBy("state", "age").sum("cost").show()

    # Aggregations using `agg`
    from pyspark.sql.functions import sum, avg, max, col
    df.groupBy("state").agg(sum("cost")).show()
    df.groupBy("state").agg(
        sum("cost").alias("sum_cost"),
        avg("cost").alias("avg_cost"),
        max("cost").alias("max_cost")
    ).show()

    # Other operations
    distinct_states = df.select('state').distinct().rdd.map(lambda r: r[0]).collect()
    print(distinct_states)
    df.select("age").show()
    df.describe().show()
    df.withColumnRenamed("Name", "EmpName").show()
    ''')
    
    elif exp == 4:
        print('''
        -------- Experiment 4 ---------
        
        # Install PySpark
        !pip install pyspark
        
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col, max, min, split
        import pandas as pd

        # Spark Session
        spark = SparkSession.builder.appName("Temperature").getOrCreate()
        sc = spark.sparkContext

        # Reading Weather Data from a CSV file
        lines = sc.textFile("/content/drive/MyDrive/weather.csv")
        print("Original Lines:")
        print(lines.collect())

        header = lines.first()
        print("Header:", header)

        lines = lines.filter(lambda line: line != header)
        print("Filtered Lines:")
        print(lines.collect())

        # Parsing the Data
        city_temperature = lines.map(lambda x: x.split(','))
        print("City Temperature Data:")
        print(city_temperature.collect())

        city_temp = city_temperature.map(lambda x: (x[0], x[1]))
        print("City and Temperature:")
        print(city_temp.collect())
        print("Type of city_temp:", type(city_temp))

        # Finding Max and Min Temperature
        city_max_temp = city_temperature.map(lambda x: x[1]).max()
        print("City with Max Temperature:", city_max_temp)

        city_min_temp = city_temperature.map(lambda x: x[1]).min()
        print("City with Min Temperature:", city_min_temp)

        # Using DataFrames for Max Temperature
        weather_df = spark.read.csv(
            "/content/drive/MyDrive/city_temperature.csv",
            header=True,
            inferSchema=True
        )

        # Finding Max Temperature Value
        max_temp_value = weather_df.agg(max(col("AvgTemperature"))).collect()[0][0]
        print("Max Temperature Value:", max_temp_value)

        # Getting Rows with Max Temperature
        max_temp_row = weather_df.filter(col("AvgTemperature") == max_temp_value)
        print("Row with Max Temperature:")
        max_temp_row.show()

        # Selecting Cities with Max Temperature
        max_temp_cities = max_temp_row.select("City")  # Ensure "City" column exists in your data
        print("Cities with Max Temperature:")
        max_temp_cities.show()

        # Comparing Data from Multiple File Formats
        # CSV File
        csv_df = spark.read.csv(
            "/content/drive/MyDrive/min_temerature.csv",
            header=True,
            inferSchema=True
        ).select("City", "Temperature", "Year")
        print("CSV File Data:")
        csv_df.show()

        # JSON File
        json_df = spark.read.json("/content/drive/MyDrive/method 2.json")
        json_clean_df = json_df.select("City", "Temperature", "Year").filter(col("City").isNotNull())
        print("JSON File Data:")
        json_clean_df.show()

        # Text File
        text_df = spark.read.text("/content/drive/MyDrive/method 3..txt")
        header = text_df.first()[0]
        data_df = text_df.filter(text_df["value"] != header)

        text_df1 = data_df.select(
            split(col("value"), ",")[0].alias("City"),
            split(col("value"), ",")[1].alias("Temperature"),
            split(col("value"), ",")[2].alias("Year")
        )
        print("Text File Data:")
        text_df1.show()

        # Excel File
        pandas_df = pd.read_excel("/content/drive/MyDrive/method 6.xlsx")
        xlsx_df = spark.createDataFrame(pandas_df)
        print("Excel File Data:")
        xlsx_df.show()

        # Data from a List
        list_data = [
            ("New York", 1, 2013),
            ("Los Angeles", 232, 2012),
            ("Chicago", 12, 2011)
        ]
        list_df = spark.createDataFrame(list_data, ["City", "Temperature", "Year"])
        print("List Data:")
        list_df.show()
        ''')

    elif exp == 5:
        print('''
    ---------- Experiment 5 ------------

    # Install PySpark
    !pip install pyspark

    # Import required libraries
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.functions import expr, when, col, lit
    from pyspark.sql.types import StringType

    # Initialize Spark Session with Hive Support
    spark = SparkSession.builder.appName("MySparkApp").enableHiveSupport().getOrCreate()

    # Sample Data and DataFrame
    data = [("101", "Harini", 20), ("103", "Kavi", 21), ("107", "Nala", 19)]
    columns = ["rollno", "name", "age"]
    df = spark.createDataFrame(data, columns)
    df.show()

    print(type(df))

    # Temporary View Creation
    df.createOrReplaceTempView("stud_view")
    result = spark.sql("SELECT * FROM stud_view")
    result.show()

    # Querying Temporary View
    result = spark.sql("SELECT * FROM stud_view WHERE age > 25")
    result.show()

    # Save DataFrame as a Table
    df.write.saveAsTable("stud_table")
    df.printSchema()

    # Creating a New Table from Existing Table
    spark.sql("CREATE TABLE IF NOT EXISTS new_stud_table AS SELECT * FROM stud_table")
    spark.sql("DESCRIBE new_stud_table").show()
    spark.sql("SHOW COLUMNS FROM new_stud_table").show()

    # Alter Table to Add a Column
    spark.sql("ALTER TABLE new_stud_table ADD COLUMNS (branch STRING)")
    spark.sql("DESCRIBE new_stud_table").show()

    # Insert Data into Table
    spark.sql("INSERT INTO TABLE new_stud_table VALUES ('104', 'Dharshini', 20, 'AIML'), ('105', 'Rosshini', 20, 'AIDS')")
    spark.sql("SELECT * FROM new_stud_table ORDER BY age").show()

    # Reading Data from Table
    df = spark.read.table("new_stud_table")
    df.show()

    # Add New Column with Expression
    updated_df = df.withColumn("age_plus_5", expr("age + 5"))
    updated_df.show()

    # Update Column Value
    updated_df = df.withColumn("age", expr("age + 1"))
    updated_df.show()

    # Conditional Column Addition
    updated_df = df.withColumn("is_adult", when(expr("age >= 18"), "Yes").otherwise("No"))
    updated_df.show()

    # Update Based on Condition
    update_condition = (col("name") == "Arun")
    updated_df = df.withColumn("age", when(update_condition, 25).otherwise(col("age")))
    updated_df.show()

    # Adding a New Column with Literal Value
    job_value = "Engineer"
    df_with_job = df.withColumn("job", lit(job_value))
    df_with_job.show()

    # Update Multiple Columns Based on Condition
    update_condition = (col("name").isin(["Arun", "Dharshini"]))
    job_update_expr = when(update_condition, lit("Senior ") + col("job")).otherwise(col("job"))
    age_update_expr = when(update_condition, col("age") + 5).otherwise(col("age"))
    updated_df = df_with_job.withColumn("job", job_update_expr).withColumn("age", age_update_expr)

    print("Updated DataFrame:")
    updated_df.show()

    # Cast Column Type While Updating
    update_condition = (col("name").isin(["Arun", "Balaji"]))
    job_update_expr = when(update_condition, "Senior Engr").otherwise(col("job")).cast(StringType())
    age_update_expr = when(update_condition, col("age") + 5).otherwise(col("age"))
    updated_df = df_with_job.withColumn("job", job_update_expr).withColumn("age", age_update_expr)

    print("Updated DataFrame:")
    updated_df.show()

    # Save DataFrame as Table
    updated_df.write.saveAsTable("new_table_name_3", format="parquet", mode="overwrite")

    # Filter Rows
    updated_df = updated_df.filter(df['name'] != 'Balaji')
    updated_df.show()

    # Delete Condition
    delete_condition = ((updated_df['name'] == 'Bob') | ((updated_df['age'] >= 30) | (updated_df['job'] == 'Manager')))
    filtered_df = updated_df.filter(~delete_condition)
    filtered_df.show()
    ''')
        
    elif exp == 6:
        print('''
        ------------ Experiment 6 ------------

        ###### String Operation ######

        # Install PySpark
        !pip install pyspark

        # Import required libraries
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import (
            concat_ws, length, upper, lower, base64, col, ascii, levenshtein,
            ltrim, locate, to_date, current_date, date_add, date_format, datediff,
            avg, month
        )

        # Initialize Spark Session
        spark = SparkSession.builder.appName("StringFunctionsExample").getOrCreate()

        # Sample Data and DataFrame
        data = [
            ("BMW", "Luxury", "2021"),
            ("Audi", "Sedan", "2023"),
            ("Jeep Wrangler ", "Off-Road SUV", "2023"),
            ("Nissan Leaf 3", "Electric Hatchback", "2020"),
            ("Benz-S-Class", "LuxurySedan", "2019")
        ]
        columns = ["model", "type", "year"]
        df = spark.createDataFrame(data, columns)

        # Concatenating Strings
        concatenated_df = df.withColumn("details", concat_ws(" - ", col("model"), col("type"), col("year")))
        print("1. Concatenated Strings:")
        concatenated_df.show(truncate=False)

        # Length of Strings
        length_df = df.withColumn("type_length", length(col("type")))
        print("2. Length of Type Strings:")
        length_df.show()

        # Substring of Strings
        substring_df = df.withColumn("type_abbr", col("type").substr(1, 4))
        print("3. Substring of Types:")
        substring_df.show()

        # Convert to Uppercase
        uppercase_df = df.withColumn("uppercase_type", upper(col("type")))
        print("4. Uppercase Types:")
        uppercase_df.show()

        # Convert to Lowercase
        lowercase_df = df.withColumn("lowercase_type", lower(col("type")))
        print("5. Lowercase Types:")
        lowercase_df.show()

        # Base64 Encoding
        encoded_df = df.withColumn("model_base64", base64(col("model")))
        print("6. Base64 Encoding of Model:")
        encoded_df.show()

        # ASCII Value
        ascii_df = df.withColumn("model_ascii", ascii(col("model")))
        print("7. ASCII Value of Model:")
        ascii_df.show()

        # Find Position of Substring
        position_df = df.withColumn("camry_position", locate("Camry", col("model"), 1))
        print("8. Position of 'Camry' in Model:")
        position_df.show()

        # Levenshtein Distance
        string_data = [("Mount", "sitting"), ("pink", "bluer"), ("weak", "week")]
        string_columns = ["string1", "string2"]
        string_df = spark.createDataFrame(string_data, string_columns)

        distance_df = string_df.withColumn("levenshtein_distance", levenshtein(col("string1"), col("string2")))
        print("9. Levenshtein Distance:")
        distance_df.show()

        # Trim Leading Whitespace
        trimmed_df = string_df.withColumn("string1_trimmed", ltrim(col("string1")))
        print("10. Trimmed Leading Whitespace:")
        trimmed_df.show()

        # Date Operations
        date_columns = ["ROLLNO", "NAME", "DOB"]
        date_data = [
            ("101", "Abi", "2004-10-30"), ("102", "Agalya", "2005-06-05"),
            ("103", "Abu", "2004-07-17"), ("105", "soni", "2004-05-18"),
            ("106", "suji", "2004-08-07"), ("107", "yugan", "2002-12-17"),
            ("108", "dev", "2005-04-07"), ("109", "nila", "2003-09-05"),
            ("110", "BABU", "2004-02-06")
        ]
        df = spark.createDataFrame(date_data, date_columns)
        df.show()

        # Add a Date Column
        df_with_date = df.withColumn("date_column", to_date(col("DOB"), "yyyy-MM-dd"))
        print("11. DataFrame with Date Column:")
        df_with_date.show()

        # Date Formatting
        formatted_date_df = df_with_date.withColumn("formatted_date", date_format(col("DOB"), "yyyy-MMM-dd"))
        print("12. Date Formatted Column:")
        formatted_date_df.show()

        # Calculate Age
        df_with_age = df_with_date.withColumn(
            "age", (datediff(current_date(), col("DOB")) / 365.25).cast("int")
        )
        print("13. Age Calculation:")
        df_with_age.show()

        # Average Age
        avg_age = df_with_age.agg(avg("age").alias("average_age"))
        print("14. Average Age:")
        avg_age.show()

        # Youngest and Oldest Person
        youngest_person = df_with_age.orderBy(col("age").asc()).limit(1)
        print("15. Youngest Person:")
        youngest_person.show()

        oldest_person = df_with_age.orderBy(col("age").desc()).limit(1)
        print("16. Oldest Person:")
        oldest_person.show()

        # Students Above Average Age
        avg_age_value = df_with_age.select(avg("age")).collect()[0][0]
        students_above_avg = df_with_age.filter(col("age") > avg_age_value)
        print("17. Students Above Average Age:")
        students_above_avg.show()

        # Extract Month
        df_with_month = df_with_date.withColumn("month", month(col("DOB")))
        print("18. Extract Month from DOB:")
        df_with_month.show()

        # Students Born Between January and May
        students_jan_to_may = df_with_month.filter((col("month") >= 1) & (col("month") <= 5))
        print("19. Students Born Between January and May:")
        students_jan_to_may.show()
            
    \n
    \n          
            #####  Date and Time #####
        ''')
        print('''
    !pip install pyspark 

    from pyspark.sql import SparkSession
    from pyspark.sql.functions import to_date, current_date, date_format, datediff, avg, col, month

    # Initialize Spark session
    spark = SparkSession.builder.appName("MySparkApp").config("spark.some.config.option", "config-value").getOrCreate()
    print(spark)

    # CREATING A DATAFRAME
    columns = ["ROLLNO", "NAME", "DOB"]
    data = [
        ("101", "AJAY", "2004-10-30"),
        ("102", "ASWIN", "2005-06-05"),
        ("103", "ANAS", "2004-07-17"),
        ("105", "ANIRUDH", "2004-05-18"),
        ("106", "ARAVIND", "2004-08-07"),
        ("107", "ARUN", "2002-12-17"),
        ("108", "DHARUN", "2005-04-07"),
        ("109", "KABILAN", "2003-09-05"),
        ("110", "BABU", "2004-02-06"),
    ]
    df = spark.createDataFrame(data, columns)
    df.show()

    # Add a date column in proper format
    df_with_date = df.withColumn("date_column", to_date(df["DOB"], "yyyy-MM-dd"))
    df_with_date.show()

    # Format the date in "yyyy-MMM-dd"
    df_with_date = df_with_date.select(col("DOB"), date_format(col("DOB"), "yyyy-MMM-dd").alias("formatted_date"))
    df_with_date.show()

    # 1. DISPLAY CURRENT DATE
    current_date_df = spark.range(1).select(current_date().alias("current_date"))
    current_date_df.show(truncate=False)

    # 2. PRINT THE AGE OF ALL STUDENTS (in Years)
    df_with_age = df_with_date.withColumn(
        "age", (datediff(current_date(), col("DOB")) / 365.25).cast("int")
    )
    df_with_age.show(truncate=False)

    # 3. PRINT THE AGE OF ALL STUDENTS (in Days)
    df_with_age_days = df_with_date.withColumn(
        "age_in_days", datediff(current_date(), col("DOB")).cast("int")
    )
    df_with_age_days.show(truncate=False)

    # 4. FIND THE AVERAGE AGE IN THE CLASS
    avg_age = df_with_age.agg(avg("age").alias("average_age"))
    avg_age.show()

    # 5. FIND THE YOUNGEST STUDENT IN THE CLASS
    youngest_person = df_with_age.orderBy(col("age").asc()).limit(1)
    youngest_person.show(truncate=False)

    # 6. FIND THE OLDEST STUDENT IN THE CLASS
    oldest_person = df_with_age.orderBy(col("age").desc()).limit(1)
    oldest_person.show(truncate=False)

    # 7. FIND THE STUDENT WHOSE AGE IS ABOVE AVERAGE
    average_age = avg_age.collect()[0]["average_age"]
    students_above_avg_age = df_with_age.filter(col("age") > average_age)
    students_above_avg_age.show(truncate=False)

    # 8. FIND THE STUDENT WHOSE AGE IS BELOW AVERAGE
    students_below_avg_age = df_with_age.filter(col("age") < average_age)
    students_below_avg_age.show(truncate=False)

    # 9. FIND THE STUDENTS BORN IN THE MONTH BETWEEN JANUARY AND MAY
    df_with_month = df_with_date.withColumn("month", month(col("DOB")))
    students_between_jan_may = df_with_month.filter((col("month") >= 1) & (col("month") <= 5))
    students_between_jan_may.show(truncate=False)

    # Stop Spark session
    spark.stop()
    ''')
        
    elif exp == 7:
        print('''

    ---------- Experiment 7 ----------

    !pip install pyspark

    from pyspark.sql import SparkSession

    # Step 2: Create a Spark session
    spark = SparkSession.builder.appName("PySpark_WindowFunction_Example").getOrCreate()

    # Create sample data
    simpleData = [
        ("James", "Sales", 3000),
        ("Michael", "Sales", 4600),
        ("Robert", "Sales", 4100),
        ("Maria", "Finance", 3000),
        ("James", "Sales", 3000),
        ("Scott", "Finance", 3300),
        ("Jen", "Finance", 3900),
        ("Jeff", "Marketing", 3000),
        ("Kumar", "Marketing", 2000),
        ("Saif", "Sales", 4100)
    ]

    columns = ["employee_name", "department", "salary"]
    df = spark.createDataFrame(data=simpleData, schema=columns)
    df.printSchema()
    df.show(truncate=False)

    # Import necessary functions
    from pyspark.sql.window import Window
    from pyspark.sql.functions import (
        row_number, rank, dense_rank, percent_rank, 
        cume_dist, lag, lead, col, avg, sum, min, max
    )

    # Define a Window specification
    windowSpec = Window.partitionBy("department").orderBy("salary")

    # Row number
    df.withColumn("row_number", row_number().over(windowSpec)) \
    .show(truncate=False)

    # Rank
    df.withColumn("rank", rank().over(windowSpec)) \
    .show()

    # Dense rank
    df.withColumn("dense_rank", dense_rank().over(windowSpec)) \
    .show()

    # Percent rank
    df.withColumn("percent_rank", percent_rank().over(windowSpec)) \
    .show()

    # Cumulative distribution
    df.withColumn("cume_dist", cume_dist().over(windowSpec)) \
    .show()

    # Lag
    df.withColumn("lag", lag("salary", 2).over(windowSpec)) \
    .show()

    # Lead
    df.withColumn("lead", lead("salary", 2).over(windowSpec)) \
    .show()

    # Aggregate functions with a Window specification for aggregation
    windowSpecAgg = Window.partitionBy("department")

    # Aggregations
    df.withColumn("row", row_number().over(windowSpec)) \
    .withColumn("avg", avg(col("salary")).over(windowSpecAgg)) \
    .withColumn("sum", sum(col("salary")).over(windowSpecAgg)) \
    .withColumn("min", min(col("salary")).over(windowSpecAgg)) \
    .withColumn("max", max(col("salary")).over(windowSpecAgg)) \
    .where(col("row") == 1) \
    .select("department", "row", "avg", "sum", "min", "max") \
    .show()

    # Repeated aggregation display
    df.withColumn("row", row_number().over(windowSpec)) \
    .withColumn("avg", avg(col("salary")).over(windowSpecAgg)) \
    .show()

    df.withColumn("row", row_number().over(windowSpec)) \
    .withColumn("avg", avg(col("salary")).over(windowSpecAgg)) \
    .withColumn("sum", sum(col("salary")).over(windowSpecAgg)) \
    .withColumn("min", min(col("salary")).over(windowSpecAgg)) \
    .withColumn("max", max(col("salary")).over(windowSpecAgg)) \
    .show()

''')
        
    elif exp == 8:

        print('''
        Not for Lab Experiment
''')

    elif exp == 9:
        print(''' 
    -------- Hyper Parameter Tunning ---------
        #### Logistic Regression ####

                     



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#importing data
df=pd.read_csv('/content/Churn_Modelling.csv')
df.head()
df.columns
#Droping the columns which are not usefull
df.drop(['RowNumber','CustomerId','Surname'],axis=1,inplace=True)
#Scaling the data for better outcome ->Importing Standard Scaler
#LabelEncoding on columns which have catogrical data ->Importing LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
label_encoding =LabelEncoder()
df['Gender'] =label_encoding.fit_transform(df['Gender'])
df['Geography']=label_encoding.fit_transform(df['Geography'])
df['Gender'].unique()
df['Geography'].unique()
#dividing data into Independent and Dependent data
X=df.iloc[:,:-1]
y=df.iloc[:,-1]
X.head()
y.head()
print(X.shape)
print(y.shape)
#Applying Scaling to all data we can also apply Scaling on indivisual row
Scaler=StandardScaler()
X_scale=Scaler.fit_transform(X.values)
#Train test Splits
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test =train_test_split(X_scale,y,test_size=0.3,random_state=2)
# ***LOGISTIC_REGRESSION***
#import Logistic Regression
from sklearn.linear_model import LogisticRegression
model_Lr=LogisticRegression()
#Traning & Testing
model_Lr.fit(X_train,y_train)
y_pred=model_Lr.predict(X_test)
#Accuracy
from sklearn import metrics
print("Accuracy_Score :",metrics.accuracy_score(y_test,y_pred))
print("Classification_Report :\n",metrics.classification_report(y_test,y_pred))
print('Confusion_Matrix :\n',metrics.confusion_matrix(y_test,y_pred))
#HYPER-TUNING in Logistic_Regression
Logistic regression does have not really have any critical hyperparameters to tune.

Sometime few of them are imp. which can inhace the performance

->solver in [‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’]

->penalty in [‘none’, ‘l1’, ‘l2’, ‘elasticnet’]

->C in [100, 10, 1.0, 0.1, 0.01]
C parameter controls the penality strength, which can also be effective

for all parameter of Logistic Regession :https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
#defining the parametres:
model =LogisticRegression()
solvers=['lbfgs','liblinear']
penalty=['l1','l2','elasticnet']
c_values=[1.0,0.1,0.001]
GRID_CV
grid=dict(solver=solvers,penalty=penalty,C=c_values)
grid_search =GridSearchCV(estimator=model,param_grid=grid,n_jobs=-1,cv=5,scoring='accuracy',error_score=0)
grid_result=grid_search.fit(X_train,y_train)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
Randomised Search Cv
random=dict(solver=solvers,penalty=penalty,C=c_values)
random_cv=RandomizedSearchCV(estimator=model,param_distributions=random,n_iter=5,scoring='accuracy',n_jobs=-1,random_state=1,error_score=0,cv=10)
random_result=random_cv.fit(X_train,y_train)

print("Best: %f using %s" % (random_result.best_score_, random_result.best_params_))
means = random_result.cv_results_['mean_test_score']
stds = random_result.cv_results_['std_test_score']
##Now if you get the more accuracy in hyper-tunning just copy those parameter and pass while making instance of algorithms

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#importing data
df=pd.read_csv('/content/Churn_Modelling.csv')

#Droping the columns which are not usefull
df.drop(['RowNumber','CustomerId','Surname'],axis=1,inplace=True)

#Scaling the data for better outcome ->Importing Standard Scaler
#LabelEncoding on columns which have catogrical data ->Importing LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

label_encoding =LabelEncoder()
df['Gender'] =label_encoding.fit_transform(df['Gender'])
df['Geography']=label_encoding.fit_transform(df['Geography'])

X=df.iloc[:,:-1]
y=df.iloc[:,-1]

#Applying Scaling to all data we can also apply Scaling on indivisual row
Scaler=StandardScaler()
X_scale=Scaler.fit_transform(X.values)

#Train test Splits
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test =train_test_split(X_scale,y,test_size=0.3,random_state=2)


from sklearn.linear_model import LogisticRegression
model_Lr=LogisticRegression()

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV


#defining the parametres:
model =LogisticRegression()
solvers=['lbfgs','liblinear']
penalty=['l1','l2','elasticnet']
c_values=[1.0,0.1,0.001]


grid=dict(solver=solvers,penalty=penalty,C=c_values)

grid_search =GridSearchCV(estimator=model,param_grid=grid,n_jobs=-1,cv=5,scoring='accuracy',error_score=0)

grid_result=grid_search.fit(X_train,y_train)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# Load the dataset
df = pd.read_csv('/content/Churn_Modelling.csv')

# Drop columns that are not useful
df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1, inplace=True)

# Label encode categorical columns
label_encoding = LabelEncoder()
df['Gender'] = label_encoding.fit_transform(df['Gender'])
df['Geography'] = label_encoding.fit_transform(df['Geography'])

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Scale the data
scaler = StandardScaler()
X_scale = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scale, y, test_size=0.3, random_state=2)

# Define the logistic regression model
model = LogisticRegression()

# Define the hyperparameter grid with compatible combinations
solvers = ['lbfgs', 'liblinear', 'saga']
penalty = ['l2']
c_values = [1.0, 0.1, 0.001]
grid = dict(solver=solvers, penalty=penalty, C=c_values)

# Create a grid search
grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=5, scoring='accuracy', error_score=0)

# Fit the grid search to the training data
grid_result = grid_search.fit(X_train, y_train)

# Print the best score and parameters
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']

------------------------------------------------------------------------------------------------------------------------------
   
        ##### Decision Tree ####
!pip install pyspark
from pyspark.sql import SparkSession

# Step 2: Create a Spark session
spark = SparkSession.builder.appName("Example").getOrCreate()
filepath="/content/houseprice.csv"
df=spark.read.format('csv').options(header='true',inferSchema='true',delimiter=';').load(filepath);
df.show(5,truncate=False)
df.printSchema()
print(type(df))
df1=spark.read.csv(filepath,header=True)
# slelct columns
df1.show()
print(type(df1))
df1.select("country","price").show(5)
from pyspark.sql import types as t
from pyspark.sql import functions as f

cdf1=df1.withColumn("price",f.when(f.col("price") > 600000 ,"high").otherwise("low"))
print(type(cdf1))

cdf1.show(5)
cdf1.select("country","price").show(5)
cdf1.groupBy("price").count().show()

from pyspark.sql.types import IntegerType,StringType

#train_df1 = cdf1.withColumn("price", train_df1["price"].cast(StringType()))
cdf1=cdf1.withColumn("bathrooms", cdf1["bathrooms"].cast(IntegerType()))
cdf1=cdf1.withColumn("bedrooms", cdf1["bedrooms"].cast(IntegerType()))
cdf1= cdf1.withColumn("sqft_living", cdf1["sqft_living"].cast(IntegerType()))
cdf1=cdf1.withColumn("sqft_lot",cdf1["sqft_lot"].cast(IntegerType()))
cdf1 = cdf1.withColumn("floors", cdf1["floors"].cast(IntegerType()))
cdf1=cdf1.withColumn("sqft_basement", cdf1["sqft_basement"].cast(IntegerType()))
cdf1.printSchema();
(train_df1, test_df1) = cdf1.randomSplit([0.8, 0.2], 11)
print("Number of train samples: " + str(train_df1.count()))
print("Number of test samples: " + str(test_df1.count()))
# StringIndexer
feature from PySpark's Machine Learning (ML) library.

Specifically, it's used for converting a categorical column with string values into a numerical format.
Input and Output Columns: You specify two columns:

inputCol: This is the name of the column you want to convert from string values to numerical indices. In your code, it's "price."
outputCol: This is the name of the new column where the numerical indices will be stored. In your code, it's "price_index."
#Label Encoding
#Label Encoding is a technique that is used to convert categorical columns into numerical ones
#so that they can be fitted by machine learning models which only take numerical data

from pyspark.ml.feature import StringIndexer

#label encoding of categorical values
price_indexer = StringIndexer(inputCol="price", outputCol="price_index")
#It computes the mapping of distinct string values
#in the "price" column to unique numerical indices
price_indexed_df1 = price_indexer.fit(train_df1);
print(price_indexed_df1)



from pyspark.ml.feature import VectorAssembler

# DecisionTreeClassifier is used for classiication problems
from pyspark.ml.classification import DecisionTreeClassifier

# Convert features into vector
inputCols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot','floors', 'sqft_basement']
outputCol = "features"
#create a VectorAssembler object
# to transform the specified input columns into a single feature vector column

vector_assembler = VectorAssembler(inputCols = inputCols, outputCol = outputCol)
train_df1 = vector_assembler.transform(train_df1)
train_df1.show(5)

# Select feature vector and label
modeling_df = train_df1.select(['features', 'price_index'])

# Create DecisionTreeClassifier model
dt_model = DecisionTreeClassifier(labelCol="price_index", featuresCol="features")

# Train model with Training Data
dt_model = dt_model.fit(modeling_df)

# Do predictions on train data
predictions = dt_model.transform(modeling_df)
predictions.show(20, truncate=False)

from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluatorDT = MulticlassClassificationEvaluator(labelCol="price_index")

# Define a grid of hyperparameters
param_grid = (ParamGridBuilder()
              .addGrid(lr.regParam, [0.01, 0.1, 1.0])
              .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
              .build())

#Label Encoding
#Label Encoding is a technique that is used to convert categorical columns into numerical ones
#so that they can be fitted by machine learning models which only take numerical data

from pyspark.ml.feature import StringIndexer

#label encoding of categorical values
price_indexer = StringIndexer(inputCol="price", outputCol="price_index")
price_indexed_df1 = price_indexer.fit(test_df1);
test_df1=price_indexed_df1.transform(test_df1);
test_df1.show();
test_df1.printSchema();
# On Test data - Transform test data using all the transformers and estimators in the same order
test_df1 = vector_assembler.transform(test_df1)
test_predictions = dt_model.transform(test_df1)
test_predictions.show(20, truncate=False)

area_under_curve = evaluatorDT.evaluate(test_predictions)
area_under_curve
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
import pyspark.sql.functions as F
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Initialize SparkSession
spark = SparkSession.builder.appName("HousePriceClassification").getOrCreate()

# Load data
filepath = "/content/houseprice.csv"
df = spark.read.csv(filepath, header=True, inferSchema=True)

# Preprocess data
# Convert "price" column to numeric based on condition
df = df.withColumn("price", F.when(F.col("price") > 600000, 1).otherwise(0).cast(IntegerType()))

# Cast selected columns to IntegerType
int_columns = ['bathrooms', 'bedrooms', 'sqft_living', 'sqft_lot', 'floors', 'sqft_basement']
for col_name in int_columns:
    df = df.withColumn(col_name, df[col_name].cast(IntegerType()))

# Split data
train_df, test_df = df.randomSplit([0.8, 0.2], seed=11)

# Label encoding
price_indexer = StringIndexer(inputCol="price", outputCol="price_index")
train_df = price_indexer.fit(train_df).transform(train_df)

# Feature vector assembly
input_cols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'sqft_basement']
vector_assembler = VectorAssembler(inputCols=input_cols, outputCol="features")
train_df = vector_assembler.transform(train_df)

# Create and train Decision Tree Classifier model
dt_model = DecisionTreeClassifier(labelCol="price_index", featuresCol="features")
dt_model = dt_model.fit(train_df)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="price_index")

# Transform and predict on test data
test_df = test_df.withColumn("price", F.when(F.col("price") > 600000, 1).otherwise(0).cast(IntegerType()))
test_df = price_indexer.fit(test_df).transform(test_df)
test_df = vector_assembler.transform(test_df)
test_predictions = dt_model.transform(test_df)

# Display evaluation results
area_under_curve = evaluator.evaluate(test_predictions)
print(f"Area under ROC curve: {area_under_curve}")

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.sql.types import IntegerType
import pyspark.sql.functions as F

# Initialize SparkSession
spark = SparkSession.builder.appName("YourAppName").getOrCreate()

# Read data from CSV
filepath = "/content/houseprice.csv"
df1 = spark.read.csv(filepath, header=True)

# Convert "price" column to numeric based on condition and cast to IntegerType
df1 = df1.withColumn("price", when(F.col("price") > 600000, 1).otherwise(0).cast(IntegerType()))

# Define input columns and output column for VectorAssembler
inputColumns = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'sqft_basement']
outputColumn = "features"

# Cast the selected input columns to IntegerType
for col_name in inputColumns:
    df1 = df1.withColumn(col_name, df1[col_name].cast(IntegerType()))

# Create a StringIndexer for "price" column
price_indexer = StringIndexer(inputCol="price", outputCol="priceIndex")

# Create a VectorAssembler for input features
vector_assembler = VectorAssembler(inputCols=inputColumns, outputCol=outputColumn)

# Create a DecisionTreeClassifier
dt_model = DecisionTreeClassifier(labelCol="price", featuresCol=outputColumn)

# Define the pipeline stages
stages = [price_indexer, vector_assembler, dt_model]

# Create a pipeline
pipeline = Pipeline(stages=stages)

# Split data into train and test
(train_df2, test_df2) = df1.randomSplit([0.8, 0.2], seed=11)

# Fit the pipeline on the training data
final_pipeline = pipeline.fit(train_df2)

# Make predictions on the test data
test_predictions_from_pipeline = final_pipeline.transform(test_df2)

# Show the first 5 rows of predictions
test_predictions_from_pipeline.select("price", "prediction").show(5)

# Evaluate the model and perform further analysis as needed

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Evaluate the model using accuracy (or other appropriate metric for multi-class classification)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Define the evaluator
evaluator = MulticlassClassificationEvaluator(labelCol="price", predictionCol="prediction", metricName="accuracy")

# Calculate the accuracy
accuracy = evaluator.evaluate(test_predictions_from_pipeline)
print(f"Accuracy: {accuracy}")


from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from sklearn.metrics import classification_report

# Calculate accuracy
evaluator = MulticlassClassificationEvaluator(labelCol="price", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(test_predictions_from_pipeline)

# Convert the PySpark DataFrame to a Pandas DataFrame
test_predictions_pd = test_predictions_from_pipeline.select("price", "prediction").toPandas()

# Get the true labels and predicted labels as lists
true_labels = test_predictions_pd["price"].tolist()
predicted_labels = test_predictions_pd["prediction"].tolist()

# Generate the classification report
report = classification_report(true_labels, predicted_labels)

# Print the classification report
print(report)
                 
''')
        