class UnitEquipment:
    def __init__(self, id: int, model: str, brand: str, serial_number: str):
        self._id = id
        self._model = model
        self._brand = brand
        self._serial_number = serial_number

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "model": self._model,
            "brand": self._brand,
            "serial_number": self._serial_number,
        }
