__author__ = 'Omar Verduga'


class Nodo:


    def __init__(self,lug,gScore,lid,parent=None):
        self.lugar = lug #lugar del pmapa
        self.gScore = gScore # costo hasta el momento
        self.parent = parent # nodo padre
        self.fScore = 0 # score de este nodo
        self.lid = lid # id para buscar el lugar
      #  print " creando nodo con costo" + str(gScore)


    def __eq__(self, l):
            if l.lugar == self.lugar and l.gScore == self.gScore and l.fScore == self.fScore and l.lid == self.lid   :
                return 1
            else:
                return 0

    def __str__(self):
        return " lugar "+ str( self.lugar)
    def __repr__(self):
        return self.__str__()