import heapq

def main():
    grafo = ler_grafo()
    if not grafo:
        return
    
    origem = input("Vértice de origem: ").strip().upper()
    while origem not in grafo:
        print("Origem inválida!")
        origem = input("Vértice de origem: ").strip().upper()
    
    destino = input("Vértice de destino: ").strip().upper()
    while destino not in grafo:
        print("Destino inválido!")
        destino = input("Vértice de destino: ").strip().upper()
    
    distancias, anterior = dijkstra(grafo, origem)
    caminho = rec_caminho(anterior, origem, destino)
    print(f"Distância mínima de {origem} para {destino}: {distancias.get(destino, 'infinito')}")
    print(f"Caminho: {caminho}")


def ler_grafo():
    grafo = {}
    while True:
        try:
            num_vertices = int(input("Digite o número de vértices (máx. 20): "))
            if 0 < num_vertices <= 20:
                break
            print("Número de vértices inválido! Deve ser entre 1 e 20.")
        except ValueError:
            print("Digite um número válido!")
    
    vertices = [input(f"Nome do vértice {i+1}: ").strip().upper() for i in range(num_vertices)]
    
    print("\nDigite os pesos das arestas (0 se não houver conexão):")
    for origem in vertices:
        grafo[origem] = {}
        for destino in vertices:
            while True:
                try:
                    peso = int(input(f"{origem} -> {destino}: "))
                    if peso < 0:
                        print("O peso não pode ser negativo! Digite novamente.")
                        continue
                    if peso > 0:
                        grafo[origem][destino] = peso
                    break  
                except ValueError:
                    print("Digite um número válido!")
    return grafo

def dijkstra(grafo, origem):
    
    distancias = {node: float('infinity') for node in grafo}  # Distâncias infinitas
    distancias[origem] = 0  # Distância da origem para ela mesma é 0
    heap = [(0, origem)]  # Fila de prioridade (distância, vértice)
    anterior = {}  # Rastreia o caminho
    
    while heap:
        #Remove o nó com menor distância da fila
        dist_atual, vertice = heapq.heappop(heap)

        #Testa pra saber se o nó ja foi processado, se ja for ignora ele
        if dist_atual > distancias[vertice]:
            continue
        
        #Para cada vizinho do vertice atual
        for vizinho, peso in grafo[vertice].items():
            #Calcula nova distancia
            nova_dist = dist_atual + peso

            #Se encontrou nova distancia, atualiza
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist  #Atualiza distância
                anterior[vizinho] = vertice      #Registra o vertice anterior
                heapq.heappush(heap, (nova_dist, vizinho))   #Adiciona ao heap

    return distancias, anterior                   #Retorna as distancias e o caminho

#Recontroi o caminho mais curto ate o destino
def rec_caminho(anterior, origem, destino):
    caminho = []
    node = destino
    while node != origem and node is not None:
        caminho.append(node)
        node = anterior.get(node, None)
        if node is None:
            return f"Não há caminho de {origem} para {destino}"
        
    caminho.append(origem)
    return ' -> '.join(reversed(caminho))

if __name__ == "__main__":
    main()