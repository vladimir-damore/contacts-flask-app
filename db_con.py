"""The database connection class for the contacts database"""

import mysql.connector
import dotenv

env_vars = dotenv.dotenv_values()


class ConnectionClass:
    """
    This is the class for the contacts database
    """

    def __init__(self):
        self.__my_conn = mysql.connector.connect(host=env_vars['DB_HOST'],
                                                 user=env_vars['DB_USER'],
                                                 password=env_vars['DB_PASSWORD'],
                                                 database=env_vars['DB_DATABASE'],
                                                 port=env_vars['DB_PORT'])
        self.__my_curr = self.__my_conn.cursor()

    def user_login_with_email(self, email: str, password: str):
        self.__my_curr.execute(
            'select * from login where email="{}" and password="{}"'.format(email, password))
        return self.__my_curr.fetchone()

    def check_whether_email_exists(self, email: str) -> bool:
        self.__my_curr.execute(
            'select * from login where email="{}"'.format(email))
        return True if self.__my_curr.fetchone() else False

    def user_signup_with_email(self, unique_id: str, name: str, email: str, password: str):
        self.__my_curr.execute('insert into login values ("{}", "{}", "{}", "{}")'.format(
            unique_id, name, email, password))
        self.__my_conn.commit()

    def put_data(self, name: str, number: int) -> None:
        """ 
        Put name and number into the database
        """
        self.__my_curr.execute(
            f'insert into identity values ("{name}", {number})')
        self.__my_conn.commit()

    def get_all_data(self) -> list:
        """
        Get all the data from the database and return it

        Returns:
            list: The list of all the data
        """
        self.__my_curr.execute('select * from contact')
        return self.__my_curr.fetchall()

    def get_data_from_name(self, name: str) -> int:
        """
        Get the number from the database from the name

        Args:
            name (str): The name of the person

        Returns:
            int: The number of the person
        """
        self.__my_curr.execute(
            f'select number from identity where name="{name}"')
        return self.__my_curr.fetchone()[0]

    def delete_data_from_name(self, name: str) -> None:
        """
        Delete the data from the database from the name

        Args:
            name (str): The name of the person
        """
        self.__my_curr.execute(f'delete from identity where name="{name}"')
        self.__my_conn.commit()

    def update_data(self, name: str, number: int) -> None:
        """
        Update the number from the database from the name

        Args:
            name (str): The name of the person
            number (int): The number of the person
        """
        self.__my_curr.execute(
            f'update identity set number={number} where name="{name}"')
        self.__my_conn.commit()

    def close_connection(self) -> None:
        """
        Close the connection
        """
        self.__my_conn.close()

    def check_connection(self) -> bool:
        """
        Check if the connection is established

        Returns:
            bool: True if the connection is established, else False
        """
        return self.__my_conn.is_connected()
