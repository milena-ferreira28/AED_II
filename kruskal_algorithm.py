import heapq

#---------------------------------MAIN---------------------------------------
def main():
    print("\n----------MENU----------\n")
    print("1. Dijkstra (caminho mínimo entre dois vértices)\n")
    print("2. Kruskal (Árvore Geradora Mínima)\n")
    print("3. Sair\n")
    print("ATENÇÃO: Dijkstra usa grafos direcionados e Kruskal grafos não direcionados!\n")
    while True:
        try:
            opcao = int(input("\nEscolha uma opção: "))
            if opcao in [1, 2, 3]:
                break
            print("Opção inválida!")
        except ValueError:
            print("Digite um número válido!")

#----------Se escolher opção 1, executa instruções referente ao Dijkstra----------
    if opcao == 1:
#Chama a função que lê o grafo direcionado
        grafo = ler_grafo_direcionado()
        if not grafo:
            return
#Vértice origem:
        origem = input("Vértice de origem: ").strip().upper()
        while origem not in grafo:
            print("Origem inválida!")
            origem = input("Vértice de origem: ").strip().upper()
#Vértice destino:
        destino = input("Vértice de destino: ").strip().upper()
        while destino not in grafo:
            print("Destino inválido!")
            destino = input("Vértice de destino: ").strip().upper()
#Chama a função Dijkstra:
        distancias, anterior = dijkstra(grafo, origem)
#Chama a função que refaz o caminho:
        caminho = rec_caminho(anterior, origem, destino)
#Resultados:
        print(f"Distância mínima de {origem} para {destino}: {distancias.get(destino, 'infinito')}")
        print(f"Caminho: {caminho}")

#----------Se escolher opção 2, executa instruções referente ao Kruskal----------
    elif opcao == 2:
#Chama a função que lê o grafo não direcionado:
        grafo = ler_grafo_nao_direcionado()
        if not grafo:
            return
        
#Chama a função Kruskal:
        mst, peso_total = kruskal(grafo)
#Resultados:
        print("\nÁrvore Geradora Mínima:\n")
        print(f"Peso total: {peso_total} \nNúmero de arestas {len(mst)}")
        print("\nArestas selecionadas:")
#Imprime as arestas selecionadas e o peso de cada:
        for i, (v1, v2, peso) in enumerate(mst, 1):
            print(f"{i}. {v1} <-> {v2} (peso: {peso})")
#Imprime todas as arestas ordenadas e mostra o status se foi ou não selecionada para a MST
        print("\nTodas as arestas ordenadas:")
        arestas = extrair_arestas(grafo)
        for peso, v1, v2 in arestas:
            status = "SELECIONADA" if (v1, v2, peso) in mst or (v2, v1, peso) in mst else "REJEITADA"
            print(f"{v1} <-> {v2}: peso {peso} - {status}")

#----------Se escolher opção 3 fecha o programa---------
    elif opcao == 3:
        print("Encerrando programa...")
        return
    else:
        print("Opção inválida!")
        opcao = int(input("\nEscolha uma opção: ")).strip()
    
#----------------------------------------------LEITURA GRAFO-------------------------------------------------------------

#----------Grafo Direcionado----------
def ler_grafo_direcionado():
    grafo = {}
    while True:
        try:
#Usuário insere o npumero de vértices que quer:
            num_vertices = int(input("Digite o número de vértices (máx. 20): "))
            if 0 < num_vertices <= 20:
                break
            print("Número de vértices inválido! Deve ser entre 1 e 20.")
        except ValueError:
            print("Digite um número válido!")
    
    vertices = []
    for i in range(num_vertices):
        while True:
#Nome dos vértices:
            nome = input(f"Nome do vértice {i+1} (apenas letras): ").strip().upper()

#Verifica se o nome de cada vértice é uma letra
            if nome.isalpha() and len(nome) > 0:
#Verifica se o nome ja nao foi usado
                if nome not in vertices:
                    vertices.append(nome)
                    break
                else:
                    print(f"O nome '{nome}' já foi usado! Escolha outro ou variações (ex. AA).")
            else:
                print("O nome deve conter SOMENTE LETRAS (sem números, símbolos, espaço, etc.).")
#Usuário digita o peso de cada aresta:
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
# A -> B peso 3 
                        grafo[origem][destino] = peso
                    break  
                except ValueError:
                    print("Digite um número válido!")
    return grafo

#----------Grafo Não Direcionado----------
def ler_grafo_nao_direcionado():
    grafo = {}
    while True:
        try:
#Usuário digita o número de vértices que quer (não limitei a 20 como o Dijkstra)
            num_vertices = int(input("Digite o número de vértices: "))
            if num_vertices > 0:
                break
            print("Número de vértices deve ser maior que 0!")
        except ValueError:
            print("Digite um número válido!")

    vertices = []
    for i in range(num_vertices):
        while True:
            nome = input(f"Nome do vértice {i+1} (apenas letras): ").strip().upper()
#Verifica se o nome é uma letra
            if nome.isalpha() and len(nome) > 0:
#Verifica se o nome ja não foi usado
                if nome not in vertices:
                    vertices.append(nome)
                    break
                else:
                    print(f"O nome '{nome}' já foi usado! Escolha outro ou variações (ex. AA).")
            else:
                print("O nome deve conter SOMENTE LETRAS (sem números, símbolos, espaço, etc.).")
    
    for vertice in vertices:
        grafo[vertice] = {}
#Usuário digita o peso das arestas:
    print("\nDigite os pesos das arestas (0 se não houver conexão):")
    for i, origem in enumerate(vertices):
        for j, destino in enumerate(vertices):
            if i < j: #Não permite loops
                while True:
                    try:
                        peso = int(input(f"{origem} <-> {destino}: "))
                        if peso < 0:
                            print("O peso não pode ser negativo! Digite novamente.")
                            continue
                        if peso > 0:
# A <-> B peso 3 (ou seja, A -> B = B -> A)
                            grafo[origem][destino] = peso
                            grafo[destino][origem] = peso
                        break  
                    except ValueError:
                        print("Digite um número válido!")
    return grafo

#-----------------------------------------DIJKSTRA----------------------------------------
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

#-------------------------------------REC CAMINHO--------------------------------------
#Recontroi o caminho mais curto ate o destino
def rec_caminho(anterior, origem, destino):
    caminho = [] #Lista ra armazenar o caminho
    node = destino #Começa no destino e vai voltando até a origem

#Reconstrói o caminho de trás pra frente:
    while node != origem and node is not None:
        caminho.append(node) #Adiciona vértice atual ao caminho
        node = anterior.get(node, None) #Procura o vertice anterior 
        if node is None:
            return f"Não há caminho de {origem} para {destino}"
        
#Saiu do while = chegou a origem      
    caminho.append(origem)
#Retorna o caminho na ordem certa (origem -> destino)
    return ' -> '.join(reversed(caminho))

#---------------------------------------Extrair Arestas-----------------------------------------------------
#Converte o grafo em lista de arestas ordenadas por peso
#retorna: [(peso, vertice1, vertice2), ...]
def extrair_arestas(grafo):
    arestas = []  #lista vazia para armazenas as tuplas (peso, vertice1, vertice2)
    
    vertices_processados = set()  #cria conjunto vazio com set para evitar duplicatas
#Percorre cada vértice do grafo:
    for origem in grafo:  
#Pra cada vérticec, pega todos os seus vizinhos:
        for destino, peso in grafo[origem].items(): 
#Par = lista tupla de origem e destino em ordem alfabética (A-B e B-A sao a mesma coisa)
            par = tuple(sorted([origem, destino])) 
            if par not in vertices_processados:  #se o par nao foi processado
                arestas.append((peso, origem, destino)) #adiciona tupla com peso, origem e destino no final da lista
                vertices_processados.add(par) #Adiciona o par a lista de vertices processados
#Ordena por peso (o primeiro elemento da tupla)
    return sorted(arestas)

#-------------------------------------------UnionFind-----------------------------------
class UnionFind():
    def __init__(self, vertices):
#Iniciliza cada vértice em seu próprio grupo
        self.lider = {} # vértice líder

#No início, cada vértice é lider de si mesmo
        for  vertice in vertices:
            self.lider[vertice] = vertice
    
    def find(self, vertice):
#Encontra o líder do grupo
        if self.lider[vertice] != vertice:
#Se não é lider de si mesmo, procura o líder
            return self.find(self.lider[vertice])
        return vertice
    
    def union(self, v1, v2):
#Une os grupos de vertice1 e vertice2
        raiz1 = self.find(v1)
        raiz2 = self.find(v2)

        if raiz1 != raiz2:
#grupos diferentes, une eles:
            self.lider[raiz1] = raiz2
            return True
        else:
            return False
            
#------------------------------------KRUSKAL------------------------------
def kruskal(grafo):
#Chama função pra extrair e ordenar as arestas
    arestas = extrair_arestas(grafo)

#Chama a função para inicializar Union-Find
    vertices = list(grafo.keys())
    uf = UnionFind(vertices)

#Lista para guardar as arestas da Árvore Gerador Mínima
    mst = []
    peso_total = 0

#Para cada aresta (ordem crescente de peso)
    for peso, v1, v2 in arestas:
#Se os vértices estão em grupos diferentes
        if uf.union(v1, v2):  #union retorna True se conseguiu unir
            mst.append((v1, v2, peso))
            peso_total += peso
            
#Se já tem n-1 arestas, para
            if len(mst) ==len(vertices) - 1:
                break

    return mst, peso_total


if __name__ == "__main__":
    main()