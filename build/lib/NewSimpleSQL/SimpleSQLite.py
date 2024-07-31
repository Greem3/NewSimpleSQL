import sqlite3
import random, string
from typing import Union

letters: list = string.ascii_letters

class Database:
    
    def __init__(self, sqlite3_connection: sqlite3.Connection):
        self.__database: sqlite3.Connection = sqlite3_connection;
        self.__cursor: sqlite3.Cursor = self.__database.cursor();
        self.__necessary: list[str] = ["TEXT", "INTEGER", "REAL", "BLOB", "NUMERIC"]
        
    def close(self):
        """
        Shut down the current database
        """
        self.__database.close()
        
    def __commit(self):
        """
        Save all changes
        """
        self.__database.commit()
        
    def simple_create_table(self, table: dict):
        """
        Create a new table in the database
        """
        
        argument: str = f"CREATE TABLE {table["name"]}("
        
        for column in table["columns"]:
            self.__convert_type(column)

            argument += f'"{column["name"]}"    {column["type"]},'
            
        argument = f"{argument[0:-1]})"
        
        self.__cursor.execute(argument)
        
        self.__commit()
            
        
    def complicated_create_tables(self, tables: list[dict]):
        """
        Create one or more tables in the database
        
        Dictionary keys:
        
        "name" : string
        "columns" : dict {
            "name" : string
            "type" : string|type
        }
        """
        
        for table_data in tables:
            
            argument: str = f"CREATE TABLE {table_data["name"]}("
            
            for column in table_data["columns"]:
                self.__convert_type(column)
                
                argument += f'"{column["name"]}"    {column["type"]},'
                
            argument = f"{argument[0:-1]})"
            
            self.__cursor.execute(argument)
            
            argument = ""
            
        self.__commit()
        
    def simple_select_data(self, table: str, columns: str, conditions: str = '', one_fetch: bool = False):
        """
        It returns information you need from a table.
        
        What is one fetch?
        
        A "One Fetch" is for when you need a single piece of information.
        """
        
        answer = self.__cursor.execute(f'SELECT {columns} FROM {table} {conditions}')
        
        if one_fetch:
            return answer.fetchone()
        
        return answer.fetchall()
    
    def complicated_select_data(self, tables: list[dict]):
        """
        It returns information you need from one or more tables.
        
        Dictionary keys:
        
        "name" : string
        "columns" : string (Example: "column1, column2, column3, column4, ..., columnInfinity)
        "conditions" : string (Example: "Where column1 = "column" ORDER BY column2 DESC")
        
        What is one fetch?
        
        A "One Fetch" is for when you need a single piece of information.
        """
        
        info: list = []
        
        for table in tables:
            
            data = self.__cursor.execute(f'SELECT {table["columns"]} FROM {table["name"]} {table["conditions"]}')
            
            if table["fetch"]:
                info.append(data.fetchone())
                continue
            
            info.append(data.fetchall())
            
        return info
        
    def simple_insert_data(self, table: str, data: tuple|list):
        """
        It allows you to insert data into a table.
        
        The data you want to insert you have to put in a tuple or list and from this tuple/list the data will be inserted in column order.
        
        WARNING:
        You can't leave any data empty, but the data you wanted to be Null will have the data from another table below.
        """
        
        placeholders = ', '.join(['?' for _ in data])
        self.__cursor.execute(f'INSERT INTO {table} VALUES ({placeholders})', data)
        
        self.__commit()
    
    def complicated_insert_data(self, tables_datas: list[dict[Union[str|bool]]]):
        """
        It allows you to insert data into one or more tables.
        
        The data you want to insert you have to put in a tuple or list and from this tuple/list the data will be inserted in column order.
        
        Dictionary keys:
        
        "name" : string
        "datas" : tuple or list
        
        WARNING:
        You can't leave any data empty, but the data you wanted to be Null will have the data from another table below.
        """
        
        for table in tables_datas:
            
            placeholders = ', '.join(['?' for _ in table["datas"]])
            self.__cursor.execute(f'INSERT INTO {table["name"]} VALUES ({placeholders})', table["datas"])
            
        self.__commit()
        
    def simple_update_data(self, table: str, columns: str, condition: str = ''):
        """_summary_

        Args:
            table (str): Table name
            column (str): Columns names and new data (Example: Column1 = "hello", Column2 = "world")
            condition (str, optional): Condition. Defaults to ''.
            
        It allows you to update data in one or more tables according to the conditions you give (or you can give none)
        """
        self.__cursor.execute(f'UPDATE {table} SET {columns} {condition}')
        self.__commit()
        
    def complicated_update_data(self, tables_column_conditions: dict):
        """
        It allows you to update data from a table according to the conditions you give (or you can give none)
        
        Dictionary keys:
        
        "name" : string
        "columns" : string (Example: Column1 = "Hello", Column2 = "World")
        "condition" : string
        """        
        for table in tables_column_conditions:
            
            self.__cursor.execute(f'UPDATE {table["name"]} SET {table["columns"]} {table["condition"]}')
            
        self.__commit()
        
    def simple_delete_table(self, table_name: str):
        """
        Delete a table from the database
        """
        
        self.__cursor.execute(f"DROP TABLE {table_name}");
        self.__commit()
        
    def complicated_delete_table(self, tables_names: list[str]):
        """
        Delete one or more tables from the database
        """
        
        for table in tables_names:
            self.__cursor.execute(f"DROP TABLE {table}");
        
        self.__commit()
        
    def custom_execute(self, query: str):
        """
        Run the SQL command you want
        """
        
        self.__cursor.execute(query)
        self.__commit()
            
    def __convert_type(self, column: dict, inverse: bool = False):
        
        if isinstance(column["type"], type):
                    
            column["type"] = column["type"].__name__
                
            if column["type"] == "str":
                column["type"] = "TEXT";
            
            elif column["type"] == "int":
                column["type"] = "INTEGER";
                
            elif column["type"] == "float":
                column["type"] = "REAL";
                
            elif column["type"] == "Blob":
                column["type"] = "BLOB";
                
            else:
                raise TypeError("This Type don't exist in sqlite3!")
        else:
            
            if column["type"].upper() in self.__necessary:
                column["type"] = column["type"].upper()
            else:
                raise TypeError("This Type don't exist in sqlite3!")
            
def generate_id(length: int = 18, contains_letters: bool = False, only_letters: bool = False):
    """
    It generates a random ID for you without you having to do it yourself
    
    WARNING:
    If the ID is for numbers only, a number of any size can be displayed.
    If the ID contains letters, or is letter-only, it will always be the same size
    """

    new_id: str = ''
    
    if contains_letters == True:
    
        for i in range(0, length):
        
            if random.random() <= 0.5:
                new_id += str(random.randint(0, 9))
            else:
                new_id += random.choice(letters)
              
        return new_id
    
    if only_letters == True:
    
        for i in range(0, length):
        
            new_id += random.choice(letters)
          
        return new_id
    
    
    return random.randint(1, 10**length)-1

__all__ = [ 'Database', 'generate_id']