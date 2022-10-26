# DynamoBase

A Json Model that is the easiest way to query DynamoDB.

# install

```
pip install DynamoBase
```

# use

## Basic try

```
from DynamoBase import DynamoBase
DynamoBase.table_region = "ap-southeast-2"
DynamoBase.table_name = "users"

user = DynamoBase.get_first(query={"first_name": "Jackson"})
print(user)
```

## Recommendation

1. Create models for each tables
