import sqlite3
from . import handler_utils as utils


class DBHandler:
    """
    Handles all database interaction for the application.

    Attributes:
        None
    """

    def __init__(self) -> None:
        pass

    def get_new_db_file(self, database_path: str) -> None:
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
        result: list[int] = utils.clean_lection_list(raw)
        return result

    def get_entries(self, lection: int) -> list[tuple[int, str, str, str]]:
        """
        Sends the entries of an entire list to the frontend in a static format.

        Args:
            lection (int): The number of the lection which should be returned.

        Returns:
            list[tuple[int, str, str, str]]: A list of all entries of the given lection.
        """
        self.cursor.execute(f"SELECT * FROM lection_{lection}")
        entries: list[tuple[int, str, str, str]] = self.cursor.fetchall()
        return entries
    
    def delete_entry(self, lection: int, id: int) -> None:
        """
        Deletes an entry from a given list based on their id.
    
        Args:
            lection (int): The number of the lection from which an entry should be deleted.
            id (int): The id of the entry which should be deleted.
    
        Returns:
            None
        """
        self.cursor.execute(f"DELETE FROM lection_{lection} WHERE id=?", (id,))
        self.connection.commit()

    def add_entry(self, lection: int, latin: str, steam: str, german: str) -> None:
        """
        Adds an entry to a given lection by taking latin, steam and german as an input
        while the id is auto-generated.
    
        Args:
            lection (int): The number of the lection to which an entry should be added.
            latin (str): The word which should be added to the 'latin' column.
            steam (str): The word which should be added to the 'steam' column.
            german (str): The word which should be added to the 'german' column.
    
        Returns:
            None
        """
        entry_id: int = self._detect_gap(lection)
        self.cursor.execute(f"INSERT INTO lection_{lection} (id, latin, steam, german) VALUES (?, ?, ? ,?)", (entry_id, latin, steam, german))
        self.connection.commit()

    def _detect_gap(self, lection: int) -> int:
        """
        Find the first missing ID in the sequence of entries for a given lection. 
        This ensures that new entries are inserted at the correct position without 
        leaving unused identifiers.

        Args:
            lection (int): The lection number whose entry IDs should be examined.

        Returns:
            int: The next available ID. If no gaps exist, returns the next 
                consecutive ID after the highest one.
        """
        entries: list[tuple[int, str, str, str]] = self.get_entries(lection)

        last_id: int = 0
        for entry in entries:
            if entry is None:
                return 0
            entry_id: int = entry[0]
            if entry_id == last_id + 1:
                last_id = entry_id
                continue
            else:
                return last_id + 1
        return last_id + 1




def main() -> None:
    handler = DBHandler()
    handler.get_new_db_file("data/demo.db")
    handler.get_entries(1)


if __name__ == "__main__":
    main()
