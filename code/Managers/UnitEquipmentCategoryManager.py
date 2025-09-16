
class UnitEquipmentCategoryManager:
    def __init__(self, id: int, name :str, description : str):
        self.idUnitEquipmentCategories = id
        self.nameUnitEquipmentCategories = name
        self.descriptionUnitEquipmentCategories = description
        self.UnitEquipmentCategories = []

    def create(self, name_, description_):
        nameUnitEquipmentCategories = name_
        descriptionUnitEquipmentCategories = description_
        newUnitEquipmentCategory = UnitEquipmentCategories(nameUnitEquipmentCategories,descriptionUnitEquipmentCategories)
        self.UnitEquipmentCategories.append(newUnitEquipmentCategory)
        
    
    def modify(self):
        """function modify
        
        returns 
        """
        return None 
    
    def search(self):
        """function search
        
        returns 
        """
        return None 
    
    def list(self):
        """function list
        
        returns 
        """
        return None 
    
    def delete(self):
        """function delete
        
        returns 
        """
        return None 
    

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
    

