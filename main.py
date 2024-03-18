'''To Run'''
from python_basics import automate
from central_log import config_log

# configure logging
config_log()

test_url = {"2008.csv.bz2":
            ("https://dataverse.harvard.edu/api/access/datafile/:"
             "persistentId?persistentId=doi:10.7910/DVN/HG7NV7/EIR0RA")}
automate.download_files(test_url, "temp")
automate.extract_bz2('temp/2008.csv.bz2')
