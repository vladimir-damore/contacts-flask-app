"""The database connection class for the contacts database"""

from datetime import date

import dotenv
from sqlalchemy import create_engine, exc, text

# Importing all environment variables
# Windows: FOR /F "eol=# tokens=*" %i IN (.env) DO SET %i
# Linux: export $(cat .env | xargs)
# Mac: export $(cat .env | xargs)

dotenv.load_dotenv()
ENV = dotenv.dotenv_values()

# Check whether all the environment variable are loaded
if "HOST" in ENV:
    print("[+] All ENVs are loaded")
else:
    print("[+] ENVs are not loaded")
    exit()

host = ENV.get("HOST", "")
user = ENV.get("USER", "")
dpwd = ENV.get("PASSWORD", "")
port = int(ENV.get("PORT"))  # type: ignore
database = ENV.get("DATABASE", "")
SECRET_KEY = ENV.get("SECRET_KEY")

DATABASE_URI = f"mysql://{user}:{dpwd}@{host}:{port}/{database}"


class ConnectionClass:
    """
    This is the class for the contacts database
    """

    def __init__(self):
        try:
            self.__engine = create_engine(
                DATABASE_URI,
                connect_args={
                    "ssl_mode": "VERIFY_IDENTITY",
                    "ssl": {"ca": "cacert.pem"},
                },
                pool_size=5,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600,
                pool_pre_ping=True,
            )

            for _ in range(self.__engine.pool.size()):
                conn = self.__engine.connect()
                conn.close()
            print("[+] Database pool warmup successful")

        except exc.SQLAlchemyError as error_name:
            print("[+] Error", error_name)
            self.__engine = None

    def check_the_connection(self) -> bool:
        """Returns True if the connection is established else False"""

        return bool(self.__engine)

    def user_login_with_user_email(self, email: str, password: str) -> list:
        """Returns the user data if the user exists in the database"""

        with self.__engine.connect() as conn:
            stmt = text("select lid, lname, lemail from login where lemail=:email and lpassword=:password")
            result = conn.execute(stmt, {"email": email, "password": password}).fetchone()

        return result  # type: ignore

    def check_whether_user_email_exists(self, email: str) -> bool:
        """Returns True if the email exists in the database else False"""

        with self.__engine.connect() as conn:
            stmt = text("select lid from login where lemail=:email")
            result = conn.execute(stmt, {"email": email}).fetchone()

        return bool(result)

    def user_signup_with_user_email(self, unique_id: str, name: str, email: str, password: str) -> bool:
        """Function to signup the user with the email and password"""

        try:
            with self.__engine.connect() as conn:
                stmt = text("insert into login values (:lid, :lname, :lemail, :lpassword)")
                conn.execute(
                    stmt,
                    {
                        "lid": unique_id,
                        "lname": name,
                        "lemail": email,
                        "lpassword": password,
                    },
                )
                conn.commit()
            return True

        except exc.SQLAlchemyError:
            return False

    def user_save_contact(self, contact_id: str, name: str, number: int, user_id: str) -> None:
        """
        Put name and number into the database
        """
        with self.__engine.connect() as conn:
            stmt = text("insert into contact values (:cid, :cname, :cnumber, :lid, :date)")
            conn.execute(
                stmt,
                {
                    "cid": contact_id,
                    "cname": name,
                    "cnumber": number,
                    "lid": user_id,
                    "date": date.today(),
                },
            )
            conn.commit()

    def get_all_contacts_of_user(self, unique_id: str) -> list:
        """
        Get all the data from the database and return it

        Returns:
            list: The list of all the data
        """
        with self.__engine.connect() as conn:
            stmt = text("select cname, cnumber from contact where lid=:lid")
            result = conn.execute(stmt, {"lid": unique_id}).fetchall()

        return result  # type: ignore

    def delete_contact_of_user(self, contact_name: str, user_unique_id: str) -> None:
        """
        Delete the contact of the user from the database from the name

        Args:
            contact_name (str): The name of the person
            user_unique_id (str): The unique id of the user
        """
        with self.__engine.connect() as conn:
            stmt = text("delete from contact where lname=:lname and lid=:lid")
            conn.execute(stmt, {"lname": contact_name, "lid": user_unique_id})
            conn.commit()

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
        with self.__engine.connect() as conn:
            stmt = text("update contact set lnumber=:lnumber where lname=:lname and lid=:lid")
            conn.execute(
                stmt,
                {
                    "lnumber": new_contact_number,
                    "lname": contact_name,
                    "lid": user_unique_id,
                },
            )
            conn.commit()
