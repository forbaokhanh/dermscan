class Ingredient:
    """A class to represent a skincare ingredient."""
    def __init__(self, name, comedogenicity, irritancy):
        self.name = name
        self.comedogenicity = int(comedogenicity)
        self.irritancy = int(irritancy)

    def as_dict(self):
        """Convert the Ingredient instance into a dictionary."""
        return {
            'name': self.name,
            'comedogenicity': self.comedogenicity,
            'irritancy': self.irritancy
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Ingredient instance from a dictionary."""
        return cls(data['name'], data['comedogenicity'], data['irritancy'])