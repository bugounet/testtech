
class BaseActionManager(object):
    def __init__(self, model):
        self.model = model


class SubActionManager(object):
    def __init__(self, actions):
        self.actions = actions
        self.model = actions.model
