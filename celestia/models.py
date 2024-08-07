import typing as t
from base64 import b64decode, b64encode
from dataclasses import dataclass, asdict as _asdict

from celestia._celestia import make_commitment


class Base64(bytes):

    def __new__(cls, value: bytes | str) -> bytes | t.Self:
        value = b64decode(value) if isinstance(value, str) else value
        return super().__new__(cls, value)


class Namespace(Base64):
    """ Celestia commitment
    """

    def __new__(cls, value: int | bytes | str) -> bytes | t.Self:
        value = bytes.fromhex('{:058x}'.format(value)) if isinstance(value, int) else value
        return super().__new__(cls, value)


class Commitment(Base64):
    """ Celestia commitment
    """


def asdict(obj: t.Any) -> t.Dict[str, t.Any]:
    """ Convert an object to a dict """

    def conv(value):
        if isinstance(value, Base64):
            return b64encode(value).decode('ascii')
        return value

    return dict((key, conv(value)) for key, value in _asdict(obj).items())


@dataclass(init=False)
class Balance:
    """ Celestia balance
    """
    amount: int
    denom: str

    def __init__(self, amount, denom):
        self.amount = int(amount)
        self.denom = denom

    @property
    def value(self):
        return float(self.amount / 1000000 if self.denom == 'utia' else self.amount)


@dataclass(init=False)
class Blob:
    namespace: Namespace
    data: Base64
    commitment: Commitment
    share_version: int = 0
    index: int = -1

    def __init__(self, namespace: Namespace, data: Base64,
                 commitment: Commitment = None, share_version: int = 0, index: int = -1):
        self.namespace = Namespace(namespace)
        self.data = Base64(data)
        self.commitment = Commitment(commitment if commitment else make_commitment(namespace, data, share_version))
        self.share_version = share_version
        self.index = index


@dataclass(init=False)
class BlobSubmitResult:
    """ BLOB submit result
    """
    height: int
    commitment: Commitment

    def __init__(self, height: int, commitment: Commitment):
        self.height = int(height)
        self.commitment = Commitment(commitment)
