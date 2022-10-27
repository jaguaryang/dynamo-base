import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from DynamoBase import DynamoBase

DynamoBase.table_region = "ap-southeast-2"
DynamoBase.table_name = "users"

# DynamoBase.put_item(Item={"first_name": "Jackson", "age": 15})
user = DynamoBase.get_first(query={"first_name": "Jackson"}, ScanIndexForward=False)
print(user)
