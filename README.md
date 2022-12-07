# DynamoBase

A lightweight JSON model that simplifies DynamoDB's obscure query operations. It retains all original parameters and supports DynamoDB versions and future upgrades.

# Install

```
pip install dynamobase
```

# Use

## Basic try

```
from DynamoBase import DynamoBase

DynamoBase.table_region = "ap-southeast-2"
DynamoBase.table_name = "users"
DynamoBase.session = ... # if you need specific settings like aws profile, credentials etc.

# get a single item
user = DynamoBase.get_item(query={"first_name": "Jackson"})
print(user)

# get a list of items, IndexName is optional
user = DynamoBase.get_items(query={"first_name": "Jackson"}, IndexName='ix_name')
print(user)

# get the first item, IndexName is optional
user = DynamoBase.get_first(query={"first_name": "Jackson"}, IndexName='ix_name')
print(user)

# insert an item
DynamoBase.put_item(Item={"first_name": "Jackson"})

# update an item, Item is part or all of item
DynamoBase.update_item(query={"first_name": "Jackson"}, Item={'field': 12345})

# delete an item
DynamoBase.delete_item(query={"first_name": "Jackson"})
```

## Recommendation

1. Create the corresponding model for each table.

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

class BaseModel(DynamoBase):
    table_region = "ap-southeast-2"

```

```
from BaseModel import BaseModel

class User(BaseModel):
    table_name = "users"
```

4. (Optional) Extend your classes to meet your business needs

```
from DynamoBase import DynamoBase

class User(DynamoBase):
    table_region = "ap-southeast-2"
    table_name = "users"

    @classmethod
    def get_item(cls, **kwargs):
        ...

    @classmethod
    def other_method(cls, **kwargs):
        ...
```

5. More example

```
res = Article.get_item(query={"_id": "hH2ZZTgQqzgK888zrkG8ui"})
print(1, res)
res = Article.get_items(
    IndexName="ix_category_id",
    query={"category_id": 1, "created_at": {">": 1}},
    ProjectionExpression="title",
    ScanIndexForward=True,
)
print(2, res)
res = Article.get_items(
    IndexName="ix_test",
    query={"_id": "ewTx3gannQUinM7ECjpQad", "url": {"begins_with": "1"}},
    ProjectionExpression="title",
    ScanIndexForward=True,
)
print(3, res)
res = Article.get_first(
    IndexName="ix_category_id",
    query={"category_id": 1, "created_at": {"between": [1670367685098, 1670367663116]}},
    ProjectionExpression="title",
    ScanIndexForward=False,
)
print(4, res)
res = Article.put_item(Item={"_id": "123", "data": {"a": 123}})
print(5, res)
res = Article.update_item(query={"_id": "123"}, Item={"data": {"a": 456}})
print(6, res)
res = Article.delete_item(query={"_id": "123"})
print(7, res)
```

```
res = Article.get_items(
    IndexName="ix_status",
    query={"status": 1},
    ProjectionExpression="title, #url",
    ExpressionAttributeNames={"#url": "url"},
    ScanIndexForward=True,
)
```

# APIs

All "GET" operations support: = | <= | < | >= | > | begins_with | between

## get_item

### parameters

| Name  | Type | Example     | description                              |
| ----- | ---- | ----------- | ---------------------------------------- |
| query | dict | {"id": 123} | query must be primary key (and sort key) |

### return: Dict or None

## get_items

### parameters: The parameters supported by `get_items` and `get_first` are as follows:

| Name                   | Type                           | description                             |
| ---------------------- | ------------------------------ | --------------------------------------- |
| query                  | dict                           | query can be primary key or GSI columns |
| IndexName              | String                         | required if query is GSI or LSI         |
| Select                 | String                         |
| AttributesToGet        | List                           |
| Limit                  | int                            |
| ConsistentRead         | String                         |
| KeyConditions          | dict                           |
| QueryFilter            | dict                           |
| ConditionalOperator    | String                         |
| ScanIndexForward       | boolean                        |
| ExclusiveStartKey      | dict                           |
| ReturnConsumedCapacity | String                         |
| ProjectionExpression   | String                         |
| FilterExpression       | boto3.dynamodb.conditions.Attr |

### return: List<Dict> or None

## get_first

### parameters: same as get_items

### return: Dict or None

## put_item

### parameters

| Name | Type | Example     |
| ---- | ---- | ----------- |
| Item | dict | {"id": 123} |

## update_item

### parameters

| Name  | Type | Example                 | description                              |
| ----- | ---- | ----------------------- | ---------------------------------------- |
| query | dict | {"id": 123}             | query must be primary key (and sort key) |
| Item  | dict | {"field": "some value"} | --                                       |

## delete_item

### parameters

| Name  | Type | Example     | description                              |
| ----- | ---- | ----------- | ---------------------------------------- |
| query | dict | {"id": 123} | query must be primary key (and sort key) |

# DynamoDB docs

[DynamoDB Query Parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)
