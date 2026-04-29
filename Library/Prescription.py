class Prescription:
    def __init__(self, prescription_meds:dict) -> None:
        self._items = prescription_meds
        
    
    def add_item(self, medication:str, dosage:str):      
        if medication not in self._items:
            self._items[medication] = dosage
            return f'{medication} was added'
        else:
            return f'Error: {medication} is already in Prescription\nUse Prescription.eddit_item to change dosage'
        
    
    def eddit_item(self, medication:str, new_dosage:str):
        if medication in self._items:
            self._items[medication] = new_dosage
            return f'{medication} was changed to {new_dosage}'
        else:
            return f'Error: {medication} is not in Prescription\nUse Prescription.add_item() to add new medication'

    
    def remove_item(self, medication:str):
        if medication in self._items:
            del self._items[medication]
            return f"Removed: {medication}"
        else:
            return f"Error: {medication} not found in prescription."
    
    
    def __str__(self) -> str:
        output = ['--- Current Prescription ---']
        
        for med, dosage in self._items.items():
            output.append(f'* {med.title()}: {dosage}')
        
        return '\n'.join(output)