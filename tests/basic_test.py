'''Unit tests for basic functions'''
import os
import shutil
from datetime import datetime
import bz2
import zipfile
from python_basics import automate


def test_list_files():
    '''Test the functionality of list_files function'''
    # create temp directory and files
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)
    test_files = [
        "file1.txt",
        "file2.txt"
    ]
    for file in test_files:
        with open(os.path.join(temp_dir, file), 'w', encoding='utf-8') as f:
            f.write('')

    # expected output
    file_info = {
        "file1.txt": {
            'File size(MB)': 0.0,
            'Last modified': datetime.today().strftime('%d %b, %Y')
            },
        "file2.txt": {
            'File size(MB)': 0.0,
            'Last modified': datetime.today().strftime('%d %b, %Y')
        }
    }

    # testing
    files, data = automate.list_files(temp_dir, '.txt')
    expected_files = [entry.name for entry in os.scandir(temp_dir)]
    actual_files = [entry.name for entry in files]
    assert actual_files == expected_files
    assert data == file_info

    # clean up temp directory and files
    shutil.rmtree(temp_dir)


def test_download_files():
    '''Test the functionality of download_files function'''
    test_url = {"variable-descriptions.csv":
                ("https://dataverse.harvard.edu/api/access/datafile/:"
                 "persistentId?persistentId=doi:10.7910/DVN/HG7NV7/YZWKHN")}
    temp_dir = "./temp"

    automate.download_files(test_url, temp_dir)

    # testing
    downloaded_file = [entry.name for entry in os.scandir('temp')][0]
    extension = os.path.splitext(downloaded_file)[1]
    assert extension == ".csv"

    # clean temp dir
    shutil.rmtree(temp_dir)


def test_check_url():
    '''Test the functionality of the check_url function'''
    test_url = "https://www.google.com/"

    content_type = automate.check_url(test_url)
    assert 'text/html' in content_type


def test_extract_bz2():
    '''Test the functionality of the bz2 file extractor'''
    # create a dummy bz2 file
    content = "This is to test extract_bz2"
    compressed_content = bz2.compress(content.encode('utf-8'))
    os.makedirs('./temp', exist_ok=True)
    temp_file = "./temp/file.txt.bz2"

    with open(temp_file, 'wb') as f:
        f.write(compressed_content)

    # testing
    automate.extract_bz2(temp_file)
    with open("./temp/file.txt", 'r', encoding='utf-8') as f:
        assert f.read() == content

    # clean temp dir
    shutil.rmtree('./temp')


def test_extract_zip():
    '''Test the functionality of the zip extractor'''
    # create a dummy .zip file
    content = "This is a test file for .zip"
    os.makedirs('./temp', exist_ok=True)

    with zipfile.ZipFile("./temp/test.zip", 'w') as z:
        z.writestr('sample.txt', content)

    # testing
    automate.extract_zip("./temp/test.zip", "./temp")
    with open("./temp/sample.txt", 'r', encoding='utf-8') as f:
        assert f.read() == content

    # clean temp dir
    shutil.rmtree('./temp')
