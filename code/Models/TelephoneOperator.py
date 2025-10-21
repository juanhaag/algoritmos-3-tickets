class TelephoneOperator:
    def __init__(self, id: str, name: str):
        self._id = id
        self._name = name

    def to_dict(self) -> dict:
        return {"id": self._id, "name": self._name}
