# To test the use cases of different functions
from python_basics.automate import listFiles

files, file_info = listFiles("red", ".md")
print(file_info)