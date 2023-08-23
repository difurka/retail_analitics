"""Контроллер в MVC"""
from model.model import Model


class Controller():
    def __init__(self):
        self.model = Model()

    def controller_proposals(self, request):
        self.model.model_proposals(request)

    def controller_result(self):
        return self.model.model_result()
