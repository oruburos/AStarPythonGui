__author__ = 'Omar Verduga'
from Nodo import *
from Camino import *
from Lugar import *
import math

class AStar:
    def __init__(self , mapaActual, anchoActual, altura, modo):
        self.mapa = mapaActual
        self.ancho = anchoActual
        self.alto = altura
        self.modoDiagonal = modo;

    def cambiaModo(self , modo):
        self.modoDiagonal = modo

    def encuentraRuta(self, origen, destino ):
        self.openSet = []
        self.on = []
        self.closedSet = []



        ultimoNodo = self.getNodo(destino)
       # print "destno nodo g " + str( ultimoNodo.gScore) + " f "+ str(ultimoNodo.fScore)
        end = destino


        primerNodo = self.getNodo(origen)
      #  print "primer nodo g " + str( primerNodo.gScore) + " f "+ str(primerNodo.fScore)
        self.on.append(primerNodo)
        self.openSet.append(primerNodo.lid)
        nodoSiguiente = primerNodo #Paso 0 , se agrega el nodo inicial como el primero a explorar

        while nodoSiguiente is not None:
            finish = self.checarNodo(nodoSiguiente, end)
            if finish:
                return self.actualizaCamino(finish)
            nodoSiguiente = self.mejorNodoSetAbierto()

        return None


    def getNodo(self, lugar):
        x = lugar.x
        y = lugar.y
        if x < 0 or x >= self.ancho or y < 0 or y >= self.alto:
            return None
        d = self.mapa[(y * self.ancho) + x]
        if d == -1:
            return None

#        print "d " + str(d)

        if  d == 4 :#salir del inicio cuesta 0
            return Nodo(lugar, 0, ((y * self.ancho) + x));
        elif d==5 :#llegar al fin cuesta
            return Nodo(lugar, 1, ((y * self.ancho) + x));
        else:
            return Nodo(lugar, d, ((y * self.ancho) + x));


#Paso 4 , aqui se ordena la lista , si fuera una fila de prioridad seria el primer elemento
    def mejorNodoSetAbierto(self):
        mejorNodo = None
        for n in self.on:
            if not mejorNodo:
                mejorNodo = n
            else:
                if n.fScore <= mejorNodo.fScore:
                        mejorNodo = n

#        print " mejor nodo set abierto " + str( mejorNodo.lugar.x) + "," +str( mejorNodo.lugar.y) +" scores :"+ str(mejorNodo.fScore) +" "+ str(mejorNodo.gScore)
        return mejorNodo

    def actualizaCamino(self, n):
        nodos = [];
       # costoActual = n.gScore;
        costoActual =  n.gScore
        p = n.parent;
        nodos.insert(0, n);

        while 1:
            if p.parent is None:
                break

            nodos.insert(0, p)
            p = p.parent

 #       print " costo actual " + str( costoActual)
        return Camino(nodos, costoActual)

    def checarNodo(self, node, end):
        i = self.openSet.index(node.lid)
        self.on.pop(i)
        self.openSet.pop(i)
        #paso 1, lo metemos en la lista de cerrados
        self.closedSet.append(node.lid)
#paso 2 se explorarn los nodos adyacentes
        nodes = self.nodosAdyacentes(node, end)

        for n in nodes: #paso 3 para cada nodo adyacente
            if n.lugar == end: #si es el nodo destino se
                # se ha alcanzado el final del camino
                return n
            elif n.lid in self.closedSet:
                # los del conjunto cerrado no los exploro
                #3b
                continue
            elif n.lid in self.openSet:
                #3c
                # busco si hay mejor score en open
                i = self.openSet.index(n.lid)
                on = self.on[i];
                if n.gScore < on.gScore:
                    self.on.pop(i);
                    self.openSet.pop(i);
                    self.on.append(n);
                    self.openSet.append(n.lid);
            else:
                # agregar nuevo nodo a la lista abierta
               # print "agregando " +str(n.lugar.x) +" " + str( n.lugar.y)

                self.on.append(n)
                self.openSet.append(n.lid)

        return None



    def nodosAdyacentes(self, nodoActual, dest):
        resultado = []
        cl = nodoActual.lugar
        dl = dest
  #      print "inicio"
      #  print " oeste"
        n = self.actualizaHeuristica(cl.x + 1, cl.y, nodoActual, dl.x, dl.y)
        if n: resultado.append(n)
      #  print " este"
        n = self.actualizaHeuristica(cl.x - 1, cl.y, nodoActual, dl.x, dl.y)
        if n: resultado.append(n)
     #   print " norte"
        n = self.actualizaHeuristica(cl.x, cl.y + 1, nodoActual, dl.x, dl.y)
        if n: resultado.append(n)
      #  print " sur"
        n = self.actualizaHeuristica(cl.x, cl.y - 1, nodoActual, dl.x, dl.y)
        if n: resultado.append(n)

        if ( self.modoDiagonal):
          #  print " noroeste"
            n = self.actualizaHeuristica(cl.x + 1, cl.y + 1, nodoActual, dl.x, dl.y)
            if n: resultado.append(n)
            #  print " noreste"
            n = self.actualizaHeuristica(cl.x - 1, cl.y + 1, nodoActual, dl.x, dl.y)
            if n: resultado.append(n)
          #  print " suroeste"
            n = self.actualizaHeuristica(cl.x + 1, cl.y - 1, nodoActual, dl.x, dl.y)
            if n: resultado.append(n)
            #  print " sureste"
            n = self.actualizaHeuristica(cl.x - 1, cl.y - 1, nodoActual, dl.x, dl.y)
            if n: resultado.append(n)
   #     print "fin"


#se expanden los 4 costos, solo se usan norte sur este oeste, no se usan diagonales
        return resultado

    def actualizaHeuristica(self, x, y, nodoAnterior, destx, desty):
        n = self.getNodo( Lugar(x, y))
        if n is not None:
           # dx = max(x, destx) - min(x, destx)

    #        print "explorando nodo " + str(x) + ", "+str(y)
            dx = math.fabs( x -destx)
     #       print " dx  = ox " +str(x) +" destx " + str(destx)
            dy = math.fabs( y -desty)
      #      print " dy  = oy "  +str(y) +" desty " + str(desty)

            if self.modoDiagonal == True :
                if dx > dy:
                    H = 1.41*dy + (dx-dy);
       #             print "dx llega diagonal  H" + str( H)
                else:
                    H = 1.41*dx + (dy-dx);
        #            print "dY llega diagonal  H" + str( H)
            else:
                H = dx + dy
            heuristica = H
         #   print " heuristica " +str( heuristica)

            n.gScore += nodoAnterior.gScore
            n.fScore = n.gScore + heuristica
            n.parent = nodoAnterior
            #print "**** score  f actual:" + str(n.fScore)
            #print "**** score  g actual:" + str(n.gScore)
            return n

        return None
