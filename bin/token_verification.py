import hashlib


def token_verification(token, collection):
    if token and token != '':
        token = hashlib.sha256(token.encode()).hexdigest()
        table = collection.find_one({'token': token}, {"_id": 0})
        if table:
            return table, token
