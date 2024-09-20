
class Helper:

    def read_txt(self, file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
    
    def chunk_create_query(self, create_query):
        query = [q.strip() + ';' for q in create_query.strip().split(';') if q.strip()]
        table = [q.split('"')[1] for q in query]
        return query, table