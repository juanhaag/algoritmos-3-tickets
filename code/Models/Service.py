class Service:
    def __init__(self, id: int, name: str, description: str, price: float):
        self._id = id
        self._name = name
        self._description = description
        self._price = price

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "price": self._price,
        }
        