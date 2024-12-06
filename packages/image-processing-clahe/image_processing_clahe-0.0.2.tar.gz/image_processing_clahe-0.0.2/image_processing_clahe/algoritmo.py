# pip install opencv-python
# pip install matplotlib

import cv2
import matplotlib.pyplot as plt

def process_image(image_path):

    # Carrega a imagem 
    img = cv2.imread(image_path) # flags: cv2.IMREAD_COLOR (padrão quando não forem definidas)
    
    # Verifica se a imagem foi carregada corretamente
    if img is None:
        raise ValueError(f"Não foi possível carregar a imagem do caminho: {image_path}")
    else:
        print("Imagem carregada com sucesso!")
    
    # Separa os canais de cor, convertendo de BGR para o espaço de cor LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab) #l: luminancia, a:green-red, b: blue-yellow

    # Cria o objeto CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) #aumento de contraste limitado a 2.0; tiles com blocos de 8x8 pixels
    clahe_l = clahe.apply(l) #aplicado somente em "L" que é a luminancia

    # Recombina os canais
    lab_clahe = cv2.merge((clahe_l, a, b)) #faz o merge entre o canal "l" que sofreu o CLAHE e os demais canais "a" e "b"
    final_img = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR) # converte novamente para BGR

    return img, final_img

def plot_img(img, final_img):

    # Visualiza a imagem original e a processada.
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Imagem Original')
    plt.xlabel('Pixels')
    plt.ylabel('Pixels')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB))
    plt.title('Imagem processada com CLAHE')
    plt.xlabel('Pixels')
    plt.ylabel('Pixels')

    plt.show()

 