"""The database connection class for the contacts database"""

from datetime import date

import os
import mysql.connector

# Importing all environment variables
# Windows: FOR /F "eol=# tokens=*" %i IN (.env) DO SET %i
# Linux: export $(cat .env | xargs)

ENV = os.environ

# Check whether all the environment variable are loaded
if "HOST" in ENV:
    print("[+] All ENVs are loaded")
    SECRET_KEY = ENV.get("SECRET_KEY")
else:
    print("[+] ENVs are not loaded")
    exit()


class ConnectionClass:
    """
    This is the class for the contacts database
    """

    def __init__(self):
        try:
            self.__my_conn = mysql.connector.connect(
                host=ENV.get("HOST", "").strip(),
                user=ENV.get("USER", "").strip(),
                password=ENV.get("PASSWORD", "").strip(),
                port=int(ENV.get("PORT")),  # type: ignore
                database=ENV.get("DATABASE", "").strip(),
                autocommit=True
            )
        except mysql.connector.Error as error_name:
            print("[+] Error", error_name)
            self.__my_conn = None
        else:
            self.__my_curr = self.__my_conn.cursor()

    def check_the_connection(self) -> bool:
        """Returns True if the connection is established else False"""

        return True if self.__my_conn else False

    def user_login_with_user_email(self, email: str, password: str) -> list:
        """Returns the user data if the user exists in the database"""

        self.__my_curr.execute(
            'select id, name, email from login where email="{}" and password="{}"'.format(
                email, password
            )
        )
        return self.__my_curr.fetchone()  # type: ignore

    def check_whether_user_email_exists(self, email: str) -> bool:
        """Returns True if the email exists in the database else False"""

        self.__my_curr.execute('select id from login where email="{}"'.format(email))
        return True if self.__my_curr.fetchone() else False

    def user_signup_with_user_email(
        self, unique_id: str, name: str, email: str, password: str
    ) -> bool:
        """Function to signup the user with the email and password"""

        try:
            self.__my_curr.execute(
                'insert into login values ("{}", "{}", "{}", "{}")'.format(
                    unique_id, name, email, password
                )
            )
            self.__my_conn.commit()

            return True
        except mysql.connector.Error:
            return False

    def user_save_contact(self, unique_id: str, name: str, number: int) -> None:
        """
        Put name and number into the database
        """
        self.__my_curr.execute(
            'insert into contact (id, name, number, create_date) values ("{}", "{}", {}, "{}")'.format(
                unique_id, name, number, date.today()
            )
        )
        self.__my_conn.commit()

    def get_all_contacts_of_user(self, unique_id: str) -> list:
        """
        Get all the data from the database and return it

        Returns:
            list: The list of all the data
        """
        self.__my_curr.execute(
            'select name, number from contact where id="{}"'.format(unique_id)
        )
        return self.__my_curr.fetchall()

    def delete_contact_of_user(self, contact_name: str, user_unique_id: str) -> None:
        """
        Delete the contact of the user from the database from the name

        Args:
            contact_name (str): The name of the person
            user_unique_id (str): The unique id of the user
        """
        self.__my_curr.execute(
            'delete from contact where name="{}" and id="{}"'.format(
                contact_name, user_unique_id
            )
        )
        self.__my_conn.commit()

    def update_contact_of_user(
        self,
        new_contact_number: str,
        contact_name: str,
        user_unique_id: str,
    ) -> None:
        """
        Update the details of the contact in the database from the name and user unique id

        Args:
            new_contact_number (int): The new number of the contact
            contact_name (str): The name of the contact
            user_unique_id (str): The unique id of the user
        """
        self.__my_curr.execute(
            'update contact set number={} where name="{}" and id="{}"'.format(
                new_contact_number, contact_name, user_unique_id
            )
        )
        self.__my_conn.commit()

    def close_connection(self) -> None:
        """
        Close the connection
        """
        self.__my_curr.close()
        self.__my_conn.close()
        print("[+] Connection closed")
