from UnitEquipmentCategoryManager import UnitEquipmentCategoryManager
from Models.UnitEquipment import UnitEquipment

class UnitEquipmentManager:
    def __init__(self):
        self.UnitEquipments = []
    
    def create(self, model_: str, brand_: str,serial_number_: str):
        modelUnitEquipment = model_
        brandUnitEquipment = brand_
        serial_numberUnitEquipment = serial_number_
        new_UnitEquipment = UnitEquipment(modelUnitEquipment, brandUnitEquipment, serial_numberUnitEquipment)
        self.UnitEquipments.append(new_UnitEquipment)
        
    
    def modify(self, id_, newModel, newBrand, newSerialNumber):
        unitEquipmentToModify = self.search(id_)

        if unitEquipmentToModify:
            unitEquipmentToModify.model = newModel
            unitEquipmentToModify.brand = newBrand
            unitEquipmentToModify.serial_number = newSerialNumber
        else:
            print("Equipo no se modificó correctamente")

    def search(self, id_):
        for UnitEquipment in self.UnitEquipments:
            if id_ == UnitEquipment.id:
                return UnitEquipment
        return None
        
    
    def list(self):
        for UnitEquipment in self.UnitEquipments:
            print(UnitEquipment)
    
    def delete(self, id_):
        unitEquipment = self.search(id_)
        if unitEquipment:
            self.UnitEquipments.remove(unitEquipment)
        else:
            print("Equipo no encontrado")
    
    #######Controllers##################
    def index(self):
        """function index
        
        returns 
        """
        return None 
    
    def store(self):
        """function store
        
        returns 
        """
        return None 
    
    def show(self):
        """function show
        
        returns 
        """
        return None 
    
    def update(self):
        """function update
        
        returns 
        """
        return None 
    
    def destroy(self):
        """function destroy
        
        returns 
        """
        return None 
    
    

