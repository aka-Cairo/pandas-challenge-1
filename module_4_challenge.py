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

df['total_weight'] = df.apply(lambda row: row['qty'] * row['unit_weight'], axis=1)
df['shipping_price'] = df.apply(lambda row: row['total_weight'] * 7 if row['total_weight'] > 50 else row['total_weight'] * 10, axis=1)

# Display the updated dataframe with the new columns
df[['unit_price', 'unit_weight', 'qty', 'total_weight', 'shipping_price']].head(3)

# Create a column for the total price
# using the subtotal and the shipping price
# along with a sales tax of 9.25%
df['line_price'] = df.apply(lambda row: round((row['line_subtotal'] + row['shipping_price']) * 1.0925, 2), axis=1)
df[['line_subtotal', 'shipping_price', 'line_price']].head(3)

# Create a column for the cost
# of each line using unit cost, qty, and
# shipping price (assume the shipping cost
# is exactly what is charged to the client).
df['line_cost'] = df.apply(lambda row: row['unit_cost'] * row['qty'] + row['shipping_price'], axis=1)
df.head(3)

# Create a column for the profit of
# each line using line cost and line price
df['line_profit'] = df.apply(lambda row: row['line_price'] - row['line_cost'], axis=1)
df.head(3)

# Check your work using the totals above
# Group the DataFrame by order_id and sum the line prices for each order
order_totals = df.groupby('order_id')['line_price'].sum()

# Filter the order_totals Series to include only the requested orders
requested_orders = [2742071, 2173913, 6128929]
requested_totals = order_totals.loc[requested_orders]

# Display the calculated total prices for the orders with dollar signs and rounded to two decimals
for order_id, total_price in requested_totals.items():
    formatted_total = f"${total_price:,.2f}"
    print(f"Order {order_id} total: {formatted_total}")

# How much did each of the top 5 clients by quantity
# spend? Check your work from Part 1 for client ids.

# Recall the top 5 clients' IDs from Part 1
top_clients_ids = [33615, 66037, 46820, 38378, 24741]

# Filter the DataFrame to include transactions made by the top 5 clients
top_clients_transactions = df[df['client_id'].isin(top_clients_ids)]

# Calculate total spending for each of the top 5 clients
total_spending_per_client = top_clients_transactions.groupby('client_id')['line_price'].sum()

# Display how much each of the top 5 clients spent
for client_id, spending in total_spending_per_client.items():
    formatted_spending = f"${spending:.2f}"
    print(f"Client {client_id} spent: {formatted_spending}")

# Create a summary DataFrame showing the totals for the
# for the top 5 clients with the following information:
# total units purchased, total shipping price,
# total revenue, and total profit. Sort by total profit.

# Group top_clients_transactions by 'client_id' and calculate requested metrics
summary_df = top_clients_transactions.groupby('client_id').agg(
    qty=('qty', 'sum'),
    shipping_price=('shipping_price', 'sum'),
    line_price=('line_price', 'sum'),
    line_cost=('line_cost', 'sum'),
    line_profit=('line_profit', 'sum')
)

# Sort the summary DataFrame by total profit
summary_df = summary_df.sort_values(by='line_profit', ascending=False)

# Display the summary DataFrame
summary_df = summary_df.reset_index() #just added this to match the provided output data
summary_df

# Format the data and rename the columns
# to names suitable for presentation.
# Currency should be in millions of dollars.

# Convert relevant columns to millions of dollars
summary_df['shipping_price'] /= 1_000_000
summary_df['line_price'] /= 1_000_000
summary_df['line_cost'] /= 1_000_000
summary_df['line_profit'] /= 1_000_000

# Format the values to have $#.##M format
summary_df['shipping_price'] = summary_df['shipping_price'].apply(lambda x: f"${x:.2f}M")
summary_df['line_price'] = summary_df['line_price'].apply(lambda x: f"${x:.2f}M")
summary_df['line_cost'] = summary_df['line_cost'].apply(lambda x: f"${x:.2f}M")
summary_df['line_profit'] = summary_df['line_profit'].apply(lambda x: f"${x:.2f}M")

# Rename the columns for clarity
summary_df.columns = ['Client ID', 'Units', 'Shipping', 'Total Revenue', 'Total Cost', 'Total Profit']

# Display the formatted summary DataFrame
summary_df

