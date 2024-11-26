import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

def calculate_mape(actual, predicted):
    """Calculate Mean Absolute Percentage Error (MAPE)."""
    return (abs(actual - predicted) / actual).mean() * 100

# Load Crypto data
predicted_data = pd.read_csv('test_predict.csv')
predicted_data['time'] = pd.to_datetime(predicted_data['time'])  # Ensure date is in datetime format

# List all currency files
currency_files = glob.glob('data/*.csv')  # Adjust the path as needed

# Dictionary to store MAPE results
mape_results = {}

for file in currency_files:
    filename = os.path.basename(file)
    currency_name = filename.split('1h')[0].lower()  # Get the currency name and convert to lowercase
    currency_data = pd.read_csv(file)
    currency_data['time'] = pd.to_datetime(currency_data['time'])  # Ensure date is in datetime format
    
    if currency_name not in predicted_data.columns:
        continue  

    # Merge currency data with predicted data on the date column
    merged_data = pd.merge(currency_data, predicted_data, on='time', suffixes=('_actual', '_predicted'))

    # Assuming the close price column for the currency is named 'close'
    if 'close' in merged_data.columns:
        # Calculate MAPE using the actual close price and the predicted price
        mape = calculate_mape(merged_data['close'], merged_data[currency_name])
        mape_results[currency_name] = mape  # Store MAPE result with currency name

        # Create a new figure for each currency
        plt.figure(figsize=(10, 5))
        plt.plot(merged_data['time'], merged_data['close'], label='Actual Price', linewidth=2)
        plt.plot(merged_data['time'], merged_data[currency_name], label='Predicted Price', linestyle='--')
        
        # Customize the plot
        plt.title(f'Actual vs Predicted Prices for {currency_name.upper()}')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Show the plot for the current currency
        plt.show()

# Print MAPE results
for currency_name, mape in mape_results.items():
    print(f"MAPE for {currency_name.upper()}: {mape:.2f}%")