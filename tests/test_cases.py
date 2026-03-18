TEST_CASES = [
    {
        "id": "tc_01",
        "question": "How many orders do we have in total?",
        "category": "answerable",
        "expected_behavior": "Returns a single total count of orders.",
        "expected_sql_contains": ["count", "from"],
        "notes": "Basic sanity check. Should be the easiest case."
    },
    {
        "id": "tc_02",
        "question": "How many completed orders do we have?",
        "category": "answerable",
        "expected_behavior": "Counts only orders with completed status.",
        "expected_sql_contains": ["count", "where", "status"],
        "notes": "Tests filtering logic."
    },
    {
        "id": "tc_03",
        "question": "What were the top 5 products by revenue?",
        "category": "answerable",
        "expected_behavior": "Ranks products by total revenue and returns 5 rows.",
        "expected_sql_contains": ["sum", "group by", "order by", "limit 5"],
        "notes": "Tests join + aggregation + ranking."
    },
    {
        "id": "tc_04",
        "question": "Who are our top 10 customers by total spend?",
        "category": "answerable",
        "expected_behavior": "Ranks customers by total revenue across their orders.",
        "expected_sql_contains": ["sum", "group by", "order by", "limit 10"],
        "notes": "Tests multi-table join and customer-level aggregation."
    },
    {
        "id": "tc_05",
        "question": "How many completed orders did we have by month?",
        "category": "answerable",
        "expected_behavior": "Returns monthly grouped counts for completed orders.",
        "expected_sql_contains": ["group by", "date", "count"],
        "notes": "Tests time grouping."
    },
    {
        "id": "tc_06",
        "question": "Who are our best customers?",
        "category": "ambiguous",
        "expected_behavior": "Returns AMBIGUOUS and asks what best means.",
        "expected_sql_contains": [],
        "notes": "Best could mean revenue, order count, or average order value."
    },
    {
        "id": "tc_07",
        "question": "What are our best-selling products?",
        "category": "ambiguous",
        "expected_behavior": "Returns AMBIGUOUS and asks whether best-selling means quantity sold, revenue, or number of orders.",
        "expected_sql_contains": [],
        "notes": "Important business ambiguity case."
    },
    {
        "id": "tc_08",
        "question": "Which products have the highest profit margin?",
        "category": "unanswerable",
        "expected_behavior": "Returns UNANSWERABLE because profit/cost data is not available.",
        "expected_sql_contains": [],
        "notes": "Tests whether the model avoids inventing missing business data."
    },
]