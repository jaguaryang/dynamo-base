# DynamoBase

A Json Model that is the easiest way to query DynamoDB.

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

# APIs

## get_item

### parameters

| Name  | Type | Example     |
| ----- | ---- | ----------- |
| query | dict | {"id": 123} |

### return: Dict or None

## get_items

### parameters: The parameters supported by `get_items` and `get_first` are as follows:

| Name                   | Type                           |
| ---------------------- | ------------------------------ |
| query                  | dict                           |
| IndexName              | String                         |
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

### return: same as get_item

## put_item

### parameters

| Name | Type | Example     |
| ---- | ---- | ----------- |
| Item | dict | {"id": 123} |

## update_item

### parameters

| Name  | Type | Example                 |
| ----- | ---- | ----------------------- |
| query | dict | {"id": 123}             |
| doc   | dict | {"field": "some value"} |

## delete_item

### parameters

| Name  | Type | Example     |
| ----- | ---- | ----------- |
| query | dict | {"id": 123} |

# DynamoDB docs

[DynamoDB Query Parameters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)
