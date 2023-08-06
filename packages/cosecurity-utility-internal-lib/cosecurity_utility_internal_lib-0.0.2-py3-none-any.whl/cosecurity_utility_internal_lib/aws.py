import os
import uuid
import boto3
import psycopg2

from dotenv import load_dotenv
from typing import Any, List, Tuple

load_dotenv()


class SimpleStorageService:
    """
    Util class for AWS S3 file and folder management

    Attributes:
        session (boto3.Session): session to connect to aws
        bucket (str): range name of files and folder
        resource (Any): instance connected to aws to reference aws s3
    """
    def __init__(self) -> None:
        self._session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self._bucket = os.getenv("BUCKET")
        self._resource = self._session.resource('s3')

    def push(self, object:Any, path:str, hash:bool=False, extension:str=None) -> str:
        """        
        Method to publish files to storage
        
        Parameters:
            object (Any): file content to be published
            path (str): remote path of the file to be published
            hash (bool | None): defines whether the new file will have a dynamic name
            extension (str | None): defines whether the new file will have a fixed extension

        Returns:
            str: returns the remote path of the published file
        """
        if hash:
            path += f'/{uuid.uuid4()}.{extension}'
        self._resource.Object(self._bucket, path).put(Body=object)
        return path

class PostgresRelationalDatabaseService:
    """
    Useful class to manage the specific relational database service for postgres

    Attributes:
        connection (Any): database connection
    """
    def __init__(self) -> None:
        self._connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )

    def query_with_return_id(self, query:str, vars:Tuple=None) -> int:
        """        
        Method to publish files to storage
        
        Parameters:
            query (str): sql command to be executed
            vars (Tuple): values to be deployed in the command
            
        Returns:
            int: returns the id of the current run
        """
        _id = None

        with self._connection.cursor() as cursor:
            cursor.execute(query, vars)
            _id = cursor.fetchone()[0]
            self._connection.commit()
        
        return _id

    def create_many(self, query:str, vars:List[Tuple]=None) -> None:
        """        
        Method to publish files to storage
        
        Parameters:
            query (str): sql command to be executed
            vars (List[Tuple]): list of values to be deployed in the command
        """
        with self._connection.cursor() as cursor:
            cursor.execute(query, vars)
            self._connection.commit()
