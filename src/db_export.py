import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class DatabaseExporter:
    """
    A class used to export pandas DataFrames to a PostgreSQL database.

    Attributes:
    ----------
    host : str
        The hostname or IP address of the PostgreSQL server.
    database : str
        The name of the PostgreSQL database to connect to.
    username : str
        The username to use for the database connection.
    password : str
        The password to use for the database connection.
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine instance used to connect to the database.
    """

    def __init__(self, host, database, username, password):
        """
        Initializes a new DatabaseExporter instance.

        Parameters:
        ----------
        host : str
            The hostname or IP address of the PostgreSQL server.
        database : str
            The name of the PostgreSQL database to connect to.
        username : str
            The username to use for the database connection.
        password : str
            The password to use for the database connection.

        Example:
        -------
        exporter = DatabaseExporter('localhost', 'mydatabase', 'myuser', 'mypassword')
        """
        print("database exporter initiated")
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.engine = None  # Initialize a variable to store the SQLAlchemy engine

    def create_connection(self):
        """
        Creates a connection to the PostgreSQL database using the provided connection parameters.

        Raises:
        ------
        SQLAlchemyError
            If an error occurs while creating the connection.

        Example:
        -------
        exporter.create_connection()
        """
        try:
            # Create a SQLAlchemy engine using the database connection parameters
            self.engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}/{self.database}')
        except SQLAlchemyError as e:
            print(f"Error creating connection: {e}")
            raise  # Re-raise the exception to propagate it up the call stack

    def export_df_to_table(self, df, table_name):
        """
        Exports a pandas DataFrame to a table in the PostgreSQL database.

        Parameters:
        ----------
        df : pandas.DataFrame
            The DataFrame to export.
        table_name : str
            The name of the table to export to.

        Raises:
        ------
        Exception
            If an error occurs while exporting the table.

        Example:
        -------
        df = pd.DataFrame({'name': ['John', 'Jane'], 'age': [25, 30]})
        exporter.export_df_to_table(df, 'mytable')
        """
        try:
            # Export the DataFrame to the specified table using pandas' to_sql method
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"Table {table_name} exported successfully!")
        except Exception as e:
            print(f"Error exporting table {table_name}: {e}")

    def close_connection(self):
        """
        Closes the connection to the PostgreSQL database.

        Note:
        ----
        This method is a no-op, as SQLAlchemy handles connection closing automatically.
        """
        # No need to close the connection explicitly with SQLAlchemy
        pass

    def export_dfs_to_tables(self, df_dict):
        """
        Exports multiple pandas DataFrames to multiple tables in the PostgreSQL database.

        Parameters:
        ----------
        df_dict : dict
            A dictionary mapping table names to DataFrames.

        Raises:
        ------
        Exception
            If an error occurs while exporting the tables.

        Example:
        -------
        df1 = pd.DataFrame({'name': ['John', 'Jane'], 'age': [25, 30]})
        df2 = pd.DataFrame({'city': ['New York', 'London'], 'country': ['USA', 'UK']})
        exporter.export_dfs_to_tables({'mytable1': df1, 'mytable2': df2})
        """
        try:
            for table_name, df in df_dict.items():
                self.export_df_to_table(df, table_name)
        except Exception as e:
            print(f"Error exporting tables: {e}")

    def run(self, df_dict):
        """
        Runs the exporter, creating a connection and exporting the provided DataFrames to tables.

        Parameters:
        ----------
        df_dict : dict
            A dictionary mapping table names to DataFrames.

        Raises:
        ------
        Exception
            If an error occurs while running the exporter.

        Example:
        -------
        df1 = pd.DataFrame({'name': ['John', 'Jane'], 'age': [25, 30]})
        df2 = pd.DataFrame({'city': ['New York', 'London'], 'country': ['USA', 'UK']})
        exporter.run({'mytable1': df1, 'mytable2': df2})
        """
        try:
            self.create_connection()
            self.export_dfs_to_tables(df_dict)
        except Exception as e:
            print(f"Error running exporter: {e}")