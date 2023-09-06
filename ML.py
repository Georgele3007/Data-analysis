import pandas as pd

df = pd.read_csv('vgsales.csv')

df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# Check for missing values
print(df.isnull().sum())

import sqlite3

# Create an SQLite in-memory database
conn = sqlite3.connect(':memory:')

# Store the DataFrame in the database
df.to_sql('sales', conn, index=False)

# Perform SQL aggregation
query = """
SELECT strftime('%Y', Year) AS SalesYear, SUM(Global_Sales) AS TotalSales
FROM sales
GROUP BY SalesYear
ORDER BY SalesYear;
"""

# Fetch the results into a new DataFrame
sales_df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

import matplotlib.pyplot as plt

# Set the SalesYear column as the index
sales_df.set_index('SalesYear', inplace=True)

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(sales_df.index, sales_df['TotalSales'], marker='o', linestyle='-', color='b')
plt.title('Global Video Game Sales Over Time')
plt.xlabel('Year')
plt.ylabel('Total Sales (in millions)')
plt.grid(True)
plt.show()