import boto3, simplejson as json
from boto3.dynamodb.conditions import Key


class DynamoBase:
    table_region = "us-east-1"
    table_name = None
    session = boto3.Session()

    @classmethod
    def get_item(cls, **kwargs):
        query = kwargs["query"]
        response = cls._table().get_item(Key=query)
        if "Item" not in response:
            return None
        res = json.loads(json.dumps(response["Item"]))
        return res

    @classmethod
    def get_items(cls, **kwargs):
        query = kwargs["query"]
        expression = cls._KeyConditionExpression(query)
        params = kwargs.copy()
        params.pop("query", None)
        params.pop("TableName", None)
        params.pop("KeyConditionExpression", None)
        params.pop("ExpressionAttributeNames", None)
        params.pop("ExpressionAttributeValues", None)
        response = cls._table().query(
            **params,
            KeyConditionExpression=" and ".join(expression["Expression"]),
            ExpressionAttributeNames=expression["ExpressionAttributeNames"],
            ExpressionAttributeValues=expression["ExpressionAttributeValues"],
        )
        res = json.loads(json.dumps(response["Items"]))
        return res

    @classmethod
    def get_first(cls, **kwargs):
        items = cls.get_items(**kwargs, Limit=1)
        return items[0] if items else None

    @classmethod
    def put_item(cls, **kwargs):
        Item = kwargs["Item"]
        response = cls._table().put_item(Item=Item)
        return response

    @classmethod
    def update_item(cls, **kwargs):
        query = kwargs["query"]
        Item = kwargs["Item"]
        expression = cls._UpdateExpression(Item)
        response = cls._table().update_item(
            Key=query,
            UpdateExpression="SET " + (", ".join(expression["Expression"])),
            ExpressionAttributeNames=expression["ExpressionAttributeNames"],
            ExpressionAttributeValues=expression["ExpressionAttributeValues"],
        )
        return response

    @classmethod
    def delete_item(cls, **kwargs):
        query = kwargs["query"]
        response = cls._table().delete_item(Key=query)
        return response

    @classmethod
    def _table(cls):
        dynamodb = cls.session.resource("dynamodb", region_name=cls.table_region)
        tb = dynamodb.Table(cls.table_name)
        return tb

    # EQ | LE | LT | GE | GT | BEGINS_WITH | BETWEEN
    # = | <= | < | >= | > | begins_with | between
    @classmethod
    def _KeyConditionExpression(cls, dct):
        Expression = []
        ExpressionAttributeNames = {}
        ExpressionAttributeValues = {}
        for key in dct:
            if type(dct[key]) is not dict:
                dct[key] = {"=": dct[key]}
            for op, vv in dct[key].items():
                # expressions
                if op == "begins_with":
                    Expression.append("begins_with(#{}, :{})".format(key, key))
                elif op == "between":
                    Expression.append("#{} between :{}1 and :{}2".format(key, key, key))
                else:
                    Expression.append("#{} {} :{}".format(key, op, key))
                # keys
                ExpressionAttributeNames["#" + key] = key
                # values
                if op == "between":
                    vv.sort()
                    ExpressionAttributeValues[":" + key + "1"] = vv[0]
                    ExpressionAttributeValues[":" + key + "2"] = vv[1]
                else:
                    ExpressionAttributeValues[":" + key] = vv

        return {
            "Expression": Expression,
            "ExpressionAttributeNames": ExpressionAttributeNames,
            "ExpressionAttributeValues": ExpressionAttributeValues,
        }

    @classmethod
    def _UpdateExpression(cls, dct):
        Expression = []
        ExpressionAttributeNames = {}
        ExpressionAttributeValues = {}
        for k, v in dct.items():
            Expression.append("#{} = :{}".format(k, k))
            ExpressionAttributeNames["#" + k] = k
            ExpressionAttributeValues[":" + k] = v
        return {
            "Expression": Expression,
            "ExpressionAttributeNames": ExpressionAttributeNames,
            "ExpressionAttributeValues": ExpressionAttributeValues,
        }
