import pandas as pd
sales = pd.read_csv(
"../data/sales.csv"
)
print("Sales loaded")
print(sales.head())