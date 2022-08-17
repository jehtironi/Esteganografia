import cv2 as cv
import numpy as np
from google.colab.patches import cv2_imshow 

img = cv.imread("imagem1.png")
imagemConvertida = "imagemconvertida.png"


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8-len(bits)):
                bits.insert(0,0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr


def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i))
        mensagem_out += chr(sum)
    return mensagem_out

def esconder_mensagem(mensagem):
  imgAltera = img.copy()
  altura, largura, x = img.shape
  tamanho_mensagem = len(mensagem)
  print("tamanho da mensagem = "+str(tamanho_mensagem))
  pos = 0

  for i in range(altura):
        for j in range(largura):
            if tamanho_mensagem > pos:
                p = img[i][j][2]
                valor = ((p // 10) * 10) + mensagem[pos]
                imgAltera[i][j][2] = valor
            elif tamanho_mensagem == pos:
                imgAltera[i][j][2] = ((p // 10) * 10) + 2
            pos = pos + 1

  cv2_imshow(imgAltera)
  cv.imwrite(imagemConvertida, imgAltera)
  cv.waitKey(0)

def encontra_mensagem():
    img2 = cv.imread(imagemConvertida)
    altura, largura, x = img.shape
    mensagem = []
    for i in range(altura):
        for j in range(largura):
            p = img2[i][j][2]
            # print(p)
            if (p % 10) < 2:
                mensagem.append(p % 10)
            elif (p % 10) >= 2:
                print("Mensagem encontrada: ")
                print(converter_mensagem(mensagem))
                return mensagem

texto = "Se alguma coisa pode dar errado, dará"
arrayBits = gerar_mensagem(texto)
print("mensagem em binario = " + str(arrayBits))
esconder_mensagem(arrayBits)
encontra_mensagem()
cv2_imshow(img)