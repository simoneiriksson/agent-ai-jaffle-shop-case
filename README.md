# Jaffle Shop Database AI-agent

This repo showcase an AI agent that allows non-technical users to query the Jaffle Shop with business questions in natural language. 

The agent uses API-calls to OpenAI GPT-4.1 for SQL generation, and chart selection, and requires an API-key to OpenAI (see below).

# Repository overview
The repository has the following structure:
```
pyne-ai-case/
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   ├── agent.py
│   ├── db.py
│   ├── eval.ipynb
│   ├── eval.py
│   ├── explore.ipynb
│   ├── main.py
│   ├── plots.py
│   ├── presentation.ipynb
│   ├── prompts.py
│   └── utils.py
└── data/
    └── jaffle_shop.duckdb
```
There are two notebooks in the repository: `presentation.ipynb` and `eval.ipynb`. The presentation notebook gives a walk-through of the agent class and show the intermediate steps and outputs. The evaluation notebook contains a simple evaluation script, as explained below.

The core agent code is placed in the class `DatabaseAgent` in `agent.py`. The main method in this class is the `__call__` class that runs a question through the agent. 
Prompt definitions are found in `prompts.py`, and the plotting functionality is in `plots.py`

# Setup
In order to run the agent, you should first create a local environment, then activate it and finally install the prerequisite packages. You do this with the following series of commands:
```
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```

The API-key can either be set as an environment variable with the command
`
OPENAI_API_KEY=<key>
` or you can add a `.env` in the root of this repo with the line.

# How to run
The agent can be run from the command line with commands of the form: 
```
python app/main.py --question "Show monthly revenue from completed orders." 
``` 
Note that the tool only takes one argument at present.

This command creates a logging folder (`logs`) and an output folder (`output`) and prints the resulting answer. If the query result in a plot, it is put in the output folder. The log contains records of the question and intermediate results.

There is also a notebook, which walks through the agents steps, and show the intermediate outputs.


# Additional capability
In addition to executing the SQL-query and writing a small report, the agent also attempts to make a plot of the data, if relevant. The approach is safety-first. Rather than allowing the LLM to provide Python code for execution on the local machine (which for some reason Andrew Ng is really excited about), I have opted for a strategy where the LLM is asked to return a restricted JSON, which contains the parameters necessary for making the plot.   

# Architecture
The agent is implemented as a `DatabaseAgent` class, and is build around the workflow in this diagram: 


````
0 Question
1    └─> SQL prompt 
2        └─> LLM query for SQL statement
3            └─> Safety check 
4                └─> SQL execution 
5                    ├─> Answer formatting prompt
6                    │   └─> LLM query for text output
7                    └─> LLM query for chart type and setup
8                        └─> Optional chart generation
````

1) First, the user question is wrapped in a prompt.
2) The prompt is then sent to the LLM with a request for an SQL statement.
3) The SQL-statement is run through a safety check.
4) Then the SQL is run against the database to output a Pandas Dataframe
5) The Dataframe is then wrapped in a prompt, together with the original question and the SQL-statement, in order for the LLM to generate a natural language explanation of the output, together with some methodological considerations. If the Dataframe has only one row, the prompt will ask for a presentation of the content of that single row. Otherwise, the prompt will ask for a presentation of the Dataframe, and then the agent will include the Dataframe in the ouput.  
6) The natural language prompt is then passed to the LLM
7) Another prompt is generated, which wraps the Dataframe, SQL-query, and question and asks which type of plot is most suitable (if any).
8) A plot is made if relevant.


# Prompting approach
There are a total of three prompts generated for this agent.
### Question → SQL
The first prompt takes the user question, the DB schema context and information about special column such as `customers.loyalty_tier`, and `orders.status` as inputs to build a prompt that asks for an SQL-query that matches the question and the DB-schema. It instructs the LLM to 
- Use only the tables and columns listed above
- Do not include id-columns in the output.
- Return a single SELECT query only
- Do not use markdown
- If ambiguous, return: AMBIGUOUS: \<question\>
- If unanswerable, return: UNANSWERABLE: \<reason\>

The full prompt can be found in the file `prompts.py` 

### Data → text
The data → text prompt is less restrictive. If the output Dataframe only contains a single row, the prompt asks the LLM to generate write a brief answer, followed by a more in-depth non-technical explanation of the chosen methodology.

If the output Dataframe is longer, then the LLM is tasked with providing a brief one-sentence explanation, followed by a more in-depth analysis of the numbers, and last an in-depth non-technical explanation of the chosen methodology.

Part of the prompt is
- BRIEF: \<one sentence non-technical description of the results. It should focus on explaining the numbers in the DataFrame.\>
- IN-DEPTH: \<2-4 sentences non-technical summary of the results, focussing on any interesting patterns, trends, or outliers in the data. It should focus on explaining the numbers in the DataFrame.\>
- METHODOLOGY: \<brief non-technical summary of any methodological choices, assumptions, or interpretations you made in writing the SQL query\>

### Text and SQL → plotting dictionary
Finally, the prompt that asks the LLM to generate a Python dict that can be used for the plotting functionality. The prompt is rather long, since it details all the options for the plotting functionality. Furthermore, it uses the LLM's ability to return output that strictly follows a schema. See the file `prompts.py` for details.

# Error handling and guardrails
The code has error handling around the SQL query execution, and LLM requests. The SQL exception handling makes sure that the program exits gracefully with an error message that the SQL did not execute correctly. Second, there is **guardrailing** that makes sure that the SQL query starts with the keyword `select` and does not contain any of the keywords `insert`, `update`, `delete`, `drop`, or `alter`.

The LLM error handling also consist of two parts: first is the exception handling in case that the LLM request in itself fails. This could be the case if the API key is wrong or there is no more credit on the account.

Second, in the case that the question can not reasonably be translated into an SQL-query, LLM is asked to return either `AMBIGUOUS: \<question\>` or `UNANSWERABLE: \<reason\>`. In these cases, the agent exits with an error message and the reason stated by the LLM.

# Evaluation approach
The notebook `eval.ipynb` contains a small evaluation script. The script read a list of test cases from `eval.py`, which each contain 
- a question
- a "golden standard" SQL
- a category: [answerable, unanswerable, unsafe] corresponding to the result from the SQL evaluation.
- a chart type

and several other fields. 

Then it loops through the test cases and runs the agent on the questions. The results are then compared between the ground truth. For now, I have implemented evaluation of the Dataframe similarity, the category, and the chart type.

This could be enhanced with letting an LLM evaluate the entire agent output (SQL, text, data) against the question, by asking if the response is adequate and precise. 

Furthermore, 10 test cases are far too few for a comprehensive test.

## Design decisions and trade-offs
- I chose a simple notebook-first Python setup to keep the system easy to inspect, explain, and evaluate. 
- The overall design is a single linear pipeline—question → SQL generation → validation → execution → answer/plotting—rather than a more complex multi-agent system. 
- I also prioritized guardrails over breadth: the agent explicitly handles ambiguous and unanswerable questions, and only allows safe read-only 
- SQL. For the additional capability, I chose plotting because it adds clear business value without adding much architectural complexity.

## Limitations
- The system still depends on LLM quality, so SQL generation and plot selection can fail on edge cases. 
- The SQL safety layer is lightweight and not equivalent to production-grade validation or governance. Plotting is intentionally constrained to a small set of supported chart types, so some valid outputs are better shown as tables. 
- The evaluation is useful as a first check, but the test set is still too small to make strong claims about overall robustness.

# Future improvements
With more time, it would be good idea to consider implementing the following:
- Add an SQL dry-run and in case of error, get the LLM to make a revised SQL.
- Add a generate → critisize → revise loop on the SQL generation to avoid wrongful, but executable SQL.
- If this should go into production somewhere, I would probably not run it on a user with writing permission to the DB. This would in turn render the SQL-guardrails redundant. 

With regard to evaluation, it is recommended to implement an LLM-based evaluation, that takes the question, the SQL-query, the Dataframe, and the natural language report and evaluate if it is all coherent.




