import pandas as pd
from sklearn.linear_model import LinearRegression

# Helper function to convert volume strings to numerical values
def convert_volume(volume_str):
    if 'M' in volume_str:
        return float(volume_str.replace('M', '')) * 1e6
    return float(volume_str)

# Create a DataFrame with 5 days of data (open, close, high, low, volume)
data = {
    'Day1_Open': [37.46], 'Day1_Close': [35.33], 'Day1_High': [37.50], 'Day1_Low': [35.33], 'Day1_Volume': [convert_volume('14.556M')],
    'Day2_Open': [35.63], 'Day2_Close': [34.72], 'Day2_High': [36.35], 'Day2_Low': [34.01], 'Day2_Volume': [convert_volume('6.012M')],
    'Day3_Open': [35.27], 'Day3_Close': [35.39], 'Day3_High': [36.00], 'Day3_Low': [34.55], 'Day3_Volume': [convert_volume('7.317M')],
    'Day4_Open': [35.47], 'Day4_Close': [35.55], 'Day4_High': [36.70], 'Day4_Low': [35.01], 'Day4_Volume': [convert_volume('10.047M')],
    'Day5_Open': [35.34], 'Day5_Close': [35.22], 'Day5_High': [36.19], 'Day5_Low': [34.75], 'Day5_Volume': [convert_volume('4.202M')]
}

df = pd.DataFrame(data)

# Labels for Day 6 (what we want to predict) - Adjusted to match the scale of the data
labels = {
    'Day6_Open': [35.50],
    'Day6_Close': [35.70],
    'Day6_High': [36.50],
    'Day6_Low': [35.10]
}

labels_df = pd.DataFrame(labels)

print("Training data:")
print(df)
print("\nLabels (Day 6 data to predict):")
print(labels_df)

# Prepare the features (Day 1 - Day 4) and labels (Day 5)
X = df[['Day1_Open', 'Day1_Close', 'Day1_High', 'Day1_Low', 'Day1_Volume',
        'Day2_Open', 'Day2_Close', 'Day2_High', 'Day2_Low', 'Day2_Volume',
        'Day3_Open', 'Day3_Close', 'Day3_High', 'Day3_Low', 'Day3_Volume',
        'Day4_Open', 'Day4_Close', 'Day4_High', 'Day4_Low', 'Day4_Volume']]

y = labels_df[['Day6_Open', 'Day6_Close', 'Day6_High', 'Day6_Low']]

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model on the training data (using all data)
model.fit(X, y)

# Since we don't have any additional data for testing, we'll predict using the same input
predictions = model.predict(X)

print("\nPredicted Day 6 values (Open, Close, High, Low):")
print(predictions)


# You can pass in the latest 5 days' data to predict the 6th day
new_data = pd.DataFrame({
    'Day1_Open': [115], 'Day1_Close': [118], 'Day1_High': [119], 'Day1_Low': [114], 'Day1_Volume': [1900],
    'Day2_Open': [113], 'Day2_Close': [115], 'Day2_High': [116], 'Day2_Low': [112], 'Day2_Volume': [1800],
    'Day3_Open': [110], 'Day3_Close': [113], 'Day3_High': [114], 'Day3_Low': [109], 'Day3_Volume': [1700],
    'Day4_Open': [108], 'Day4_Close': [110], 'Day4_High': [111], 'Day4_Low': [107], 'Day4_Volume': [1600],
    'Day5_Open': [105], 'Day5_Close': [108], 'Day5_High': [110], 'Day5_Low': [104], 'Day5_Volume': [1500]
})

# Predict Day 6
day_6_prediction = model.predict(new_data)
print(f"Predicted Day 6 values: {day_6_prediction}")
