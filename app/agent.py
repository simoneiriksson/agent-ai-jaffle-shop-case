from db import get_connection, get_schema_summary, execute_query, get_special_columns_content, is_safe_select
from prompts import build_sql_prompt, build_df_presentation_prompt, build_text_from_dataextract_prompt
from prompts import build_presentation_type_prompt, build_chart_prompt
from openai import OpenAI
import os
import json
from prompts import build_chart_prompt, CHART_SCHEMA
from plots import build_plot
import matplotlib.pyplot as plt
import pandas as pd

class DatabaseAgent():
    def __init__(self, conn, log=print, special_columns=None):
        self.conn = conn
        self.log = log
        api_key=os.environ.get("OPENAI_API_KEY", None)
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        if special_columns:
            self.special_columns = self.get_special_columns_content(special_columns)  
        else: self.special_columns = None

        self.get_schema_summary()

    def get_llm_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content

    def get_llm_response_jsonschema(self, prompt, json_schema):
        response = self.client.responses.create(
            model="gpt-4o",
            input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "json_response",
                        "strict": True,
                        "schema": json_schema
                    }
                }
        )
        try:
            output_dict = json.loads(response.output_text.strip())
        except json.JSONDecodeError as e:
            self.log(f"Error decoding JSON response: {e}")
            self.log(f"Raw response was: {response}")
            raise e
        return output_dict


    def get_schema_summary(self):
        self.schema_summary = get_schema_summary(self.conn)
        return self.schema_summary
    
    def get_special_columns_content(self, special_columns):
        self.special_columns = get_special_columns_content(self.conn, special_columns)
        return self.special_columns

    def sql_query(self, question):
        prompt = build_sql_prompt(question, self.schema_summary, self.special_columns)
        sql_query = self.get_llm_response(prompt)
        if sql_query.upper().startswith("AMBIGUOUS"):
            self.log(f"Generated SQL query is ambiguous. returning: {sql_query}")
            return {"success": False, "error type": "AMBIGUOUS", "error text": sql_query}

        if sql_query.upper().startswith("UNANSWERABLE"):
            self.log(f"Generated SQL query is unanswerable. returning: {sql_query}")
            return {"success": False, "error type": "UNANSWERABLE", "error text": sql_query}

        if not is_safe_select(sql_query):
            self.log("Generated SQL query is not a safe SELECT statement.")
            return {"success": False, "error type": "UNSAFE", "error text": sql_query}

        self.log(f"Generated SQL:\n{sql_query}")

        try:
            query_result = execute_query(sql_query, self.conn)
        except Exception as e:
            self.log(f"Error executing SQL query: {e}")
            return {"success": False, "error type":"SQL ERROR", "error text": f"Error executing SQL query: {e}"}
        
        return {"success": True, "sql_query": sql_query, "query_result": query_result}

    def __call__(self, question):
        self.log(f"Received question: {question}")
        sql_response_dict = self.sql_query(question)
        if not sql_response_dict["success"]:
            return sql_response_dict
        self.log("SQL query executed successfully. Processing results...")

        sql_query = sql_response_dict["sql_query"]
        query_result = sql_response_dict["query_result"]
        result_columns_and_DT_dict = {col: str(dtype) for col, dtype in zip(query_result.columns, query_result.dtypes)}
        presentation_type_prompt = build_presentation_type_prompt(question, self.schema_summary, sql_query, query_result.head())
        self.log(f"Presentation type prompt:\n{presentation_type_prompt}")
        presentation_type = self.get_llm_response(presentation_type_prompt)
        self.log(f"Determined presentation type: {presentation_type}")        
        
        if presentation_type == "PRESENTATION: TEXT":
            to_text_prompt = build_text_from_dataextract_prompt(question, self.schema_summary, sql_query, query_result.head())
            text_output = self.get_llm_response(to_text_prompt)
            self.log("Text Output:", text_output)   
            return {"success": True, "presentation_type": "TEXT", "text": text_output}
        
        elif presentation_type == "PRESENTATION: TABLE":
            df_presentation_prompt = build_df_presentation_prompt(question, self.schema_summary, sql_query, query_result.head())
            df_intro_text = self.get_llm_response(df_presentation_prompt)
            text_output = f"{df_intro_text}\n\n{query_result.to_string(index=False)}"
            self.log("Table Output:")
            self.log(text_output)
            chart_prompt = build_chart_prompt(question=question, sql=sql_query, columns=result_columns_and_DT_dict, preview_rows=query_result.head())
            chart_response_dict = self.get_llm_response_jsonschema(chart_prompt, json_schema=CHART_SCHEMA)
            fig, ax = build_plot(chart_response_dict, query_result, log=self.log)
            return {"success": True, 
                    "presentation_type": "TABLE", 
                    "text": text_output, 
                    "dataframe": query_result, 
                    "chart": (fig, ax)}



