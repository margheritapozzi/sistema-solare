import pygame
import math
pygame.init()


width, height = 1000, 1000 #px dello schermo in cui si visualizzerà la simulazione
finestra = pygame.display.set_mode((width, height)) #schermo
pygame.display.set_caption("Simulazione pianeti") #titolo della finestra in cui si visualizzerà la simulazione

# colori
bluscuro=(1, 1, 18)#colore sfondo
bianco=(255,255,255) #così a caso
giallo=(237, 207, 12) #colore sole
grigio=(156, 145, 143)#colore mercurio, a quanto pare mercurio è grigio, non so per quale motivo io ero convinta fosse marrone/rosso boh saranno i poteri forti che lo hanno ridipinto negli ultimi anni
griallo=(176, 170, 125)#colore venere
bluette=(37, 124, 156)#colore terra
rossancio=(186, 91, 17)#colore marte, ho appena realizzato che non devo dare nomi troppo stupidi e a caso perchè poi non me li ricordo e quando li devo usare devo continuare ad andare a vedere come si chiamano sti cosi :(
mariallo=(199, 164, 133)#colore giove
giagio=(214, 212, 191)#colore saturno
azzurro=(168, 221, 224)#colore urano, effettivamente potrei anche non scrivere ogni volta colore visto che si trova nella sezione colori mmmm
blu=(46, 149, 209)#colore nettuno
aranmarronero=(161, 149, 129)#colore plutone, 1° #JUSTICEFORPLUTONE  2° sto coso ha 18 colori diversi quindi ne ho scelto uno a caso


class Pianeta:
    
    AU = 1.496e6 *1000 # unità astronomica: distanza in metri dalla terra dal sole
    G = 6.67428e-11 #costante gravitazionale
    SCALA = 250/AU  # scala del gioco è 250 px equivale a 1 AU 
    TEMPO = 3600*24 #tempo in secondi che voglio che sia preso in considerazione, in questo caso 1 giorno -> quindi la simulazione userà come dato la posizione di ogni giorno, non ogni secondo se no esplode tutto :)
    def __init__(self,x,y,raggio, colore, massa): #definisce i vari valori che serviranno
        self.x=x
        self.y=y
        self.raggio=raggio
        self.colore=colore
        self.massa=massa
        
        self.orbita=[]
        self.sole=False
        self.distanza_da_sole=0
        
        self.x_vel=0
        self.y_vel=0

    def draw(self, finestra):
        x = self.x*self.SCALA + width/2 #così le misure non risultino troppo grandi, aggiungere la larghezza dello schermo/2 perchè con 0,0 come coordinate si intende l'angolo in alto a sinistra, quindi bisogna spostarlo manualmente al centro dello schermo
        y = self.y*self.SCALA + height/2
        
        pygame.draw.circle(finestra, self.colore, (x,y), self.raggio) 
        
    def attrazione(self, other): #per calcolare la forza attrattiva tra un pianeta e un altro corpo
        other_x, other_y = other.x, other.y
        distanza_x = other_x - self.x #sottrarre l'uno dall'altro, non cambia l'ordine tanto poi si ^2 quindi diventa sempre positivo e si trova la compoente x del raggio
        distanza_y = other_y - self.y
        distanza= math.sqrt(distanza_x**2 + distanza_y**2)
        
        if other.sole:
            self.distanza_da_sole = distanza #così da salvare il dato e così lo possiamo scrivere sullo schermo, che in realtà è brutto e quindi non lo faremo 
            
        forza = self.G * self.massa * other.massa /distanza**2 #la formula della forza gravitazionale: F=GMm/r^2
        alpha = math.atan2(distanza_y, distanza_x)#angolo tra la F e Fx, atan è arctan non so perhcè ci sia un 2 ma noi non ci facciamo domande

        forza_x = math.cos(alpha)*forza #componente orizzontale di F
        forza_y = math.sin(alpha)*forza #componente verticale di F
        
        return forza_x, forza_y

    def update_position(self, planets):
        total_fx=total_fy = 0 #non ho capito
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attrazione(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.massa * self.TEMPO #da F=ma 
        self.y_vel += total_fy / self.massa * self.TEMPO 
        
        self.x += self.x_vel * self.TEMPO
        self.y += self.y_vel * self.TEMPO
        self.orbita.append((self.x, self.y))
        
def main():
    run=True
    clock = pygame.time.Clock()
    
    #pianetiiiiiii
    
    sole = Pianeta(0,0, 40, giallo, 1.98892 * 10**30 ) #il raggio credo sia preso a caso però poi possiamo prenderli quelli veri, solo che mi sa che viene un po troppo grosso il sole e gli altri troppo piccini quindi dovremmo provare e vedere se ha senso come cosa
    sole.sole = True
    
    mercurio = Pianeta(0.387 * Pianeta.AU, 0, 8, grigio, 3.30 * 10**23)#tutte le misure assolutamente copiate dal boss
    
    venere = Pianeta(0.723 * Pianeta.AU, 0, 14, griallo, 4.8685 * 10**24)
    
    terra = Pianeta(1 * Pianeta.AU, 0, 16, bluette, 5.9742 * 10**24)
    
    marte = Pianeta(1.524 * Pianeta.AU, 0, 12, rossancio, 6.39 * 10**23)
    
    
    planets=[sole, mercurio, venere, terra, marte, ]
    
    for planet in planets:
        planet.sole= False
    
    while run:
        
        clock.tick(60) #massimo di reload per secondo del gioco, così non la velocità del gioco non dipende dalla velocità del processore che si utilizza
        finestra.fill(bluscuro)
        
        for event in pygame.event.get(): #se l'utente clicca la X per chiudere la finestra, se no va avanti all'infinito
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(finestra)
            
        pygame.display.update()
        
    pygame.quit()
    
main()
