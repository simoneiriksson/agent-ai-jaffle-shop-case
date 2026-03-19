import pandas as pd

HUMAN_COLUMN_NAMES = {
    # customers
    "customer_id": "Customer ID",
    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "Email",
    "loyalty_tier": "Loyalty Tier",
    "created_at": "Created At",

    # order_items
    "order_item_id": "Order Item ID",
    "order_id": "Order ID",
    "product_id": "Product ID",
    "quantity": "Quantity",
    "unit_price": "Unit Price",
    "line_total": "Line Total",

    # orders
    "order_date": "Order Date",
    "status": "Order Status",
    "total_amount": "Total Amount",
    "order_channel": "Order Channel",

    # products
    "product_name": "Product Name",
    "category": "Product Category",
    "price": "Price",
    "description": "Description",
}

def humanize_column_name(col: str) -> str:
    col = str(col).strip()
    if col in HUMAN_COLUMN_NAMES:
        return HUMAN_COLUMN_NAMES[col]

    # fallback for unknown columns, e.g. total_revenue -> Total Revenue
    return col.replace("_", " ").strip().title()

def rename_columns_human(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [humanize_column_name(col) for col in df.columns]
    return df