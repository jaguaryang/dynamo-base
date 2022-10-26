import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from DynamoBase import DynamoBase

DynamoBase.table_name = "users"

user = DynamoBase.get_first(query={"first_name": "Jackson"})

print(user)
