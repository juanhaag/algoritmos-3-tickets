
class Technician:
    """Class Technician
    """
    def __init__(self, id: str, name: str, surname: str, phone: str):
        self.id = id
        self.name = name
        self.surname = surname
        self.phone = phone

    @property
    def id(self):
        return self.id
    
    @property
    def name(self):  
        return self.name
    
    @property
    def surname(self):
        return self.surname
    
    @property
    def phone(self):
        return self.phone
    
    @id.setter
    def set_id(self, id: str):
        self.id = id
    
    @name.setter
    def set_name(self, name: str):
        self.name = name
    
    @surname.setter
    def set_surname(self, surname: str):
        self.surname = surname
    
    @phone.setter
    def set_phone(self, phone: str):
        self.phone = phone