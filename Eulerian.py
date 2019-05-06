#do tworzenia głębokiej kopi przy wyznaczaniu cyklu/ściezki eulera
import copy

#obliczanie ilości wierzchołków
#weierzchołki to ilość obiektów w kolumnie
vertexCount = lambda rows : len(rows)

#obliczanie ilości krawędzi
#ilość krawędzi to ilość wszystkich możliwych krawędzi - ilość braku krawędzi
#to podejście uwzględnia zapis innych liczb od 1 jako krawędzie
edgeCount = lambda rows : int((vertexCount(rows)**2 - sum([row.count(0) for row in rows]))/2)

#obliczanie stopnia wierzchołka
#ilość wierchków minus brak połączenia z nimi
#to podejście uwzględnia zapis innych liczb od 1 jako krawędzie
getDegree = lambda row : vertexCount(row)-row.count(0)

#oblicznie wszystkich stopni
#użycie wyrażenia generującego do utworzenia listy stopni
getDegrees = lambda rows : [getDegree(row) for row in rows]

#funkcja licząca nieparzyste wierzchołki
getNonEvenVertexCount = lambda matrix : list(map(lambda x:x%2,getDegrees(matrix))).count(1)

#funkcja szukająca wierzchołka o nieparztystym stopniu
getNonEvenVertex = lambda matrix : list(map(lambda x:x%2,getDegrees(matrix))).index(1)

#funkcja sprawdzająca czy graf eulerowski poprzez sprawdzenie czy wszystkie wierzchołki parzyste
isEulerianCycle = lambda matrix : getNonEvenVertexCount(matrix)==0 and getDFS(matrix,0)

#funkcja sprawdzająca czy graf półeulerowski poprzez sprawdzenie czy nieparzystych wierzchołków jest mniej niż 3
isEulerianPath = lambda matrix : getNonEvenVertexCount(matrix)<=2 and getDFS(matrix,0)

def inputMatrix():
    matrix=[]
    # input from user
    #pobieram pierwszą linijkę i nastepnie resztę zakładając że macierz jest kwadratowa
    matrix.append(list(map(int,input().split())))
    for i in range(1, len(matrix[0])):
        matrix.append(list(map(int,input().split())))
    return matrix

def getDFS(matrix,startVertex):
    #rozpoczynam odwiedzanie od podanego wierzchołka
    visited=[startVertex]
    pile=[startVertex]
    isCoherent=1

    #odwiedzam dopóki nie stwiedzę że jest nie spójny lub wszystko odwiedze
    while isCoherent and len(matrix)!=len(visited):
        #wstępnie zakładam że jest niespójny
        isCoherent=0
        #sprawdzam krawędzie wierzchołka
        for i in range(len(matrix)):
            if(len(pile) and matrix[pile[len(pile)-1]][i]!=0):
                #jesli wierzchołek jest jest polaczny z jakimś innym to możliwe że jest spójny
                isCoherent=1
                #odwiedzam wierzchołek jeśli jeszcze go nie odwiedzałem
                if(not(i in visited)):
                    visited.append(i)
                    pile.append(i)
                    #po odwiedzeniu wychodzę z pętli
                    break
            #jeśli stos nie równy [] i sprawdziłem już wszystkie krawędzie dla danego wierzchołka to muszę się cofnąć
            if(len(pile) and i==len(matrix)-1):
                del pile[len(pile)-1]
        #jeśli nie moge dojść do jakiegoś wierzchołka to będę się tak długo cofać aż stos=[] i domyślnie uznam graf za niespójny
    #jeśli jest spójny to zwracam listę odwiedzania
    return visited if isCoherent else 0

def delVertex(matrix, vertex):
    #usuwam kolumne
    for j in range(len(matrix)):
        del matrix[j][vertex]

    #usuwam wiersz
    del matrix[vertex]

def getEulerian(matrix):
    #wpisuje tu odwiedzone wierzchołki
    visited=[]
    #jeśli jest cycklem rozpoczynam od pierwszego wierzchołka, jeśli jest sciezką zaczynam od pierwszego nieparzystego, inaczej podaje 0
    if(isEulerianCycle(matrix)):
        visited.append(0)
    elif(isEulerianPath(matrix)):
        visited.append(getNonEvenVertex(matrix))
    else:
        return 0

    #robie kopie macierzy aby nie zmienić oryginału
    tempMatrix=copy.deepcopy(matrix)
    #zapisuje numery wierzchołkow w liście
    vertexInMatrix=list(range(len(matrix)))

    #odwiedzam dopóki z macierzy nie zostanie jeden wierzchołek
    while len(tempMatrix)!=1:
        #ustala obecny wierzchołek na podstawie listy obecnych wierzchołków
        #ponieważ w liście odwiedzonych mam numery wierzchołków odpowiadających oryginalnej macierzy a pracuję na pomniejszanej
        currentVertex = vertexInMatrix.index(visited[len(visited)-1])
        #sprawdzam czy z wierzchołka wychodzi jedna krawędz
        if(tempMatrix[currentVertex].count(1) == 1):
            #dodaje wierzchołek z którym jest połączony odstatni odwiedzony do odwiedzonych
            visited.append(vertexInMatrix[tempMatrix[currentVertex].index(1)])
            #usuwam wierzchołek który który miał 1 krawędz z macierzy
            delVertex(tempMatrix,vertexInMatrix.index(visited[len(visited)-2]))
            #usuwam wierzchołek który który miał 1 krawędz z listy z obecnymi wierzchołkami
            del vertexInMatrix[currentVertex]
        else:
            for i in range(len(tempMatrix)):
                #sprawdzam z jakim wierzchołkiem jest podłączony odwiedzony wierzchołek
                if(tempMatrix[currentVertex][i]!=0):
                    #kopiuje tymczasową macierz tak aby jej nie zmienić
                    testMatrix=copy.deepcopy(tempMatrix)
                    #usuwam testowo krawedz
                    testMatrix[currentVertex][i]=0
                    testMatrix[i][currentVertex]=0
                    #jeśli graf pozostał spójny po usunieciu krawędzi, usuwam krawędz z macierzy tymczasowej
                    # i dodaje wierzchołek który był połaczony tą krawędzią do odwiedzonych
                    # oraz wychodzę z pętli - nie szukam dalej w tym wierchołku
                    if(getDFS(testMatrix,0)):
                        tempMatrix[currentVertex][i]=0
                        tempMatrix[i][currentVertex]=0
                        visited.append(vertexInMatrix[i])
                        break
    #zwracam wierzchołki jakie odwiedzałem
    return visited

#wczytuję macierz
matrix=inputMatrix()

#sprawdzam czy graf jest eulerowski (wypisuje cykl), półeulerowski (wypisuje ścieżkę), nieeulerowski, niespójny
if(isEulerianCycle(matrix)):
    print("Graf jest eulerowski")
    print("Cykl Eulera: ", *getEulerian(matrix))
elif(isEulerianPath(matrix)):
    print("Graf jest półeulerowski")
    print("Ścieżka Eulera: ", *getEulerian(matrix))
elif(getDFS(matrix,0)):
    print("Graf nie jest eulerowski")
else:
    print("Graf jest niespójny")
