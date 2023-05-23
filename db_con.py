"""The database connection class for the contacts database"""

import sqlite3
from datetime import date

class ConnectionClass:
    """
    This is the class for the contacts database
    """

    def __init__(self):
        self.__my_conn = sqlite3.connect(
            database='db/filestore.db', check_same_thread=False)  # 'filestore.db
        self.__my_curr = self.__my_conn.cursor()

    def user_login_with_user_email(self, email: str, password: str) -> list:
        """Returns the user data if the user exists in the database"""

        self.__my_curr.execute(
            'select * from login where email="{}" and password="{}"'.format(email, password))
        return self.__my_curr.fetchone()

    def check_whether_user_email_exists(self, email: str) -> bool:
        """Returns True if the email exists in the database else False"""

        self.__my_curr.execute(
            'select * from login where email="{}"'.format(email))
        return True if self.__my_curr.fetchone() else False

    def user_signup_with_user_email(self, unique_id: str, name: str, email: str, password: str) -> bool:
        """Function to signup the user with the email and password"""

        try:
            self.__my_curr.execute('insert into login values ("{}", "{}", "{}", "{}")'.format(
                unique_id, name, email, password))
            self.__my_conn.commit()

            return True
        except sqlite3.Error:
            return False

    def user_save_contact(self, unique_id: str, name: str, number: int) -> None:
        """ 
        Put name and number into the database
        """
        self.__my_curr.execute(
            'insert into contact values ("{}", "{}", {}, "{}")'.format(unique_id, name, number, date.today()))
        self.__my_conn.commit()

    def get_all_contacts_of_user(self, unique_id: str) -> list:
        """
        Get all the data from the database and return it

        Returns:
            list: The list of all the data
        """
        self.__my_curr.execute('select * from contact where id="{}"'.format(unique_id))
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
            f'select number from contacts where name="{name}"')
        return self.__my_curr.fetchone()[0]

    def delete_data_from_name(self, name: str) -> None:
        """
        Delete the data from the database from the name

        Args:
            name (str): The name of the person
        """
        self.__my_curr.execute(f'delete from contacts where name="{name}"')
        self.__my_conn.commit()

    def update_data(self, name: str, number: int) -> None:
        """
        Update the number from the database from the name

        Args:
            name (str): The name of the person
            number (int): The number of the person
        """
        self.__my_curr.execute(
            f'update contacts set number={number} where name="{name}"')
        self.__my_conn.commit()

    def close_connection(self) -> None:
        """
        Close the connection
        """
        self.__my_conn.close()
