class BaseState:
    def __init__(self) -> None:
        self._rules = [getattr(self, func) for func in dir(self.__class__) if callable(
            getattr(self.__class__, func)) and func.startswith("apply_rule")]

    def __eq__(self, o: object):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    @staticmethod
    def validate(state):
        raise NotImplementedError()

    @property
    def is_objective(self):
        raise NotImplementedError()

    @property
    def is_valid(self):
        return self.validate(self)

    def __repr__(self):
        return str(self)

    @property
    def rules(self):
        return self._rules

    def generate_next_states(self):
        assert isinstance(self, BaseState) and self.is_valid,\
            "Valid state required"
        if self.is_objective:
            return []
        new_states = []
        for rule in self.rules:
            new_state = rule()
            if new_state is not None:
                new_states.append(new_state)
        return new_states
