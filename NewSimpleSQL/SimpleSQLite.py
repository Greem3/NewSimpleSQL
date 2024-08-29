import sqlite3
import random, string
from typing import Union

class Database():
    
    def __init__(self, sqlite3_connection: sqlite3.Connection|str, auto_commit: bool = True):
        self.__database: sqlite3.Connection = sqlite3.connect(sqlite3_connection) if isinstance(sqlite3_connection, str) else sqlite3_connection;
        self.__database.autocommit = auto_commit
        self.__cursor: sqlite3.Cursor = self.__database.cursor();
        self.__necessary: tuple[str] = ("TEXT", "INTEGER", "REAL", "BLOB", "NUMERIC")
        
    def close(self):
        """
        Shut down the current database
        """
        self.__database.close()
        
    def commit(self):
        """
        Save all changes
        """
        self.__database.commit()
        
    def simple_create_table(self, table: dict):
        """
        Create a new table in the database
        """
        
        argument: str = f"CREATE TABLE {table["name"]}("
        
        for column_name, column_type in table["columns"].items():
            column_type = self.__convert_type(column_type)

            argument += f'"{column_name}"    {column_type},'
        
        if table.get("fk") != None:
            for column_name, foreign_info in table["fk"].items():
                column_name: str; foreign_info: list|tuple
                
                argument += f'FOREIGN KEY ({column_name}) REFERENCES {foreign_info[0]}({foreign_info[1]})'
                
                #TODO: hacer que detecte si la referencia contiene un ON DELETE CASCADE, que sirve para que se elimine la fila si se elimina el registro de la foreing key
                
                if len(foreign_info) >= 3:
                    if foreign_info[2]:
                        argument += "ON DELETE CASCADE"
                
                argument += ','
                
            
        argument = f"{argument[0:-1]})"

        self.__cursor.execute(argument)
            
        
    def complicated_create_tables(self, tables: list[dict]):
        """
        Create one or more tables in the database
        
        Dictionary keys:
        
        "name" : str
        "columns" : dict
        
        Columns Keys:
        
        "name" : str|type
        """
        
        for table_data in tables:
            
            self.simple_create_table(table_data)
        
    def simple_select_data(self, table: str, columns: str, conditions: str = '', one_fetch: bool = False) -> list[tuple]|tuple:
        """
        It returns information you need from a table.
        
        What is one fetch?
        
        A "One Fetch" is for when you need a single piece of information.
        """
        
        answer = self.__cursor.execute(f'SELECT {columns} FROM {table} {conditions}')
        
        if one_fetch:
            return answer.fetchone()
        
        return answer.fetchall()
    
    def complicated_select_data(self, tables: list[dict]) -> list[list[tuple]|tuple]|list[tuple]:
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
            
        
        
    def simple_update_data(self, table: str, columns: str, condition: str = ''):
        """_summary_

        Args:
            table (str): Table name
            column (str): Columns names and new data (Example: Column1 = "hello", Column2 = "world")
            condition (str, optional): Condition. Defaults to ''.
            
        It allows you to update data in one or more tables according to the conditions you give (or you can give none)
        """
        self.__cursor.execute(f'UPDATE {table} SET {columns} {condition}')
        
        
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
        
    def simple_delete_table(self, table_name: str):
        """
        Delete a table from the database
        """
        
        self.__cursor.execute(f"DROP TABLE {table_name}");
        
        
    def complicated_delete_table(self, tables_names: list[str]):
        """
        Delete one or more tables from the database
        """
        
        for table in tables_names:
            self.__cursor.execute(f"DROP TABLE {table}");
        
        
        
    def custom_execute(self, query: str, *args: tuple|list) -> list[tuple]|tuple|None:
        """
        Run the SQL command you want
        """
        
        self.__cursor.execute(query, args)
        
            
    def __convert_type(self, value: str|type, inverse: bool = False) -> str|tuple:
        
        def sqltype(value_type: str|type) -> str:
            value_type = value_type.__name__ if isinstance(value_type, type) else type(value_type).__name__
            
            if value_type == "tuple":
                
                valor: str =  f'{sqltype(value[0].__name__)} PRIMARY KEY'
                
                if len(value) == 2:
                    valor += f" AUTO_INCREMENT"
                
                return valor
            
            if value_type == "list":
                return f'{sqltype(value[0].__name__)} DEFAULT {value[1]}'
            
            if value_type == "dict":
                return f'{sqltype(value["type"].__name__)} {value['constraints']}'
            
            if value_type == "str":
                return "TEXT"
            
            if value_type == "int":
                return "INTEGER"
            
            if value_type == "float":
                return "REAL"
            
            if value_type == "Blob":
                return "BLOB"
            
            if value_type == "Numeric":
                return "NUMERIC"

            raise TypeError("This Type don't exist in sqlite!")
        
        if isinstance(value, type|tuple|list|dict):  
            return sqltype(value)
            
        if value.upper() in self.__necessary:
            return value.upper()
        
        raise TypeError("This Type don't exist in sqlite!")
    
class Numeric(): pass