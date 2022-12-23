from setuptools import setup,find_packages
from typing import List
Requirement_file_name = "requirements.txt"
variable = "-e ."

def get_requirement():
    with open(Requirement_file_name) as f :
        data = f.readlines()
    data = [word.replace('\n',"") for word  in data ]


    if variable in data :
        data.remove(variable)
    return data




setup(
    name = "sensor",
    version= "0.0.1",
    author= "monu",
    pacakage = find_packages(),
    install_requires = get_requirement(),
)