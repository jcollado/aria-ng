
import random
from shortuuid import ShortUUID

# See: https://github.com/stochastic-technologies/shortuuid
UUID = ShortUUID(alphabet='01234567890ABCDEF')

def generate_id():
    return UUID.uuid()

GENERATED_IDS = set()

def generate_id_old():
    # TODO: a bad way to make sure our IDs are unique (they won't be unique across
    # multiple running instances of ARIA), but better than nothing
    def gen():
        return '%05x' % random.randrange(16 ** 5)
    id = gen()
    while id in GENERATED_IDS:
        id = gen()
    GENERATED_IDS.add(id)
    return id
