import sqlite3
from handler_utils import clean_lection_list


class DBHandler:
    """
    Handles all database interaction for the application.

    Attributes:
        None
    """

    def __init__(self) -> None:
        pass

    def _get_new_db_file(self, database_path: str) -> None:
        """
        Refreshes the database path so that the user can manage multiple databases.

        Args:
            database_path (str): The path to your SQLite file.

        Returns:
            None
        """
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def get_tables(self) -> list[int]:
        """
        Searches the given database and returns all lection numbers.

        Args:
            None

        Returns:
            list[int]: The numbers of the founded lections.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        raw: list[tuple[str]] = self.cursor.fetchall()
        result: list[int] = clean_lection_list(raw)
        return result


def main() -> None:
    handler = DBHandler()
    handler._get_new_db_file("data/demo.db")
    handler.get_tables()


if __name__ == "__main__":
    main()
