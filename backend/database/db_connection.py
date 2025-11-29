import mysql.connector
from mysql.connector import Error
from config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                db_config = Config.get_db_config()
                self._connection = mysql.connector.connect(**db_config)
                logger.info("Database connection established")
            except Error as e:
                logger.error(f"Error connecting to MySQL: {e}")
                raise
        return self._connection
    
    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.rowcount
            return result
        except Error as e:
            connection.rollback()
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()

