
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def clean_cell_content(cell):
    """
    Clean and combine multiple elements within a table cell.
    Returns a single string with all text content combined.
    """
    # Get all text elements, including those in nested tags
    text_elements = [text.strip() for text in cell.stripped_strings]
    # Combine elements with a space between them
    return ' '.join(filter(None, text_elements))

def scrape_cdc_tables():
    # URL of the CDC page
    url = "https://www.cdc.gov/infection-control/hcp/isolation-precautions/appendix-a-type-duration.html"
    
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all tables in the page
        tables = soup.find_all('table')
        
        # List to store all dataframes
        dfs = []
        
        # Process each table
        for i, table in enumerate(tables):
            # Get headers
            headers = []
            header_row = table.find('thead') or table.find('tr')
            if header_row:
                headers = [clean_cell_content(th) for th in header_row.find_all(['th', 'td'])]
            
            # Get rows
            rows = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                # Process each cell in the row
                row_data = [clean_cell_content(cell) for cell in row.find_all(['td', 'th'])]
                if row_data:  # Only add non-empty rows
                    rows.append(row_data)
            
            # Create DataFrame
            if rows:
                if not headers:
                    # If no headers found, use default column names
                    df = pd.DataFrame(rows)
                else:
                    # Ensure the number of headers matches the number of columns
                    max_cols = max(len(row) for row in rows)
                    headers = headers[:max_cols]  # Truncate if too many headers
                    # Extend headers if too few
                    while len(headers) < max_cols:
                        headers.append(f'Column_{len(headers)+1}')
                    df = pd.DataFrame(rows, columns=headers)
                
                # Add table identifier
                df['Table_Number'] = f'Table_{i+1}'
                
                # Clean up the DataFrame
                df = df.replace({np.nan: '', None: ''})
                
                dfs.append(df)
        
        if not dfs:
            print("No tables found on the page")
            return None
            
        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Save to CSV
        combined_df.to_csv('infection_data.csv', index=False)
        
        print(f"Successfully scraped {len(dfs)} tables and saved to 'infection_data.csv'")
        return combined_df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print("Starting CDC table scraping...")
    result = scrape_cdc_tables()
    if result is not None:
        print("\nFirst few rows of the combined data:")
        print(result.head())
        print("\nColumns in the combined data:")
        print(result.columns.tolist())