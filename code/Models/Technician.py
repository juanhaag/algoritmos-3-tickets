
class Technician:
    """Class Technician
    """
    def __init__(self, id: str, name: str, surname: str, phone: str):
        self._id = id
        self._name = name
        self._surname = surname
        self._phone = phone

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:  
        return self._name
    
    @property
    def surname(self) -> str:
        return self._surname
    
    @property
    def phone(self) -> str:
        return self._phone
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "surname": self._surname,
            "phone": self._phone,
        }