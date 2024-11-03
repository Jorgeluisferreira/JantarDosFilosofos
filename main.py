import threading
import time
import random

class MesaDeJantar:
    def __init__(self):
        self.nomes_filosofos = ["Arsenne", "Thanatos", "Izanagi", "Orpheus", "Hermes"]
        self.num_filosofos = len(self.nomes_filosofos)
        self.garfos = [True] * self.num_filosofos  #Todos os garfos começam livres
        self.condicao = threading.Condition()  #criação do monitor

    def pegar_garfos(self, i):
        with self.condicao:
            #Espera até que os dois garfos (à esquerda e à direita) estejam livres
            while not (self.garfos[i] and self.garfos[(i + 1) if (i+1) != self.num_filosofos else 0]):
                self.condicao.wait()  # Espera a liberação dos garfos

            #Define os garfos como ocupados
            self.garfos[i] = self.garfos[(i + 1) if (i+1) != self.num_filosofos else 0] = False
            print(f"{self.nomes_filosofos[i]} pegou os garfos {i} e {(i + 1) if (i+1) != self.num_filosofos else 0}")

    def soltar_garfos(self, i):
        with self.condicao:
            #define os garfos livres
            self.garfos[i] = self.garfos[(i + 1) if (i+1) != self.num_filosofos else 0] = True
            print(f"{self.nomes_filosofos[i]} soltou os garfos {i} e {(i + 1) if (i+1) != self.num_filosofos else 0}")
            self.condicao.notify_all()  #Notifica todos os filósofos aguardando

    def jantar(self, i):
        while True:
            #Filósofo pensa
            print(f"{self.nomes_filosofos[i]} está pensando.")
            time.sleep(random.uniform(1, 3))  

            #Filósofo tenta pegar os garfos para comer
            self.pegar_garfos(i)
            print(f"{self.nomes_filosofos[i]} está comendo.")
            time.sleep(random.uniform(1, 3)) 
            self.soltar_garfos(i)

def main():
    mesa = MesaDeJantar()
    threads = []

    for i in range(mesa.num_filosofos):
        thread = threading.Thread(target=mesa.jantar, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join() #utilizo o join para garantir que o programa principal não se encerre, e mantenha rodando uma vez que o jantar tem um looping infinito

if __name__ == "__main__":
    main()
