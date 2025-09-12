from ServiceManager import ServiceManager

class ServiceCategoryManager:

    def __init__(self):
        self.Categories = []

    def create(self, CategoryName_, CategoryId_):
        ServiceCategory = ServiceManager(CategoryName_,CategoryId_)
        self.Categories.append(ServiceCategory)

  
    def modify(self, ServiceCategoryId_, ServiceCategoryNewName_):
        CategoryToModify = self.search(ServiceCategoryId_)

        if CategoryToModify:
            CategoryToModify.Category = ServiceCategoryNewName_
        else:
            print("Categoria no encontrada")
  
    def search(self, SearchId_):
        for ServiceCategory in self.Categories:
            if ServiceCategory.CategoryId == SearchId_:
                return ServiceCategory
        return None 
    
    def list(self):
        return self.Categories

    
    def delete(self,CategoryId_):
        DeletedCategory = self.search(CategoryId_)
        if DeletedCategory:
            print(f"Categoria removida: {DeletedCategory.Category}")
            self.Categories.remove(DeletedCategory)
        else:
            print("Categoria no encontrada")


