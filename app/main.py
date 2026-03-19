from agent import DatabaseAgent
import duckdb
import argparse
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import os

def main(log=print, **kargs):
    db_path = kargs.get("db_path", None)
    conn = duckdb.connect(db_path)
    special_columns = [{"table":"customers", "col": "loyalty_tier"},{"table":"orders", "col": "status"}]
    agent = DatabaseAgent(conn, special_columns=special_columns, log=log)
    question = kargs.get("question", None)
    if question is None:
        log("No question provided. Exiting.")
        return
    response = agent(question)
    log("Agent response:")
    log(response)
    if response["success"]:
        print(response["text"])
        if response["presentation_type"] == "TABLE" and (response.get("chart", None) is not None):
            print("Saving and displaying chart...")
            fig, ax = response["chart"]
            fig.savefig(f"output/chart_{kargs['start_datetime']}.png")  # Save the figure to a file
            plt.show()
        return 0
            
    else: 
        error_text = f"Encountered an error of type {response.get('error type', 'UNKNOWN')}: {response.get('error text', 'No error text provided.')}"
        log(error_text)
        print(error_text)
        return 1

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str)
    args = parser.parse_args()
    args = vars(args)  # convert Namespace to dict
    # For development, you can hardcode the database path here or pass it as an argument
    args["db_path"] = 'data/jaffle_shop.duckdb'
    os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists
    os.makedirs("output", exist_ok=True)  # Ensure output directory exists
    logger = logging.getLogger("my-logger")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    start_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    handler_file = logging.FileHandler(f"logs/log_{start_datetime}.log", mode='w') # and log to file
    args["start_datetime"] = start_datetime
    handler_file.setLevel(logging.DEBUG)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)
    main(log=logger.debug, **args)
    
