import logging
import os
import re
import sqlite3
import ssl

import certifi
import tldextract
from colorama import Fore, Style
from yarl import URL

"""This file contains generic information and functions that are used around the program"""

FILE_FORMATS = {
    'Images': {
        '.jpg', '.jpeg', '.png', '.gif',
        '.gif', '.webp', '.jpe', '.svg',
        '.tif', '.tiff', '.jif',
    },
    'Videos': {
        '.mpeg', '.avchd', '.webm', '.mpv',
        '.swf', '.avi', '.m4p', '.wmv',
        '.mp2', '.m4v', '.qt', '.mpe',
        '.mp4', '.flv', '.mov', '.mpg',
        '.ogg', '.mkv'
    },
    'Audio': {
        '.mp3', '.flac', '.wav', '.m4a'
    },
    'Other': {
        '.json', '.torrent', '.zip', '.rar'
    }
}

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
ssl_context = ssl.create_default_context(cafile=certifi.where())

MAX_FILENAME_LENGTH = 100

logger = logging.getLogger(__name__)


async def sanitize(input: str) -> str:
    return re.sub(r'[<>:"/\\|?*\']', "", input)


async def sql_initialize(download_history):
    conn = sqlite3.connect(download_history)
    curr = conn.cursor()
    create_table_query = """CREATE TABLE IF NOT EXISTS downloads (
                                filename TEXT,
                                size INTEGER NOT NULL,
                                completed INTEGER NOT NULL,
                                PRIMARY KEY (filename, size)
                            );"""
    curr.execute(create_table_query)

    conn.commit()
    return conn, curr


async def sql_check_existing(cursor: sqlite3.Cursor, filename, size):
    cursor.execute("""SELECT completed FROM downloads WHERE filename = '%s' and size = %d""" % (filename, size))
    sql_file_check = cursor.fetchone()
    if sql_file_check:
        if sql_file_check[0] == 1:
            return True
    return False


async def sql_insert_file(connection: sqlite3.Connection, cursor: sqlite3.Cursor, filename, size, completed):
    cursor.execute("""INSERT OR IGNORE INTO downloads VALUES ('%s', %d, %d)""" % (filename, size, completed))
    connection.commit()


async def sql_update_file(connection: sqlite3.Connection, cursor: sqlite3.Cursor, filename, size, completed):
    cursor.execute("""INSERT OR REPLACE INTO downloads VALUES ('%s', %d, %d)""" % (filename, size, completed))
    connection.commit()


async def log(text, style=Fore.WHITE) -> None:
    """Wrapper around print() to add color to text"""
    logger.debug(text)
    print(style + str(text) + Style.RESET_ALL)


async def clear() -> None:
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


async def make_title_safe(title: str):
    title = re.sub(r'[\\*?:"<>|./]', "-", title)
    return title


async def purge_dir(dir, in_place=True):

    deleted = []
    dir_tree = list(os.walk(dir, topdown=False))

    for tree_element in dir_tree:
        sub_dir = tree_element[0]
        is_empty = not len(os.listdir(sub_dir))
        if is_empty:
            deleted.append(sub_dir)

    if in_place:
        list(map(os.rmdir, deleted))

    return deleted


async def regex_links(urls) -> list:
    all_links = [x.group().replace(".md.", ".") for x in re.finditer(r"(?:http.*?)(?=('|$|\n|\r\n|\r|\s|\"|\[/URL]))", urls)]
    yarl_links = []
    for link in all_links:
        yarl_links.append(URL(link))
    return yarl_links


async def bunkr_parse(url: URL) -> URL:
    """Fix the URL for bunkr.is."""
    extension = '.' + str(url).split('.')[-1]
    if extension.lower() in FILE_FORMATS['Videos']:
        url = URL('https://media-files.bunkr.is/').with_name(url.name)
        return url
    if extension.lower() in FILE_FORMATS['Images']:
        url = url.with_host('cdn.bunkr.is')
        return url
    return url


async def cyberdrop_parse(url: URL) -> URL:
    mapping_direct = [r'img-...cyberdrop...', r'f.cyberdrop...', r'fs-...cyberdrop...']
    url = str(url)
    for mapping in mapping_direct:
        url = re.sub(mapping, 'cyberdrop.to', url)
    return URL(url)


async def pixeldrain_parse(url: URL, title: str) -> URL:
    """Fix the URL for Pixeldrain"""
    if url.parts[1] == 'l':
        final_url = URL('https://pixeldrain.com/api/list/') / title / 'zip'
    else:
        final_url = (URL('https://pixeldrain.com/api/file/') / title).with_query('download')
    return final_url


async def check_direct(url: URL):
    mapping_direct = ['i.pixl.is', r's..putmega.com', r's..putme.ga', r'img-...cyberdrop...', r'f.cyberdrop...',
                      r'fs-...cyberdrop...', r'cdn.bunkr...', r'media-files.bunkr...', r'jpg.church/images/...',
                      r'stream.bunkr...', r'simp..jpg.church']
    for domain in mapping_direct:
        extension = '.' + str(url).split('.')[-1]
        if re.search(domain, url.host):
            return True
        elif extension in FILE_FORMATS['Videos'] or extension in FILE_FORMATS['Images'] or extension in FILE_FORMATS['Audio'] or extension in FILE_FORMATS['Other']:
            return True
    return False
