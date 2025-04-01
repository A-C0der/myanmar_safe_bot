import json as jr
import pandas as pd

with open("mdy_resuce_data.json", "r") as mdr:
    data = jr.load(mdr)

# Convert JSON data into a DataFrame
df = pd.DataFrame(data)

# Print each row in the desired format
for index, row in df.iterrows():
    print(f"Name: {row.get('name', 'N/A')}, Location: {row.get('location', 'N/A')}, Phone: {row.get('phone', 'N/A')}")
