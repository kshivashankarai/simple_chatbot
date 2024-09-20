
import os
from dotenv import load_dotenv

from database.database_functions import PostgresConnection
from helpers.helper_functions import Helper
from vector_database.vector_database_functions import VectorDatabaseFunctions
from text_to_sql_model.text_to_sql_functions import TextToSql
from conversation_model.conversation_functions import Conversation


load_dotenv()

collection_name = os.getenv("COLLECTION_NAME")

pg_connection = PostgresConnection()
helper = Helper()
vector_db_connection = VectorDatabaseFunctions()
text_to_sql_functions = TextToSql()
conversation = Conversation()

conn, message = pg_connection.connect()

def update_database_structure_in_vector_db():
    file_path = os.getenv("QUERY_FILE_PATH")
    db_structure = helper.read_txt(file_path)
    query, table = helper.chunk_create_query(db_structure)
    vector_db_connection.update_vectors(collection_name, query, table)


def fetch_context_from_vector_db(query, count):
    update_database_structure_in_vector_db()
    return vector_db_connection.fetch_similar_tables(collection_name, query, count, max_distance=1.5)

# results = fetch_context_from_vector_db('get all departments', 1)
# print(results)

# def generate_sql_from_text_to_sql(context, query):
#     return text_to_sql_functions.generate_sql(context, query)

# context = 'CREATE TABLE head (age INTEGER)'

# query = "How many heads of the departments are older than 56 ?"

# sql_query = generate_sql_from_text_to_sql(context, query)

# print(sql_query)

def get_db_response(conn, query):
    return pg_connection.execute_query(conn, query)

result, response = get_db_response(conn, 'SELECT users.*, department.* FROM users JOIN department ON users.department_id = department.id')

print(result)


def get_answer(question, response):
    return conversation.generate_answer(question, response)

# # Test get_answer function
result = get_answer('List down all the users along with their email and department', result)

print(result.content)
print('----------')
exit()