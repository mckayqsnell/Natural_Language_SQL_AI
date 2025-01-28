# Natural Language SQL Project

## Tech Stack
- Language: Python (easy integration with SQLite and OpenAI).
- Libraries: sqlite3, openai

## Workflow
1. User Input : Collect user input in the form of a question
    - example: `What is the total number of employees?`
2. Query Generation : Generate SQL query using GPT from the user input.
3. Query Execution : Execute the SQL query on the database.
4. Result Generation : Generate the result from the database and use GPT for formatting.

## Prompt Strategies
- Zero-shot: Use the base prompt with no examples.
- Single-domain: Add university-specific examples to the prompt
- Cross-domain: Include examples from unrelated domains (e.g., restaurants) to test robustness.