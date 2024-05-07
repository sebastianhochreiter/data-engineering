# Importing necessary libraries
import os
import bs4
import pandas as pd
from io import StringIO
import calendar

def extract_daily_statistics(html_content, year, month):
    """
    Extracts daily statistics and adds 'Year' and 'Month' columns.
    
    Args:
        html_content (str): HTML content of the page.
        year (int): The year for which statistics are being extracted.
        month (int): The month for which statistics are being extracted.
        
    Returns:
        DataFrame: DataFrame containing the extracted statistics.
    """
    # Parsing HTML content
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    # Finding the table with daily statistics for the given year and month
    th_element = soup.find('th', string=f"Daily Statistics for {calendar.month_name[month]} {year}")
    if th_element:
        print(f"TH element found for {calendar.month_name[month]} {year}.")
        # Finding the parent table of the TH element
        table = th_element.find_parent('table')
        if table:
            print(f"Table found for {calendar.month_name[month]} {year}.")
            # Converting the table to HTML string and reading it into a DataFrame
            html_str = str(table)
            df = pd.read_html(StringIO(html_str))[0]

            # Correcting column names to capture only the first column of each data point
            df.columns = ['Day', 'Hits', 'Hits2', 'Files', 'Files2', 'Pages', 'Pages2', 'Visits', 'Visits2', 'Sites', 'Sites2', 'KBytes', 'KBytes2']
            df = df[['Day', 'Hits', 'Files', 'Pages', 'Visits', 'Sites', 'KBytes']]  # Selecting necessary columns

            # Adding 'Year' and 'Month' columns
            df.insert(0, 'Year', year)
            df.insert(1, 'Month', month)

            # Removing rows where only 'Year' and 'Month' have data
            df = df[df[['Hits', 'Files', 'Pages', 'Visits', 'Sites', 'KBytes']].notnull().any(axis=1)]

            return df
    print(f"No statistics found for {calendar.month_name[month]} {year}.")
    return None

# Directory containing the HTML files
html_directory = ''

# Absolute path to the directory
current_folder = os.path.dirname(os.path.abspath(__file__))
html_directory_path = os.path.join(current_folder, html_directory)

# DataFrame for all statistics
all_stats_df = pd.DataFrame()

# Iterating over years and months
for year in range(2015, 2025):
    for month in range(1, 13 if year < 2024 else 6):
        html_filename = f'usage_{year}{month:02d}.html'
        html_filepath = os.path.join(html_directory_path, html_filename)

        # Checking if the file exists before opening it
        if os.path.exists(html_filepath):
            print(f"File {html_filepath} exists.")
            # Reading HTML content from the file
            with open(html_filepath, 'r') as file:
                content = file.read()

            # Extracting daily statistics
            df_daily_stats = extract_daily_statistics(content, year, month)

            if df_daily_stats is not None:
                # Adding the current DataFrame to all statistics
                all_stats_df = pd.concat([all_stats_df, df_daily_stats], ignore_index=True)
        else:
            print(f"File {html_filepath} does not exist.")

# Saving all statistics to a CSV file
output_csv_path = os.path.join(current_folder, 'all_daily_statistics.csv')
all_stats_df.to_csv(output_csv_path, index=False, float_format='%.0f')

print(f"All daily statistics successfully extracted and saved in CSV format at {output_csv_path}.")
