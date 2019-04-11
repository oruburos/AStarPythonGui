

import pygame
from pygame.locals import *
from AStar import *

class AStarEGC:


    #configuracion de interfaz , tamamo de celda y largo de mapa
    grosorLinea= 2
    tamanoScreenAncho = 750
    tamanoScreenAlto = 500
    tamanoBotonAncho= 120
    tamanoBotonAlto= 25
    puntoInicioMenu = 520
    tamanoCelda = 25
    anchoMapa = 20
    altoMapa = 15
    astar = None
    modoDiagonal = False
    debugCasilla = False


#colores del menu
    colores = [(0,0,0),
              (150,150,150),
              (90,90,90),
              (50,50,50),
              (230,50,50),
              (50,50,230),
              (0,0,200)]

    ruta = []

    def initAStar(self,w,h):
        self.mapaActual = []
        self.anchoMapa = w
        self.altoMapa = h
        self.nodoInicio = [0,h/2]
        self.nodoFin = [w-1,h/2]
        self.astar = None

        size = w*h;
        for i in range(size):
            self.mapaActual.append(1)



        self.mapaActual[(self.nodoInicio[1]*w)+self.nodoInicio[0]] = 4 #color d einicio
        self.mapaActual[(self.nodoFin[1]*w)+self.nodoFin[0]] = 5#color de nodo fin


        self.zonaMapaGUI = Rect(0,0,w*self.tamanoCelda,h*self.tamanoCelda)


    def encuentraRutaGUI(self):

        astar = AStar(self.mapaActual,self.anchoMapa,self.altoMapa , self.modoDiagonal  )
        start = Lugar(self.nodoInicio[0],self.nodoInicio[1])
        end = Lugar(self.nodoFin[0],self.nodoFin[1])

        self.repaint()
        self.drawMapa()
        self.pintaGUI()

        if pygame.font:
          font = pygame.font.SysFont("Arial", 20)
          text = font.render( "" , 1, (10, 10, 10))
          self.screen.blit(text, text.get_rect(centery=self.screen.get_height()-20))

        p = astar.encuentraRuta(start,end)
        text = font.render( "" , 1, (10, 10, 10))
        self.screen.blit(text, text.get_rect(centery=self.screen.get_height()-20))

        if not p:
            if pygame.font:
                font = pygame.font.SysFont("Arial", 36)
                text = font.render("No hay ruta!", 1, (10, 10, 10))
                textpos = text.get_rect(centerx=self.screen.get_width()/2+100 , centery = 230)
                self.screen.blit(text, textpos)

        else:

            if pygame.font:
                font = pygame.font.SysFont("Arial", 22)
              #  print " movimientos" +str( len(p.getNodos()))+ " Costo: " + str(p.getCostoTotal())
                text = font.render( ("Se encontro ruta :  movimientos "+ str( len(p.getNodos())) + " Costo: " + str(p.getCostoTotal()) ) , 1, (10, 10, 10))
                self.screen.blit(text, text.get_rect(centery=self.screen.get_height()-20))


            self.ruta = []
            self.ruta.append((start.x*self.tamanoCelda+self.tamanoCelda/2,start.y*self.tamanoCelda+self.tamanoCelda/2))
            for n in p.getNodos():
                self.ruta.append((n.lugar.x*self.tamanoCelda+self.tamanoCelda/2,n.lugar.y*self.tamanoCelda+self.tamanoCelda/2))
            self.ruta.append((end.x*self.tamanoCelda+self.tamanoCelda/2,end.y*self.tamanoCelda+self.tamanoCelda/2))

    def repaint(self):

        self.screen.fill((120,150,180))
        self.drawMapa()
        self.pintaGUI()


    #meto para dibujar la cuadricula en base a la cantida de celdas y su grosor
    def drawCuadricula(self):

        x = 0
        y = 0

        rect = [0,0,1,self.tamanoCelda]
        rect2 = [0,0,self.tamanoCelda,2]
        for p in self.mapaActual:
            if p == -1:
                p = 0
            rect[0] = x*self.tamanoCelda
            rect[1] = y*self.tamanoCelda
            rect2[0] =rect[0]
            rect2[1] = rect[1]
            #print " rectangulo actual %d %d %d %d" , rect[0],rect[1],rect[2],rect[3]
            pygame.draw.rect( self.screen, (150,0,255), rect )
            pygame.draw.rect( self.screen, (150,0,255), rect2 )
            if (self.debugCasilla ):
                if pygame.font:
                    font = pygame.font.SysFont("Arial", 14)
                    text = font.render(""+str(x)+","+str(y) , 1, (10, 10, 10))
                    self.screen.blit(text, rect)

            x+=1
            if x>=self.anchoMapa:
                x=0
                y+=1




    def actualizaMapa(self,x,y,v):
        mi = (y*self.anchoMapa)+x
        #print "update " + str( mi)
        if v == 4: # nodoInicio
           if self.mapaActual[mi] != 4 and self.mapaActual[mi] != 5:
                self.mapaActual[(self.nodoInicio[1]*self.anchoMapa)+self.nodoInicio[0]] = 1
                self.screen.fill(self.colores[1],(self.nodoInicio[0]*self.tamanoCelda,self.nodoInicio[1]*self.tamanoCelda,self.tamanoCelda,self.tamanoCelda))
                self.nodoInicio = [x,y]
                self.mapaActual[mi] = 4
                #self.mapaActual[mi] = 1
                self.screen.fill(self.colores[4],(x*self.tamanoCelda,y*self.tamanoCelda,self.tamanoCelda,self.tamanoCelda))
        elif v == 5: # nodoFin
          if self.mapaActual[mi] != 4 and self.mapaActual[mi] != 5:
                self.mapaActual[(self.nodoFin[1]*self.anchoMapa)+self.nodoFin[0]] = 1
                self.screen.fill(self.colores[1],(self.nodoFin[0]*self.tamanoCelda,self.nodoFin[1]*self.tamanoCelda,self.tamanoCelda,self.tamanoCelda))
                self.nodoFin = [x,y]
                self.mapaActual[mi] = 5
                #self.mapaActual[mi] = 1
                self.screen.fill(self.colores[5],(x*self.tamanoCelda,y*self.tamanoCelda,self.tamanoCelda,self.tamanoCelda))
        else:
            if self.mapaActual[mi] != 5 and self.mapaActual[mi] != 6:

                if v == 0:
                    self.mapaActual[mi] = -1
                else:
                    self.mapaActual[mi] = v

                self.screen.fill(self.colores[v],(x*self.tamanoCelda,y*self.tamanoCelda,self.tamanoCelda,self.tamanoCelda))
        self.encuentraRutaGUI()
    def drawMapa(self):

        x = 0
        y = 0
        rect = [0,0,self.tamanoCelda,self.tamanoCelda]
        for p in self.mapaActual:
            if p == -1:
                p = 0
            rect[0] = x*self.tamanoCelda
            rect[1] = y*self.tamanoCelda
            self.screen.fill(self.colores[p],rect)

            #self.screen.drawLines(rect,self.colores[p])

            x+=1
            if x>=self.anchoMapa:
                x=0
                y+=1
        self.drawCuadricula()
    def pintaGUI(self):

        text = ["Obstaculo (-1)", " Nodo facil(1)",  "Nodo medio (2)", "Nodo dificil (3)", "Inicio(4)", "Fin(5)",  "Reinicio"]

        fnt = pygame.font.SysFont("Arial", 15)

        self.menurect = Rect(self.puntoInicioMenu,5,self.tamanoBotonAncho,self.tamanoBotonAlto*len(self.colores))

        rect = Rect(self.puntoInicioMenu,5,self.tamanoBotonAncho,self.tamanoBotonAlto)

        i = 0
        for c in self.colores:
            self.screen.fill(c,rect)
            ts=fnt.render(text[i], 1, (200,200,200))
            trect = ts.get_rect()
            trect.center = rect.center
            self.screen.blit(ts,trect.topleft)
            rect.y+=self.tamanoBotonAlto
            i+=1


    def loopGame(self):

        pygame.init()    

        self.screen = pygame.display.set_mode((self.tamanoScreenAncho, self.tamanoScreenAlto),HWSURFACE)
        pygame.display.set_caption(' Ejemplo IA simbolica: Algoritmo A*')

        self.screen.fill((120,150,180))

        self.initAStar(self.anchoMapa,self.altoMapa)
        self.drawMapa()
        self.editmode = 0

        self.pintaGUI()

        font = pygame.font.SysFont("Arial", 15)
        text = font.render( "Obstaculo seleccionado por default" , 1, (10, 10, 10))
        self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

        while 1:                                                                      
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:          
                    if event.key == K_ESCAPE:
                        return                    

                elif event.type == MOUSEBUTTONDOWN:                    
                    if len(self.ruta):
                        self.ruta=[]
                        self.drawMapa()
                    mx = event.pos[0]
                    my = event.pos[1]
                    if self.zonaMapaGUI.collidepoint(mx,my):
                        self.actualizaMapa(mx/self.tamanoCelda,my/self.tamanoCelda,self.editmode)
                    elif self.menurect.collidepoint(mx,my):
                        my-=self.menurect.y
                        em = my/self.tamanoBotonAlto
                        if em == 0:
                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "Obstaculo" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

                        if em == 1:
                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "NODO Facil" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

                        if em == 2:
                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "NODO Medio" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

                        if em == 3:
                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "NODO Dificil" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

                        if em == 4:

                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "NODO INICIO" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))

                        if em == 5:
                            #print "modo fin"
                            self.editmode = em
                            self.repaint()
                            font = pygame.font.SysFont("Arial", 15)
                            text = font.render( "NODO FIN" , 1, (10, 10, 10))
                            self.screen.blit(text, text.get_rect(centerx = 600 ,centery=self.screen.get_height()-100))


                        elif em == 6: #reset
                            self.repaint()
                            self.initAStar(self.anchoMapa, self.altoMapa )
                            self.drawMapa()
                        else:
                            self.editmode = em
                        
                elif event.type == MOUSEMOTION and event.buttons[0]:            
                    mx = event.pos[0]
                    my = event.pos[1]
                    if self.zonaMapaGUI.collidepoint(mx,my):
                        if len(self.ruta):
                            self.ruta=[]
                            self.drawMapa()
                        self.actualizaMapa(mx/self.tamanoCelda,my/self.tamanoCelda,self.editmode)


            if len(self.ruta):
                pygame.draw.lines(self.screen, (255,255,255,255), 0, self.ruta, self.grosorLinea )
            pygame.display.flip()

def main():
    graficadorAStar = AStarEGC()
    graficadorAStar.loopGame()

 
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
    
