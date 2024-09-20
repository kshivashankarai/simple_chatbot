import os
from dotenv import load_dotenv

import psycopg2
from psycopg2 import OperationalError, Error

load_dotenv()

class PostgresConnection:

    def connect(self):
        try:
            conn = psycopg2.connect(
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                host=os.getenv("DB_HOST"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT"),
            )
            return conn, "Connection to PostgreSQL successful."
        except OperationalError as e:
            return None, f"Error: {e}"

    def close(self, conn):
        if conn:
            conn.close()
            return "Connection closed."
        return "Connection was not established."

    def execute_query(self, conn, query):
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                cursor.close()
                return results, "Query executed successfully."
            conn.commit()
            cursor.close()
            return None, "Query executed successfully."
        except (Exception, Error) as e:
            return None, f"Error executing query: {e}"

    def get_all_table_structure(self, conn):
        query = """
        SELECT table_name, column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        results, message = self.execute_query(conn, query)

        if results:
            table_structure = {}
            for row in results:
                table_name, column_name, data_type, max_length = row
                if table_name not in table_structure:
                    table_structure[table_name] = []
                table_structure[table_name].append({
                    "column_name": column_name,
                    "data_type": data_type,
                    "max_length": max_length
                })
            return table_structure, message
        
        return None, message