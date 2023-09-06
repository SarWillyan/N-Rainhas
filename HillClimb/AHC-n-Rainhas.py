import random
import time
from matplotlib import patches, pyplot as plt
import numpy as np

attack_history = []

#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*
#*--*                                                             *--*

def plot_attacks(attack_history):
    plt.plot(attack_history, marker='o')
    plt.xlabel('Iterações totais')
    plt.ylabel('Número de Ataques')
    plt.title('Variação do Número de Ataques durante as Execuções')
    plt.grid(True)
    plt.show()
    
def plot_solution(solution, N):
    fig = plt.figure()
    #fig.set_size_inches(20, 20)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim((0, N))
    ax.set_ylim((0, N))

    # Adicionar quadriculado
    for i in range(N):
        for j in range(N):
            color = 'white' if (i + j) % 2 == 0 else 'black'
            ax.add_patch(patches.Rectangle((j, i), 1, 1, color=color))
    
    count = 0
    for queen in solution:
        ax.add_patch(patches.Circle((queen + 0.5, count + 0.5), radius=0.4, fill=True, color='red'))
        count += 1
    plt.show()
    
#*--*                                                             *--*
#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*

#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*
#*--*                                                             *--*

def calcular_ataques(estado):
    ataques = 0
    for i in range(len(estado)):
        for j in range(i + 1, len(estado)):
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == j - i:
                ataques += 1
    return ataques

def gerar_estado_inicial(N):
    return [random.randint(0, N - 1) for _ in range(N)]

def hill_climb_N_queens(N):
    global attack_history
    inicio = time.time()
    estado_atual = gerar_estado_inicial(N)
    melhor_ataques = calcular_ataques(estado_atual)
    attack_history.append(melhor_ataques)
    total_iteracoes = 0
    
    while melhor_ataques > 0:
        melhor_vizinho = None
        
        for coluna in range(N):
            for linha in range(N):
                if estado_atual[coluna] != linha:
                    estado_vizinho = list(estado_atual)
                    estado_vizinho[coluna] = linha
                    ataques_vizinho = calcular_ataques(estado_vizinho)
                    
                    if ataques_vizinho < melhor_ataques:
                        melhor_vizinho = estado_vizinho
                        melhor_ataques = ataques_vizinho
                        total_iteracoes += 1
        
        if melhor_vizinho is None:
            break
        
        estado_atual = melhor_vizinho
        attack_history.append(melhor_ataques)
    fim = time.time()
    return estado_atual, (fim - inicio), total_iteracoes

#*--*                                                             *--*
#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*

#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*
#*--*                                                             *--*

if __name__ == '__main__':
    # Exemplo de uso:
    N = 128 # Número de rainhas e tamanho do tabuleiro
    rodadas = 5
    conflitos_tot = []

    for _ in range(rodadas):
        print(f'======== RODADA {_} ========')
        solucao, tempo, iteracoes = hill_climb_N_queens(N)
        conflitos = calcular_ataques(solucao)
        conflitos_tot.append(conflitos)
        min = int(tempo/60)
        sec = float(tempo%60)
        print(f'Conflitos: {conflitos}')
        print(f'Tempo -> {min} m {sec} s')
        print(f'Total de iterações: {iteracoes}')
        print(f'============================\n')

    qualidade_solucoes = sum(conflitos_tot) / rodadas
    print('QUALIDADE DAS SOLUCOES ', qualidade_solucoes)
    
    #-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*
    # Plot da solução encontrada no tabuleiro
    # Usar para somente uma execução, ou criar 
    # uma estrutura para armazear várias soluções
    # plot_solution(solution=solucao, N=N)
    
    # Plot da variação dos ataques durante a execução
    # atk = np.sort(attack_history)[::-1]
    plot_attacks(attack_history)
    
#*--*                                                             *--*
#-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*---*-*-*-*-*-*-*-*-*-*-*-*