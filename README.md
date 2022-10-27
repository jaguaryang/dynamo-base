# DynamoBase

A Json Model that is the easiest way to query DynamoDB.

# Install

```
pip install DynamoBase
```

# Use

## Basic try

```
from DynamoBase import DynamoBase
DynamoBase.table_region = "ap-southeast-2"
DynamoBase.table_name = "users"

user = DynamoBase.get_item(query={"first_name": "Jackson"})
print(user)

user = DynamoBase.get_items(query={"first_name": "Jackson"}, IndexName='ix_name')
print(user)

# Doesn't need parameter IndexName when query primary key, GSI does
user = DynamoBase.get_first(query={"first_name": "Jackson"})
print(user)

user = DynamoBase.put_item(Item={"first_name": "Jackson"})
print(user)

user = DynamoBase.update_item(query={"first_name": "Jackson"}, doc={'field': 12345})
print(user)

user = DynamoBase.delete_item(query={"first_name": "Jackson"})
print(user)
```

## Recommendation

1. Create models for each table. 
```
from DynamoBase import DynamoBase

class User(DynamoBase):
    table_region = "ap-southeast-2"
    table_name = "users"

```

2. Query database
```
user = User.get_first(query={"first_name": "Jackson"})
print(user)
```

3. (Optional) You can also create a base-model to configure common properties, such as region and credentials
```
from DynamoBase import DynamoBase

class MyModel(DynamoBase):
    table_region = "ap-southeast-2"
    table_name = "lt_feedbacks"
```

```
from MyModel import MyModel

class User(MyModel):
    pass
```

4. (Optional) Extend your classes to meet your business needs
```
from DynamoBase import DynamoBase

class MyModel(DynamoBase):
    table_region = "ap-southeast-2"
    table_name = "lt_feedbacks"

    @classmethod
    def get_item(cls, **kwargs):
        ...

    @classmethod
    def other_method(cls, **kwargs):
        ...
```

# Parameters

Supports all DynamoDB query properties:

[DynamoDB Query Parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)
