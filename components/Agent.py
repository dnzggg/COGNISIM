class Agent:
    def __init__(self, index: int, name: str, strategy: str = ""):
        self.index = index
        self.name = name
        self.strategy = strategy

    def set_strategy(self, strategy: str):
        self.strategy = strategy
