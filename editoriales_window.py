from catalogo_simple import SimpleCatalogWindow



 

class EditorialesWindow(SimpleCatalogWindow):

    def __init__(self, parent, on_change=None):

        super().__init__(parent, "editoriales", "Gestión de Editoriales", "Editorial", on_change)