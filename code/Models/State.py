class State:
    """Simple ticket state value object."""
    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> dict:
        return {"name": self.name}
