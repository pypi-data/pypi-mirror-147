import configparser
import contextlib
from datetime import datetime
import json
import os
import pickle
import platform
from rich import box
from rich.console import Console
from rich.table import Table
import shutil
import sqlite3
import sys
from typing import Optional, Any
import warnings

class DnRes:

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.logs = dict()
        self.logs['structure'] = list()
        self.logs['db'] = list()
        self.structure = dict()
        self.db = None
        self.description = None

        if not os.path.exists(self.config_file):
            raise FileNotFoundError('Config file does not exist.')

        self._check_config()
        self._parse_config()
        self._check_structure()
        self._check_db()

        self.console = Console()

    def _check_config(self) -> None:
        """
        Expects the config file to have the sections "STRUCTURE" and "DATABASE".
        It raises exception if they are missing.

        The "STRUCTURE" section should have directory names as keys and paths as values.
        In LINUX systems the paths may include "~".
        It raises exception if "STRUCTURE" is empty.

        The "DATABASE" section should have the key "filename" which is a sqlite database. 
        Missing exception is raised otherwise.

        Directory names from STRUCTURE are stored in database as tables.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if not config.has_section("STRUCTURE"):
            raise KeyError("STRUCTURE section is missing in configuration file.")

        if not config['STRUCTURE']:
            raise KeyError("STRUCTURE section in configuration file is empty.")

        if not config.has_section("DATABASE"):
            raise KeyError("DATABASE section is missing in configuration file.")

        if not config['DATABASE'].get("filename", False):
            raise KeyError('The key "filename" is missing in DATABASE section.')

        if not config.has_section('INFO'):
            raise KeyError("INFO section is missing in configuration file.")

        if not config['INFO'].get("description", False):
            warnings.warn('Key "description" missing in INFO section of config.')

    def _parse_config(self) -> None:
        """
        Parse config file and set self.structure, self.db and self.description.
        """
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.db = config['DATABASE']['filename']

        if config['INFO'].get("description", False):
            self.description = config['INFO']['description']

        for directory, path in config['STRUCTURE'].items():
            if platform.system() == "Linux" and directory.startswith('~/'):
                directory = os.path.expanduser(directory)
            self.structure[directory] = path

    def _check_structure(self) -> None:
        """
        Checks if directories in STRUCTURE section exists.
        Creates the ones that don't exist.
        """
        for directory, path in self.structure.items():
            if not os.path.exists(path):
                os.makedirs(path)
                self.logs['structure'].append(f'Created: "{directory}".')
            else:
                self.logs['structure'].append(f'OK: "{directory}".')

    def _initialize_db(self) -> None:
        """Creates database based on filename specified in DATABASE."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                CREATE TABLE paths(
                directory TEXT,
                path TEXT
                )
                """
                c.execute(query)
                conn.commit()

    def _update_directory_path(self, directory: str, path: str) -> None:
        """Updates the paths of the directories as defined in STRUCTURE"""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                UPDATE paths 
                SET path=(?) 
                WHERE directory=(?)
                """
                c.execute(query, (path, directory))
                conn.commit()

    def _create_table(self, table: str) -> None:
        """Creates table with the name given as directory in STRUCTURE."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                CREATE TABLE {table}(
                date INTEGER,
                filename TEXT,
                datatype TEXT,
                description TEXT,
                source TEXT
                )
                """
                c.execute(query)
                conn.commit()

    def _get_paths_table_entries(self) -> dict:
        """Returns registered directories and paths in DATABASE."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT * FROM paths 
                """
                c.execute(query)
                results = c.fetchall()
        if results:
            results = {res[0]:res[1] for res in results}
        else:
            results = {}
        return results

    def _register_directory(self, directory: str, path: str) -> None:
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                INSERT INTO paths (directory, path) 
                VALUES (?,?)
                """
                c.execute(query, (directory, path))
                conn.commit()

    def _check_db(self) -> None:
        """
        Creates database if it doesn't exist.
        Creates tables with names those given as directories in STRUCTURE.
        Updates directories paths.
        """
        if not os.path.exists(self.db):
            self._initialize_db()
            self.logs['db'].append('Created: database.')
        else:
            self.logs['db'].append('OK: database.')

        paths = self._get_paths_table_entries()
        for directory, path in self.structure.items():
            if paths.get(directory, False):
                if paths[directory] != path:
                    self._update_directory_path(directory, path)
                    self.logs['db'].append(f'Updated path: "{directory}".')
                else:
                    self.logs['db'].append(f'OK: "{directory}".')
            else:
                self._register_directory(directory, path)
                self.logs['db'].append(f'Registered: "{directory}".')
                self._create_table(directory)
                self.logs['db'].append(f'Created table: "{directory}".')

    def _has_filename(self, directory: str, filename: str) -> bool:
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                SELECT 1 FROM {directory}
                WHERE filename=(?)
                """
                c.execute(query, (filename, ))
                result = c.fetchone()
        if result:
            return True
        else:
            return False

    def store(self, 
            data: Any, 
            directory: str, 
            filename: str, 
            description: Optional[str]=None,
            source: Optional[str]=None,
            serialization: Optional[str]=None,
            isfile: bool=False,
            overwrite: bool=False) -> None:
        """
        Stores specified data/results. Data can be an object or a filepath. Objects are serialized.

        Parameters
        ----------
        data : any
            Data to store. It could be any kind of object. If data is a string of a file path, pass isfile=True.
        directory : str
            The directory to store data.
        filename : str
            The filename with extension under which the data will be stored. 
        source : str, optional
            Defaults to None. Source of generated data. If None, the name of the calling script will be considered.
        description : str, optional
            Defaults to None. Short description about the data.
        serialization : str, optional
            Defaults to None. Valid serialization methods : json | pickle
        isfile : bool
            Defaults to False. Pass True in case data is path to a file.
        overwrite : bool
            Defaults to False. Boolean for overwritting previous data with same filename.

        Examples
        --------
        Data is some variable. It could be any object, str, dict, list, tuple etc.
        >>> res.store(data=someVariable, filename="foobar.json", directory="foo", description="some description", serialization="json")

        Data is path to a file.
        >>> res.store(data="foo/somefile.txt", filename="somefile.txt", directory="bar", description="some description", isfile=True)
        """
        serialization_methods = ["json", "pickle"]

        if not self.structure.get(directory, False):
            raise KeyError("Specified directory not found in structure.")

        date = int(datetime.today().strftime('%Y%m%d'))

        if isfile:
            if '.' in data:
                datatype = data.split('.')[-1]
            else:
                datatype = 'unknown'
                warnings.warn("Filetype could not be determined for file.")
        else:
            datatype = str(type(data))

        if serialization:
            if serialization not in serialization_methods:
                raise KeyError(f'Unknown serialization method "{serialization}". Valid methods: {serialization_methods}') 

            if not filename.endswith(f".{serialization}"):
                filename = f"{filename}.{serialization}"

            storePath = os.path.join(self.structure[directory], filename)
            if os.path.exists(storePath) and not overwrite:
                raise FileExistsError(f'Filename "{filename}" exists in "{directory}". Change filename or use overwrite=True.')

            if serialization == 'json':
                with open(storePath, 'w') as outf:
                    json.dump(data, outf)
            elif serialization == 'pickle':
                with open(storePath, 'wb') as outf:
                    pickle.dump(data, outf)
        else:
            # data is assumed a path to file
            if not isinstance(data, str):
                raise TypeError('Data is not a file. Apply serialization method.')
            if not isfile:
                raise Exception('If passed string is filepath pass isfile=True. Otherwise, pass serialization method.')
            if not os.path.exists(data):
                raise FileNotFoundError(f'File "{data}" was not found.')
            if os.path.exists(os.path.join(self.structure[directory], os.path.basename(data))) and not overwrite:
                raise FileExistsError(f'Filename "{os.path.basename(data)}" exists in "{directory}". Use overwrite=True.')
            if overwrite:
                shutil.move(data, os.path.join(self.structure[directory], os.path.basename(data)))
            else:
                shutil.move(data, self.structure[directory])

        self._insert_in_db(directory, 
                           date,
                           filename,
                           datatype,
                           description,
                           source)
        print('Done store.')

    def load(self, directory: str, filename: str) -> Any:
        """
        Loads data/results from specified directory stored as filename. If filename is not serialized object, it returns the path of the filename.

        Parameters
        ----------
        directory : str
            Directory as defined in structure where data/results were stored.
        filename : str
            The filename under which data/results where stored.

        Returns
        -------
        Python object, if filename has the extension json or pickle.
        Filepath, if filename is not a serialized python object.
        """

        if not self.structure.get(directory, False):
            raise KeyError('Directory not found in structure.')

        if not self._has_filename(directory, filename):
            raise FileNotFoundError('Filename not found in database.')

        if not os.path.exists(os.path.join(self.structure[directory], filename)):
            raise FileNotFoundError('Filename not found in structure.')

        if filename.endswith('.json'):
            with open(os.path.join(self.structure[directory], filename), 'r') as inf:
                return json.load(inf)
        elif filename.endswith('.pickle'):
            with open(os.path.join(self.structure[directory], filename), 'rb') as inf:
                return pickle.load(inf)
        else:
            return os.path.join(self.structure[directory], filename)

    def _delete_from_db(self, directory: str, filename: str) -> None:
        """Deletes filename from database based on directory table."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                DELETE FROM {directory} 
                WHERE filename=(?) 
                """
                c.execute(query, (filename, ))
                conn.commit()

    def _insert_in_db(self, 
                      directory: str, 
                      date: int,
                      filename: str,
                      datatype: str,
                      description: Optional[str],
                      source: Optional[str]) -> None:
        """Inserts filename in database, or updates database if filename exists based on directory table."""
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                if self._has_filename(directory, filename):
                    query = f"""
                    UPDATE {directory} 
                    SET date=(?),
                        filename=(?),
                        datatype=(?),
                        description=(?),
                        source=(?)
                    """
                else:
                    query = f"""
                    INSERT INTO {directory} 
                    (date, filename, datatype, description, source) 
                    VALUES (?,?,?,?,?)
                    """
                c.execute(query, (date,
                                  filename,
                                  datatype,
                                  description,
                                  source))
                conn.commit()

    def delete(self, directory: str, filename: str) -> None:
        """
        Deletes data from structure and database based on the given filename.

        directory : str
            The directory where the data were stored.
        filename : str
            The name under which data were stored.
        """

        filepath = os.path.join(self.structure[directory], filename)

        if not os.path.exists(filepath):
            warnings.warn("Filename not found in structure.")
        else:
            os.remove(filepath)

        self._delete_from_db(directory, filename)
        print("Done delete.")

    def move(self, filename: str, source: str, destination: str, overwrite: bool=False) -> None:
        """
        Moves data from source to destination. 

        source : str
            Directory in structure where data are stored.
        destination : str
            Directory in structure where data will be moved to.
        overwrite : bool
            Defaults to False. Flag for overwriting data in destination.
        """

        filepathSource = os.path.join(self.structure[source], filename)
        filepathDestination = os.path.join(self.structure[destination], filename)

        if not self.structure.get(source, False):
            raise KeyError("Source not found in structure.")

        if not self.structure.get(destination, False):
            raise KeyError("Destination not found in structure.")

        if not self._has_filename(source, filename): 
            raise FileNotFoundError("Filename not found in source in database. Cannot get filename info.")

        if self._has_filename(destination, filename) and not overwrite:
            raise FileExistsError("Filename exists in destination in database. Pass overwrite=True.")
        else:
            self._delete_from_db(destination, filename)

        if not os.path.exists(filepathSource):
            raise FileNotFoundError("Filename not found in source structure.")

        if not os.path.exists(filepathDestination):
                shutil.move(filepathSource, self.structure[destination])
        else:
            if not overwrite:
                raise FileExistsError("Filename exists in destination structure. Pass overwrite=True.")
            else:
                shutil.move(filepathSource, filepathDestination)

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                SELECT * FROM {source} 
                WHERE filename=(?)
                """
                c.execute(query, (filename, ))
                results = c.fetchone()

        self._delete_from_db(source, filename)
        self._insert_in_db(destination, *results)
        print("Done move.")

    def set_description(self, description: str, directory: str, filename: str) -> None:
        """
        Set description for existing filename in database based on directory table.

        Parameters
        ----------
        description : str
            The new description.
        directory : str
            Directory table in database where filename is.
        filename : str
            Filename in database to update description.
        """
        if not self.structure.get(directory, False):
            raise KeyError('Directory not found in structure.')

        if not self._has_filename(directory, filename):
            raise FileNotFoundError('Filename not found in database.')

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                UPDATE {directory} 
                SET description=(?) 
                WHERE filename=(?)
                """
                c.execute(query, (description, filename))
                conn.commit()

    def set_source(self, source: str, directory: str, filename: str) -> None:
        """
        Set source information for existing filename in database based on directory table.

        Parameters
        ----------
        source : str
            The new source information.
        directory : str
            Directory table in database where filename is.
        filename : str
            Filename in database to update description.
        """
        if not self.structure.get(directory, False):
            raise KeyError('Directory not found in structure.')

        if not self._has_filename(directory, filename):
            raise FileNotFoundError('Filename not found in database.')

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                UPDATE {directory} 
                SET source=(?) 
                WHERE filename=(?)
                """
                c.execute(query, (source, filename))
                conn.commit()

    def rename(self, directory: str, previous: str, new: str) -> None:
        """
        Rename data from previous to new name filename.

        Parameters
        ----------
        directory : str
            Directory where the filename is.
        previous : str
            Previous name of filename.
        new : str
            New name of filename.
        """

        if not self.structure.get(directory, False):
            raise KeyError('Directory not found in structure.')
        
        filepathPrevious = os.path.join(self.structure[directory], previous)
        filepathNew = os.path.join(self.structure[directory], new)
        if not os.path.exists(filepathPrevious):
            raise FileNotFoundError('Filename not found in structure.')
        os.rename(filepathPrevious, filepathNew)

        # Get new datatype
        if '.' in new:
            datatype = new.split('.')[-1]
        else:
            datatype = 'unknown'
            warnings.warn("Filetype could not be determined for new filename.")

        if not self._has_filename(directory, previous):
            raise FileNotFoundError('Filename not found in database.')

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                UPDATE {directory} 
                SET filename=(?),
                    datatype=(?) 
                WHERE filename=(?)
                """
                c.execute(query, (new, datatype, previous))
                conn.commit()
        print("Done rename.")

    def _print_table(self, rows: list) -> None:
        """Prints rich table of given rows. Rows are list of lists or list of tuples."""
        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("Date", justify="right", no_wrap=True)
        table.add_column("Filename", justify="right", no_wrap=True)
        table.add_column("Datatype", justify="right", no_wrap=True)
        table.add_column("Description", justify="right", no_wrap=False)
        table.add_column("Source", justify="right", no_wrap=False)
        for row in rows:
            # Make sure only strings are passed to table
            table.add_row(*list(map(str, row)))
        self.console.print(table)

    def info_directory(self, directory: str) -> None:
        """
        Shows information for directory.

        Parameters
        ----------
        directory : str
            Directory to show information.
        """
        if not self.structure.get(directory, False):
            raise KeyError("Directory not found in structure.")
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"SELECT * FROM {directory}"
                c.execute(query)
                results = c.fetchall()
        if not results:
            print("No information found for directory.")
        else:
            self._print_table(results)

    def info_filename(self, directory: str, filename: str) -> None:
        """
        Shows information for filename based on directory.

        Parameters
        ----------
        directory : str
            Directory where filename is stored.
        filename : str
            Filename to show information.
        """
        if not self.structure.get(directory, False):
            raise KeyError("Directory not found in structure.")

        if not self._has_filename(directory, filename):
            raise FileNotFoundError('Filename not found in database.')

        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = f"""
                SELECT * FROM {directory} 
                WHERE filename=(?)
                """
                c.execute(query, (filename, ))
                results = c.fetchone()
        if not results:
            print("No information found for directory.")
        else:
            table = Table(box=box.SIMPLE_HEAVY)
            table.add_column("Column", justify="right", style="magenta", no_wrap=True)
            table.add_column("Value", justify="left", no_wrap=False)
            columns = ['Date', 'Filename', 'Datatype', 'Description', 'Source']
            # Make sure only strings are passed to console.print
            for column, value in zip(columns, list(map(str, results))):
                table.add_row(column, value)
            self.console.print(table)

                # self.console.print(f"[bold magenta]{column}[/bold magenta]: {value}")

    def __repr__(self):
        with contextlib.closing(sqlite3.connect(self.db)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                dirsRows = dict()
                for directory in self.structure.keys():
                    query = f"SELECT * FROM {directory}"
                    c.execute(query)
                    results = c.fetchall()
                    if not results:
                        results = [['NA']*5]
                    dirsRows[directory] = results

        if not self.description:
            self.console.print("[bold magenta]Description[/bold magenta]: Not available")
        else:
            self.console.print(f"[bold magenta]Description[/bold magenta]: {self.description}")
        print()
        for directory in self.structure.keys():
            self.console.print(f"[bold magenta]{directory}[/bold magenta]")
            self._print_table(dirsRows[directory])
            print()
        return ''


