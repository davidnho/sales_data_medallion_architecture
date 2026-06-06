import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

# PRODUCTS

products = []

for i in range(1,101):

    products.append({
        "product_id": i,
        "product_name": f"Product_{i}",
        "category": np.random.choice(
            ["Electronics","Furniture","Clothing"]
        ),
        "price": round(
            np.random.uniform(10,500),
            2
        )
    })

pd.DataFrame(products).to_csv(
    "data/products.csv",
    index=False
)

# CUSTOMERS

customers = []

for i in range(1,301):

    customers.append({
        "customer_id": i,
        "customer_name": fake.name(),
        "city": fake.city(),
        "country": fake.country()
    })

pd.DataFrame(customers).to_csv(
    "data/customers.csv",
    index=False
)

# SALES

sales = []

for i in range(1,1001):

    qty = np.random.randint(1,10)

    sales.append({
        "sale_id": i,
        "customer_id": np.random.randint(1,301),
        "product_id": np.random.randint(1,101),
        "quantity": qty,
        "sale_date": fake.date_between(
            start_date="-1y",
            end_date="today"
        )
    })

pd.DataFrame(sales).to_csv(
    "data/sales.csv",
    index=False
)

print("Data Generated")