import hashlib
import secrets

from utils.get_mongo_base import nagrada_base


def token_verification(args):
    token = args['token']
    if token and token != '':
        token = hashlib.sha256(token.encode()).hexdigest()
        collection = nagrada_base['persons']
        table = collection.find_one({'login': args['login']}, {"_id": 0})
        if table and secrets.compare_digest(table['token'], token):
            return True
        return
    aborting(4, args)
