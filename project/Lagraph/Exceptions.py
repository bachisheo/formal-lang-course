class InterpretingError(Exception):
    """Exception using for interpreting error"""

    def __init__(self, msg: str = "Interpreting error"):
        self.msg = msg

    def __repr__(self):
        return self.msg
