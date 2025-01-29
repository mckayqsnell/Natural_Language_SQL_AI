# Disc Golf Database AI Interface - Natural Language SQL Project

## Purpose
This database is designed to manage disc golf equipment inventory, tracking discs, their owners, flight characteristics, types, and manufacturers. It allows for querying detailed information about discs, their specifications, and ownership details.

## Schema
The database schema consists of the following tables:
- Disc: Contains information about discs, including their name, type, flight characteristics, and manufacturer.
- Manufacturer: Contains information about disc manufacturers.
- Owner: Contains information about disc owners, including their name and contact information.
- FlightRating: Contains information about the flight ratings of discs.

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

## Example Usage
Program output: 

Ask a question about disc golf (or 'quit' to exit): 

Input:

How many of the discs are of the manufacturer Discraft?

Output:

Generated SQL query: SELECT COUNT(*) FROM Disc INNER JOIN Manufacturer ON Disc.manufacturerID = Manufacturer.manufacturerID WHERE Manufacturer.name = 'Discraft';

Response: Based on the provided query results, there are 3 discs in the database that are manufactured by Discraft.

Fact check: There are indeed 3 discs in the database that are manufactured by Discraft.

## Prompting Strategies Tested
Based on the paper *How to Prompt LLMs for Text-to-SQL: A Study in Zero-shot, Single-domain, and Cross-domain Settings*, I implemented the following prompting strategies:

1. Zero-shot: Use the base prompt with no examples.

    Input: "How many discs does Sarah Johnson own?"
    
    Output:   
    "Generated SQL query:
        `SELECT COUNT(*) FROM Disc d JOIN Owner o ON d.ownerID = o.ownerID WHERE o.firstName = 'Sarah' AND o.lastName = 'Johnson';`
        Response: Sarah Johnson owns 2 discs."

    Input: "What is the total number of discs in the database?"

    Output: 
    "Generated SQL query: 
        `SELECT COUNT(*) FROM Disc;`"
        Response: The total number of discs recorded in the database is 10."

    Input: "How many discs have a speed rating of 13?"

    Output:
    "Generated SQL query: 
        `SELECT COUNT(*) FROM Disc INNER JOIN FlightRating ON Disc.flightRatingID = FlightRating.flightRatingID WHERE FlightRating.speed = 13;`
        Response: There are 2 discs in the database that have a speed rating of 13."
    
2. Single-domain: Questions with disc golf domain context included.
   
   Input: How many of the discs have a Speed rating of 13 or a glide rating of 5?
   
   Output:
   "Generated SQL query: 
        `SELECT COUNT(*) 
        FROM Disc 
        JOIN FlightRating ON Disc.flightRatingID = FlightRating.flightRatingID 
        WHERE FlightRating.speed = 13 OR FlightRating.glide = 5;`
    Response: According to the database query results, there are a total of 6 discs that have either a speed rating of 13 or a glide rating of 5."

    Input: "How many discs are manufactured by Innova and have a turn rating of -1?"

    Output: 
    "Generated SQL query: 
        `SELECT COUNT(*) as disc_count 
        FROM Disc 
        JOIN Manufacturer ON Disc.manufacturerID = Manufacturer.manufacturerID 
        JOIN FlightRating ON Disc.flightRatingID = FlightRating.flightRatingID 
        WHERE Manufacturer.name = 'Innova' AND FlightRating.turn = -1;`
    Response: According to the database query results, there are 2 discs manufactured by Innova that have a turn rating of -1."

3. Cross-domain: In cross-domain, I include examples from different domains before showing the disc golf schema and question.

    Input: "Query me a list of each manufacturer's name and the number of discs they have in the database."

    Output:
    "Generated SQL query: 
        `SELECT Manufacturer.name, COUNT(Disc.discID) AS discCount 
        FROM Manufacturer 
        LEFT JOIN Disc ON Manufacturer.manufacturerID = Disc.manufacturerID 
        GROUP BY Manufacturer.manufacturerID, Manufacturer.name;`
    
    Response: The query returned a list of manufacturers along with the number of discs they have in the database. Here are the results:

    - **Innova** has 3 discs.
    - **Discraft** also has 3 discs.
    - **Dynamic Discs** has 2 discs.
    - **Latitude 64** has 1 disc.
    - **MVP Disc Sports** has 1 disc.

    In summary, the manufacturers Innova and Discraft are tied with the highest number of discs, each having three, while the others have fewer. "


## Conclusion
Overall the project was successful in implementing a natural language interface for querying a disc golf database. 
The AI model was able to generate SQL queries based on user input questions and provide accurate responses based on the database results. 
The prompting strategies tested showed that the model performed well in zero-shot, single-domain, and cross-domain settings, demonstrating its robustness and adaptability to different contexts. 
This project has the potential to be expanded further to include more complex queries, additional database tables, and enhanced natural language processing capabilities.


 
