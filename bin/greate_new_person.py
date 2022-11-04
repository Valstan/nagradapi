import hashlib
from datetime import datetime
from secrets import token_urlsafe


def greate_new_person(args):
    collection = nagrada_base['persons']
    if collection.find_one({'login': args['login']}):
        return aborting(5, args)
    token = token_urlsafe(16)
    body = request.get_json(force=True)
    body['token'] = hashlib.sha256(token.encode()).hexdigest()
    body['reg_date'] = int(datetime.timestamp(datetime.now()))
    collection.update_one({'login': args['login']},
                          {'$set': body}, upsert=True)
    return token
