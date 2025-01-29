import sqlite3
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

class DiscGolfDB:
    def __init__(self):
        self.conn = sqlite3.connect('disc_golf.db')
        self.cursor = self.conn.cursor()
    
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall(), [description[0] for description in self.cursor.description]
        except Exception as e:
            return None, str(e)
    def getSchema(self):
        return """
        CREATE TABLE Disc(
            discID INTEGER PRIMARY KEY AUTOINCREMENT,
            ownerID INTEGER NOT NULL,
            flightRatingID INTEGER,
            discTypeID INTEGER NOT NULL,
            manufacturerID INTEGER NOT NULL,
            color VARCHAR(255),
            name VARCHAR(255),
            weight DECIMAL(5, 2),
            FOREIGN KEY(flightRatingID) REFERENCES FlightRating(flightRatingID),
            FOREIGN KEY(manufacturerID) REFERENCES Manufacturer(manufacturerID),
            FOREIGN KEY(ownerID) REFERENCES Owner(ownerID),
            FOREIGN KEY(discTypeID) REFERENCES DiscType(discTypeID)
        );

        CREATE TABLE FlightRating(
            flightRatingID INTEGER PRIMARY KEY AUTOINCREMENT,
            speed DECIMAL(8, 2) NOT NULL,
            glide DECIMAL(8, 2) NOT NULL,
            turn DECIMAL(8, 2) NOT NULL,
            fade DECIMAL(8, 2) NOT NULL
        );

        CREATE TABLE Owner(
            ownerID INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            phoneNumber VARCHAR(15) NOT NULL
        );

        CREATE TABLE DiscType(
            discTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
            typeName VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL
        );

        CREATE TABLE Manufacturer(
            manufacturerID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL
        );
        """

# Prompt strategies

def zero_shot_prompt(schema, question):
    return f"""
    Given the following SQLite database schema:
    {schema}
        
    Generate a SQL query to answer this question: {question}
        
    Important: Return ONLY the raw SQL query without any markdown formatting, quotes, or explanation.
    For example, just return: SELECT * FROM Table WHERE condition;
    """
    
def single_domain_prompt(schema, question):
    return f"""
    Given the following SQLite database schema:
    {schema}
        
    Here are some example questions and their SQL queries:

    Question: "What are all the discs made by Innova?"
    SQL: SELECT Disc.name, Disc.color, DiscType.typeName 
        FROM Disc 
        JOIN Manufacturer ON Disc.manufacturerID = Manufacturer.manufacturerID 
        JOIN DiscType ON Disc.discTypeID = DiscType.discTypeID 
        WHERE Manufacturer.name = 'Innova';

    Question: "Show me all discs with speed rating above 10"
    SQL: SELECT Disc.name, FlightRating.speed 
        FROM Disc 
        JOIN FlightRating ON Disc.flightRatingID = FlightRating.flightRatingID 
        WHERE FlightRating.speed > 10;

    Question: "Which owners have more than 2 discs?"
    SQL: SELECT Owner.firstName, Owner.lastName, COUNT(*) as disc_count 
        FROM Owner 
        JOIN Disc ON Owner.ownerID = Disc.ownerID 
        GROUP BY Owner.ownerID, Owner.firstName, Owner.lastName 
        HAVING COUNT(*) > 2;

    Now generate a SQL query for this question: {question}
    Important: Return ONLY the raw SQL query without any markdown formatting, quotes, or explanation.
    For example, just return: SELECT * FROM Table WHERE condition;
    """
    
def cross_domain_prompt(schema, question):
    return f"""
    # Example Database 1: Car Dealership
    CREATE TABLE Vehicle(
        vehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
        modelID INTEGER NOT NULL,
        dealerID INTEGER NOT NULL,
        price DECIMAL(10, 2),
        color VARCHAR(255)
    );
        
    Question: "How many red vehicles cost more than $20000?"
    SQL: SELECT COUNT(*) 
        FROM Vehicle 
        WHERE Vehicle.color = 'red' 
        AND Vehicle.price > 20000;

    # Example Database 2: Library
    CREATE TABLE Book(
        bookID INTEGER PRIMARY KEY AUTOINCREMENT,
        authorID INTEGER NOT NULL,
        genreID INTEGER NOT NULL,
        rating DECIMAL(3, 1),
        pageCount INTEGER
    );
        
    Question: "Which authors have written books with ratings above 4.5?"
    SQL: SELECT Author.firstName, Author.lastName, COUNT(*) 
        FROM Book 
        JOIN Author ON Book.authorID = Author.authorID 
        WHERE Book.rating > 4.5 
        GROUP BY Author.authorID, Author.firstName, Author.lastName;

    # Your Disc Golf Database
    {schema}
        
    Now generate a SQL query for this question: {question}
    Important: Return ONLY the raw SQL query without any markdown formatting, quotes, or explanation.
    For example, just return: SELECT * FROM Table WHERE condition;
    """


class GPTInterface:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = OpenAI()
        
    
    def generate_sql(self, schema, question, strategy='zero-shot'):
        if strategy == "zero-shot":
            prompt = zero_shot_prompt(schema, question)
        elif strategy == "single-domain":
            prompt = single_domain_prompt(schema, question)
        else:
            prompt = cross_domain_prompt(schema, question)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a SQL expert. Generate only SQL queries without any explanation."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_response(self, schema, question, query, result, columns):
        prompt = f"""
        Given the following:
        
        Database schema:
        {schema}
        
        Question: {question}
        
        SQL Query used:
        {query}
        
        Query results (columns: {', '.join(columns)}):
        {result}
        
        Please provide a natural language response to the original question.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant explaining database query results in natural language."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()


def main():
    db = DiscGolfDB()
    gpt = GPTInterface()
    
    while True:
        strategy = input("Select a strategy (zero-shot, single-domain, cross-domain): ")
        
        if strategy not in ["zero-shot", "single-domain", "cross-domain"]:
            print("Invalid strategy. Please choose from 'zero-shot', 'single-domain', or 'cross-domain'.")
            continue
            
        question = input("\nAsk a question about disc golf (or 'quit' to exit): ")
        
        if question.lower() == 'quit':
            break
        
        try:
            sql_query = gpt.generate_sql(db.getSchema(), question, strategy)
            print(f"Generated SQL query: {sql_query}")
            
            results, columns = db.execute_query(sql_query)
            
            if results is None:
                print(f"Error: {columns}")
                continue
            
            response = gpt.generate_response(db.getSchema(), question, sql_query, results, columns)
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
if __name__ == "__main__":
    main()