import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class DatabaseExporter:
    def __init__(self, host, database, username, password):
        print("database exporter initiated")
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.engine = None  # Initialize a variable to store the SQLAlchemy engine

    def create_connection(self):
        try:
            # Create a SQLAlchemy engine using the database connection parameters
            self.engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}/{self.database}')
        except SQLAlchemyError as e:
            print(f"Error creating connection: {e}")
            raise  # Re-raise the exception to propagate it up the call stack

    def export_df_to_table(self, df, table_name):
        try:
            # Export the DataFrame to the specified table using pandas' to_sql method
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Table {table_name} exported successfully!")
        except Exception as e:
            print(f"Error exporting table {table_name}: {e}")

    def close_connection(self):
        # No need to close the connection explicitly with SQLAlchemy
        pass

    def export_dfs_to_tables(self, df_dict):
        try:
            for table_name, df in df_dict.items():
                self.export_df_to_table(df, table_name)
        except Exception as e:
            print(f"Error exporting tables: {e}")

    def run(self, df_dict):
        try:
            self.create_connection()
            self.export_dfs_to_tables(df_dict)
        except Exception as e:
            print(f"Error running exporter: {e}")