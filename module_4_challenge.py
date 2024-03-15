import pandas as pd

df = pd.read_csv('Resources/client_dataset.csv')

# View the column names in the data
print(df.columns)

# Use the describe function to gather some basic statistics
df.describe()
df.head()

# Use this space to do any additional research
# and familiarize yourself with the data.
df.info()

# What three item categories had the most entries?
top_three = df['category'].value_counts().head(3)
print(top_three)

# For the category with the most entries,
# which subcategory had the most entries?
consumables_df = df[df['category'] == 'consumables']
most_common_subcategory = consumables_df['subcategory'].value_counts().idxmax()
print(most_common_subcategory)

# Which five clients had the most entries in the data?
top_clients = df['client_id'].value_counts().head(5)
print(top_clients)

# Store the client ids of those top 5 clients in a list.
top_clients_ids = top_clients.index.tolist()
print(top_clients_ids)

# How many total units (the qty column) did the
# client with the most entries order order?
most_entries_client = df['client_id'].value_counts().idxmax()
most_entries_client_df = df[df['client_id'] == most_entries_client]
total_units_ordered = most_entries_client_df['qty'].sum()
print(total_units_ordered)

###PART 2 STARTS HERE###

# Create a column that calculates the 
# subtotal for each line using the unit_price
# and the qty
df['line_subtotal'] = df['unit_price'] * df['qty']

# Display the updated dataframe with the new 'subtotal' column
df = df[['unit_price', 'qty', 'line_subtotal']]
print(df.head())

# Create a column for shipping price.
# Assume a shipping price of $7 per pound
# for orders over 50 pounds and $10 per
# pound for items 50 pounds or under.

# Define a function to calculate total weight and shipping price
def calculate_shipping(row):
    total_weight = row['qty'] * row['unit_weight']
    if total_weight > 50:
        shipping_price = total_weight * 7  # $7 per pound for orders over 50 pounds
    else:
        shipping_price = total_weight * 10  # $10 per pound for orders 50 pounds or under
    return total_weight, shipping_price

# Apply the function to create the 'total_weight' and 'shipping_price' columns
df[['total_weight', 'shipping_price']] = df.apply(calculate_shipping, axis=1)