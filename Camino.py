__author__ = 'Omar Verduga'


class Camino:
    def __init__(self, nodos  , costoTotal ):

        self.nodos = nodos
        self.costoTotal = costoTotal


    def getNodos(self):

        return self.nodos

    def getCostoTotal(self):

        return self.costoTotal
