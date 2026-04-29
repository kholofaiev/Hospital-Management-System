from .Prescription import Prescription

class Diagnosis():
    def __init__(self, diagnosis_name:str, treatment = None) -> None:
        if treatment:
            self._diagnosis_name = diagnosis_name
            self.treatment = treatment
        else:
            self._diagnosis_name = diagnosis_name
    
    
    def __str__(self) -> str:
        return f'Diagnosis is {self._diagnosis_name}\nTreatment is {self.treatment}'
    