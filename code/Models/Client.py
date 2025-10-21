class Client:
    def __init__(self, id: int, name: str, address: str):
        self._id = id
        self._name = name
        self._address = address

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "address": self._address,
        }
