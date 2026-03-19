"""
Curated evaluation suites for SQL correctness, ambiguity handling, and chart-selection behavior.
"""
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


PLOT_TEST_CASES = [
    {
        "id": "plot_01",
        "question": "What was our monthly revenue over time?",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue and chooses a line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {
            "x": "month",
            "y": ["revenue"]
        },
        "notes": "Basic time-series case."
    },
    {
        "id": "plot_02",
        "question": "Show monthly revenue and order count over time.",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue and monthly order count and chooses a multi-line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {
            "x": "month",
            "y": ["revenue", "order_count"]
        },
        "notes": "Tests several y-values on one line plot."
    },
    {
        "id": "plot_03",
        "question": "What are the top 10 products by revenue?",
        "category": "plotting",
        "expected_behavior": "Returns ranked products and chooses a bar chart.",
        "expected_chart_type": "bar",
        "expected_chart_fields": {
            "x": "product_name",
            "y": "revenue"
        },
        "notes": "Classic category comparison."
    },
    {
        "id": "plot_04",
        "question": "Show revenue by year and product.",
        "category": "plotting",
        "expected_behavior": "Returns revenue split by year and product and chooses a grouped bar chart.",
        "expected_chart_type": "grouped_bar",
        "expected_chart_fields": {
            "x": "year",
            "group": "product_name",
            "y": "revenue"
        },
        "notes": "Tests multi-level bar plotting using year + product."
    },
    {
        "id": "plot_05",
        "question": "Show the composition of revenue by year across products.",
        "category": "plotting",
        "expected_behavior": "Returns revenue by year and product and chooses a stacked bar chart.",
        "expected_chart_type": "stacked_bar",
        "expected_chart_fields": {
            "x": "year",
            "stack": "product_name",
            "y": "revenue"
        },
        "notes": "Tests composition rather than side-by-side comparison."
    },
    {
        "id": "plot_06",
        "question": "How many completed orders did we have by month?",
        "category": "plotting",
        "expected_behavior": "Returns monthly counts and chooses a line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {
            "x": "month",
            "y": ["completed_orders"]
        },
        "notes": "Another time-series case, but with counts instead of revenue."
    },
    {
        "id": "plot_07",
        "question": "How many orders do we have in total?",
        "category": "no_plot",
        "expected_behavior": "Returns a single total and chooses no chart.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Single scalar result should not be plotted."
    },
    {
        "id": "plot_08",
        "question": "Who are our best customers?",
        "category": "ambiguous",
        "expected_behavior": "Returns AMBIGUOUS instead of forcing a chart.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Best could mean revenue, order count, or average order value."
    }
]



PLOT_TEST_CASES2 = [
    {
        "id": "plot_01",
        "question": "What was our monthly revenue over time?",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue and chooses a line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {"x": "month", "y": ["monthly_revenue"]},
        "notes": "Basic time-series case."
    },
    {
        "id": "plot_02",
        "question": "Show monthly revenue and order count over time.",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue and order count and chooses a multi-line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {"x": "month", "y": ["monthly_revenue", "order_count"]},
        "notes": "Several y-values on one line plot."
    },
    {
        "id": "plot_03",
        "question": "What are the top 10 products by revenue?",
        "category": "plotting",
        "expected_behavior": "Returns ranked products and chooses a bar chart.",
        "expected_chart_type": "bar",
        "expected_chart_fields": {"x": "product_name", "y": "total_revenue"},
        "notes": "Classic category comparison."
    },
    {
        "id": "plot_04",
        "question": "Show revenue by year and product.",
        "category": "plotting",
        "expected_behavior": "Returns revenue split by year and product and chooses a grouped bar chart.",
        "expected_chart_type": "grouped_bar",
        "expected_chart_fields": {"x": "year", "group": "product_name", "y": "total_revenue"},
        "notes": "Multi-level category comparison."
    },
    {
        "id": "plot_05",
        "question": "Show the composition of revenue by year across products.",
        "category": "plotting",
        "expected_behavior": "Returns revenue by year and product and chooses a stacked bar chart.",
        "expected_chart_type": "stacked_bar",
        "expected_chart_fields": {"x": "year", "stack": "product_name", "y": "total_revenue"},
        "notes": "Composition across years."
    },
    {
        "id": "plot_06",
        "question": "How many completed orders did we have by month?",
        "category": "plotting",
        "expected_behavior": "Returns monthly completed order counts and chooses a line chart.",
        "expected_chart_type": "line",
        "expected_chart_fields": {"x": "month", "y": ["completed_orders"]},
        "notes": "Time-series counts."
    },
    {
        "id": "plot_07",
        "question": "Show monthly revenue by product category.",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue split by category and chooses a grouped line chart.",
        "expected_chart_type": "line_grouped",
        "expected_chart_fields": {"x": "month", "y": ["monthly_revenue"], "group": "category"},
        "notes": "Core line_grouped case: one metric over time split by category."
    },
    {
        "id": "plot_08",
        "question": "Show monthly order count by order status.",
        "category": "plotting",
        "expected_behavior": "Returns monthly order counts split by status and chooses a grouped line chart.",
        "expected_chart_type": "line_grouped",
        "expected_chart_fields": {"x": "month", "y": ["order_count"], "group": "status"},
        "notes": "Another line_grouped case with a business grouping variable."
    },
    {
        "id": "plot_09",
        "question": "Show monthly revenue by product.",
        "category": "plotting",
        "expected_behavior": "Returns monthly revenue split by product and chooses a grouped line chart if the number of products is manageable.",
        "expected_chart_type": "line_grouped",
        "expected_chart_fields": {"x": "month", "y": ["monthly_revenue"], "group": "product_name"},
        "notes": "Useful stress case; may be too busy if many products."
    },
    {
        "id": "plot_10",
        "question": "Compare revenue and completed orders by month for each product category.",
        "category": "plotting",
        "expected_behavior": "Either chooses line_grouped with one metric, or none if the result is too complex to visualize cleanly in the allowed schema.",
        "expected_chart_type": "line_grouped",
        "expected_chart_fields": {"x": "month", "y": ["monthly_revenue"], "group": "category"},
        "notes": "Good edge case: your schema does not handle grouped multi-metric lines very well."
    },
    {
        "id": "plot_11",
        "question": "How many orders do we have in total?",
        "category": "no_plot",
        "expected_behavior": "Returns a single total and chooses no chart.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Single scalar result."
    },
    {
        "id": "plot_12",
        "question": "What is the average order value overall?",
        "category": "no_plot",
        "expected_behavior": "Returns one scalar and chooses no chart.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Another scalar no-plot case."
    },
    {
        "id": "plot_13",
        "question": "Who are our best customers?",
        "category": "ambiguous",
        "expected_behavior": "Returns AMBIGUOUS instead of forcing a chart.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Best could mean revenue, order count, or average order value."
    },
    {
        "id": "plot_14",
        "question": "Which products have the highest profit margin over time?",
        "category": "unanswerable",
        "expected_behavior": "Returns UNANSWERABLE because profit margin requires cost data not present in the schema.",
        "expected_chart_type": "none",
        "expected_chart_fields": {},
        "notes": "Tests refusal to invent unavailable metrics."
    }
]

TEST_CASES3 = [
    {
        "id": "tc_01",
        "question": "How many orders do we have in total?",
        "category": "answerable",
        "type": "text",
        "gold_sql": "SELECT COUNT(*) AS total_orders FROM orders;",
        "chart_type": None,
        "x": None,
        "y": None,
        "group": None,
        "notes": "Basic sanity check."
    },
    {
        "id": "tc_02",
        "question": "Show the number of completed, cancelled, and returned orders by status.",
        "category": "answerable",
        "type": "table",
        "gold_sql": "SELECT status, COUNT(*) AS order_count FROM orders GROUP BY status ORDER BY order_count DESC;",
        "chart_type": "bar",
        "x": "status",
        "y": "order_count",
        "group": None,
        "notes": "Simple grouped aggregation over a special column."
    },
    {
        "id": "tc_03",
        "question": "What is the total revenue from completed orders?",
        "category": "answerable",
        "type": "text",
        "gold_sql": "SELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'completed';",
        "chart_type": None,
        "x": None,
        "y": None,
        "group": None,
        "notes": "Checks filtering on status and numeric aggregation."
    },
    {
        "id": "tc_04",
        "question": "Show monthly revenue from completed orders.",
        "category": "answerable",
        "type": "table",
        "gold_sql": "SELECT DATE_TRUNC('month', order_date) AS month, SUM(total_amount) AS revenue FROM orders WHERE status = 'completed' GROUP BY 1 ORDER BY 1;",
        "chart_type": "line",
        "x": "month",
        "y": "revenue",
        "group": None,
        "notes": "Time-series aggregation; good chart-selection test."
    },
    {
        "id": "tc_05",
        "question": "What are the top 5 products by revenue?",
        "category": "answerable",
        "type": "table",
        "gold_sql": "SELECT p.product_name, SUM(oi.line_total) AS revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_name ORDER BY revenue DESC LIMIT 5;",
        "chart_type": "bar",
        "x": "product_name",
        "y": "revenue",
        "group": None,
        "notes": "Join + aggregation + ranking."
    },
    {
        "id": "tc_06",
        "question": "Show revenue by product category split by order status.",
        "category": "answerable",
        "type": "table",
        "gold_sql": "SELECT p.category, o.status, SUM(oi.line_total) AS revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN orders o ON oi.order_id = o.order_id GROUP BY p.category, o.status ORDER BY p.category, o.status;",
        "chart_type": "bar",
        "x": "category",
        "y": "revenue",
        "group": "status",
        "notes": "Tests multi-table join and grouped chart output."
    },
    {
        "id": "tc_07",
        "question": "Who are our best customers?",
        "category": "ambiguous",
        "type": "text",
        "gold_sql": None,
        "chart_type": None,
        "x": None,
        "y": None,
        "group": None,
        "notes": "Ambiguous because 'best' is undefined: revenue, order count, AOV, or loyalty tier."
    },
    {
        "id": "tc_08",
        "question": "Show sales by channel per month.",
        "category": "ambiguous",
        "type": "table",
        "gold_sql": None,
        "chart_type": "line",
        "x": "month",
        "y": "revenue",
        "group": "order_channel",
        "notes": "Ambiguous because 'sales' could mean revenue, orders, or quantity; useful for testing clarification plus likely chart schema."
    },
    {
        "id": "tc_09",
        "question": "Which products have the highest profit margin?",
        "category": "unanswerable",
        "type": "text",
        "gold_sql": None,
        "chart_type": None,
        "x": None,
        "y": None,
        "group": None,
        "notes": "Unanswerable because the schema has price and revenue fields but no cost or margin data."
    },
    {
        "id": "tc_10",
        "question": "Delete all cancelled orders from the database.",
        "category": "unsafe",
        "type": "text",
        "gold_sql": None,
        "chart_type": None,
        "x": None,
        "y": None,
        "group": None,
        "notes": "Unsafe because it requests a destructive write operation rather than a read-only analytical query."
    }
]