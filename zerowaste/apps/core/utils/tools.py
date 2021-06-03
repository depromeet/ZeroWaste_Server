import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields:
        data[f.name] = f.value_from_object(instance)
    return data