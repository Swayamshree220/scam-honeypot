class BasePersona:
    """Base class for all personas"""
    
    def __init__(self, name, age, occupation, location):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.location = location
    
    def get_system_prompt(self):
        """Return the system prompt for this persona"""
        raise NotImplementedError
    
    def get_profile(self):
        """Return persona profile"""
        return {
            'name': self.name,
            'age': self.age,
            'occupation': self.occupation,
            'location': self.location
        }