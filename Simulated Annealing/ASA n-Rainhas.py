import math
import random
import time
import numpy as np
from matplotlib import patches, pyplot as plt

historico_de_ataques = []

def gera_estado_inicial(n):
    board = [random.randint(0, n-1) for _ in range(n)]
    return board

def calcula_ataques(n, board):
    h = 0
    for i in range(n):
        for j in range(i+1, n):

            if board[i] == board[j]:   # checagem de rainhas na mesma linha
                h += 1

            offset = j - i

            # checagem das diagonais
            if (board[j] == board[i]-offset) or (board[j] == board[i] + offset):
                h+=1

    return h

def move(n, board, h, temperature):
    boardTemperature = list(board)
    found = False
  
    while not found:
        boardTemperature = list(board)

        # seleciona um movimento aleatório
        new_row = random.randint(0,n-1)
        new_col = random.randint(0,n-1)
        boardTemperature[new_col] = new_row
        new_h = calcula_ataques(n, boardTemperature)

        # se o movimento for otimo, aceita
        if new_h < h:
            found = True
        else:
            # senão, calcula o risco
            # se for arriscado rejeita(continua o laço), senão aceita
            delta_e = h - new_h
            accept_prob = min(1,math.exp(delta_e/temperature))
            found = random.random() <= accept_prob
    
    return boardTemperature


def simulatedAnnealing(n):
    global historico_de_ataques
    
    inicio = time.time()
    
    board = gera_estado_inicial(n)
    h = calcula_ataques(n, board)
    historico_de_ataques.append(h)
    
    temperature = n**2
    cooling_rate = 0.95
    steps = 0
    
    while h > 0:
        board = move(n, board,h, temperature)
        h = calcula_ataques(n, board)
        historico_de_ataques.append(h)
        
        # diminui aceitavelmente a temperatura
        n_temp = max(temperature * cooling_rate,0.01)
        temperature = n_temp

        steps += 1
        if steps >= 2000:
            break

    fim = time.time()
    return steps, board, (fim - inicio)

if __name__ == "__main__":
    historico_de_ataques = []
    total_ataques = []

    queens = 32
    rodadas = 5

    for ex in range(rodadas):
        print(f'======== RODADA {ex+1} ========')

        steps, board, tempo = simulatedAnnealing(queens)
            
        h = calcula_ataques(queens, board)
        total_ataques.append(h)
            
        minutos = int(tempo/60)
        segundos = float(tempo%60)
            
        print(f"Conflitos: {h}")
        print(f'Tempo -> {minutos} m {segundos} s')
        print(f"número de passos: {steps}")

        if h != 0:
            print("Limite de movimentos atingido")
        else:
            print("Estado objetivo alcançado")
        
        print(f'============================\n')
        
    qualidade_solucoes = sum(total_ataques) / rodadas
    print('QUALIDADE DAS SOLUCOES ', qualidade_solucoes)