import cv2 as cv # Importa a biblioteca OpenCV para manipulação de imagens
import numpy as np # Importa a biblioteca NumPy para manipulação de arrays
from google.colab.patches import cv2_imshow  # Importa a função cv2_imshow para exibição de imagens no Google Colab

img = cv.imread("imagem1.png") # Carrega a imagem a ser usada
imagemConvertida = "imagemconvertida.png" # Define o nome do arquivo da imagem convertida

# Função para converter um número inteiro em uma lista de bits
def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

# Função para gerar a mensagem em formato de array de bits
def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m) # Converte o caractere para seu valor ASCII
        bits = bitfield(val) # Converte o valor ASCII para bits

        if len(bits) < 8:  # Garante que cada caractere tenha 8 bits
            for a in range(8-len(bits)):
                bits.insert(0,0)
        lista.append(bits)
    arr = np.array(lista) # Cria um array NumPy a partir da lista de bits
    arr = arr.flatten() # Achata o array para uma única dimensão
    return arr

# Função para converter a mensagem de um array de bits para uma string
def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8)) # Redimensiona o array para formato (n, 8)
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i)) # Calcula o valor decimal do byte
        mensagem_out += chr(sum) # Converte o valor decimal para caractere
    return mensagem_out

# Função para esconder a mensagem na imagem
def esconder_mensagem(mensagem):
  imgAltera = img.copy() # Cria uma cópia da imagem original
  altura, largura, x = img.shape # Obtém as dimensões da imagem
  tamanho_mensagem = len(mensagem)
  print("tamanho da mensagem = "+str(tamanho_mensagem))
  pos = 0

  for i in range(altura):
        for j in range(largura):
            if tamanho_mensagem > pos:
                p = img[i][j][2] # Obtém o valor do pixel no canal vermelho
                valor = ((p // 10) * 10) + mensagem[pos] # Altera o valor do pixel para esconder o bit da mensagem
                imgAltera[i][j][2] = valor
            elif tamanho_mensagem == pos:
                imgAltera[i][j][2] = ((p // 10) * 10) + 2 # Marca o fim da mensagem com um valor especial
            pos = pos + 1

  cv2_imshow(imgAltera)
  cv.imwrite(imagemConvertida, imgAltera) # Exibe a imagem alterada
  cv.waitKey(0) # Salva a imagem alterada

# Função para encontrar a mensagem escondida na imagem
def encontra_mensagem():
    img2 = cv.imread(imagemConvertida) # Carrega a imagem convertida
    altura, largura, x = img.shape
    mensagem = []
    for i in range(altura):
        for j in range(largura):
            p = img2[i][j][2] # Obtém o valor do pixel no canal vermelho
            # print(p)
            if (p % 10) < 2:
                mensagem.append(p % 10) # Adiciona o bit da mensagem ao array
            elif (p % 10) >= 2:
                print("Mensagem encontrada: ")
                print(converter_mensagem(mensagem)) # Converte os bits de volta para a mensagem original
                return mensagem

# Texto a ser escondido na imagem
texto = "Se alguma coisa pode dar errado, dará"
# Gera o array de bits da mensagem
arrayBits = gerar_mensagem(texto) 
print("mensagem em binario = " + str(arrayBits))
esconder_mensagem(arrayBits) # Esconde a mensagem na imagem
encontra_mensagem()  # Encontra e exibe a mensagem escondida
cv2_imshow(img) # Exibe a imagem original
