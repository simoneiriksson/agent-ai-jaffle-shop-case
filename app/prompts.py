import pandas as pd
def build_sql_prompt_bck(question, schema_context):
    prompt = f"""You are an expert data analyst who writes SQL queries to answer questions about a database. 
    The database schema is as follows:
{schema_context}
Write a SQL query to answer the following question:
{question}
Only write the SQL query, without any explanation."""
    return prompt


def build_sql_prompt(question: str, schema_context: str, special_columns=None) -> str:
    prompt = f"""
        You are an expert data analyst who writes SQL queries to answer questions about a database. 
        The question may contain information about plotting preferences, but you should ignore that for this prompt and focus only on writing a SQL query to answer the question.
        The database schema is as follows:
        Schema:
        {schema_context}"""
    
    if special_columns:
        prompt += f"""
            Some columns have special semantics:
            {special_columns}
            """
    prompt += f"""

            Instructions:
        - Use only the tables and columns listed above
        - Do not include id-columns in the output.
        - Return a single SELECT query only
        - Do not use markdown
        - If ambiguous, return: AMBIGUOUS: <question>
        - If unanswerable, return: UNANSWERABLE: <reason>

        User question:
        {question}
        """.strip()
    return prompt


# def build_presentation_type_prompt(question: str, schema_context: str, sql_query: str, db_extract: pd.DataFrame) -> str:
#     prompt = f"""
#         You are a data analyst, and you have just executed the following SQL query against a DuckDB database.

#         Instructions:
#         - evaluate if the pandas DataFrame extract from the SQL query is best presented as a text answer or a table
#         - If the DataFrame has 1 row and 1 column, return: PRESENTATION: TEXT
#         - If the DataFrame has more than 1 row or more than 1 column, return: PRESENTATION: TABLE

#         Schema:
#         {schema_context}

#         User question:
#         {question}

#         SQL query:
#         {sql_query}

#         SQL result: 
#         {db_extract.head(n=20).to_string(index=False)}
#         """.strip()
#     return prompt

# def build_df_presentation_prompt_bck(question: str, schema_context: str, sql_query: str, db_extract: pd.DataFrame) -> str:
#     prompt = f"""
#     You are a data analyst, and you have just executed the following SQL query against a DuckDB database.
#     Instructions:
#         - write a very short introductory text to present the data in the DataFrame, based on the user question and the SQL query 
#         - the introductory text should contain a brief non-techical summary any methodological choices you made in writing the SQL query, such as how you interpreted ambiguous aspects of the question, and any assumptions you made.
#         - do not include information from the table 
#         - the data will be presented in a dataframe after the text
#         User question:
#         {question}

#         SQL query:
#         {sql_query}
#     """.strip()
#     return prompt



def build_presentation_prompt_df(question: str, schema_context: str, sql_query: str, db_extract: pd.DataFrame) -> str:
    prompt = f"""
    You are a data analyst, and you have just executed the following SQL query against a DuckDB database.
    Instructions:
        - write a short introductory text to present the data in the DataFrame, based on the user question and the SQL query 
        - the data will be presented in a dataframe after the text
        - Do not use any type of markup (e.g. markdown, html, etc.) in your response. Return plain text only.
        The text should have three sections:
        BRIEF: <one sentence non-technical description of the results. It should focus on explaining the numbers in the DataFrame.>
        IN-DEPTH: <2-4 sentences non-technical summary of the results, focussing on any interesting patterns, trends, or outliers in the data. It should focus on explaining the numbers in the DataFrame.>
        METHODOLOGY: <brief non-technical summary of any methodological choices, assumptions, or interpretations you made in writing the SQL query>

        User question:
        {question}

        SQL query:
        {sql_query}

        DataFrame:
        {db_extract.to_string(index=False)}

    """.strip()
    return prompt


def build_presentation_prompt_short(question: str, schema_context: str, sql_query: str, db_extract: pd.DataFrame) -> str:
    prompt = f"""
        You are a data analyst, and you have just executed the following SQL query against a DuckDB database.

        Instructions:
        - write a short text answer to the user question based on the SQL query and its result.
        - the text should contain a brief non-techical  summary any methodological choices you made in writing the SQL query, such as how you interpreted ambiguous aspects of the question, and any assumptions you made.
        
        BRIEF: <one sentence non-technical description of the results. It should focus on explaining the numbers in the DataFrame.>
        METHODOLOGY: <brief non-technical summary of any methodological choices, assumptions, or interpretations you made in writing the SQL query>

        Schema:
        {schema_context}

        User question:
        {question}

        SQL query:
        {sql_query}

        SQL result: 
        {db_extract.to_string(index=False)}
        """.strip()
    return prompt


def build_chart_prompt(question: str, sql: str, columns: list[dict], preview_rows: pd.DataFrame) -> str:
    return f"""
You are choosing a chart specification for a pandas DataFrame result.

Your task:
Select the best chart type for the result and return a JSON object only.

Allowed chart types:
- "none"
- "line"
- "line_grouped"
- "bar"
- "grouped_bar"
- "stacked_bar"

Chart rules:
- Use "none" if the result is not meaningfully chartable.
- Use "line" for ordered or time-like x values, with one or more numeric y series.
- Use "line_grouped" for line charts with a grouping variable to split into multiple lines.
- Use "bar" for one categorical x and one numeric y.
- Use "grouped_bar" for one primary x, one grouping column, and one numeric y.
- Use "stacked_bar" for one primary x, one grouping column, and one numeric y.
- Only use columns that appear in the provided DataFrame schema.
- Do not invent columns.
- Do not return code.
- Do not return markdown.
- Return valid JSON only.
- Return only the JSON, without any explanation or additional text.
- Your response must begin with '{' and end with '}'.

JSON schema:
{{
  "chart_type": "none | line | line_grouped | bar | grouped_bar | stacked_bar",
  "x": "string or null",
  "y": "string, array of strings, or null",
  "group": "string or null",
  "title": "string",
  "xlabel": "string",
  "ylabel": "string",
  "reason": "string"
}}

Additional constraints:
- For "line": x must be a single column, y must be an array of one or more numeric columns.
- For "line_grouped": x must be a single column, y must be an array of one or more numeric columns, group must be a single column.
- For "bar": x must be a single column, y must be a single numeric column.
- For "grouped_bar": x must be a single column, group must be a single column, y must be a single numeric column.
- For "stacked_bar": x must be a single column, group must be a single column, y must be a single numeric column.
- For "none": set x, y, group, and stack to null.

User question:
{question}

SQL used to produce the result:
{sql}

DataFrame columns and dtypes:
{columns}

Preview rows:
{preview_rows.to_string(index=False)}
""".strip()


CHART_SCHEMA = {
    "type": "object",
    "properties": {
        "chart_type": {
            "type": "string",
            "enum": ["none", "line", "line_grouped", "bar", "grouped_bar", "stacked_bar"]
        },
        "x": {
            "anyOf": [{"type": "string"}, {"type": "null"}]
        },
        "y": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
                {"type": "null"}
            ]
        },
        "group": {
            "anyOf": [{"type": "string"}, {"type": "null"}]
        },
        "title": {"type": "string"},
        "xlabel": {"type": "string"},
        "ylabel": {"type": "string"},
        "reason": {"type": "string"}
    },
    "required": ["chart_type", "x", "y", "group", "title", "xlabel", "ylabel", "reason"],
    "additionalProperties": False
}