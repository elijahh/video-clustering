import matplotlib.pyplot as plt
import numpy as np
import scipy.misc


M = 8
N = 8


def loadAndProcessImage(filename):
    img = scipy.misc.imread(filename)
    img = np.dot(img[:,:,:3], [.299, .587, .114]) # grayscale
    img = scipy.misc.imresize(img, (M, N))
    plt.imshow(img, cmap=plt.get_cmap('gray'))
    plt.show()
    return img


def aHash(img):
    return sum((1 << i) for i, j in enumerate(img.flatten()) if j >= np.mean(img))


def dHash(img):
    flatImg = img.flatten()
    return sum((1 << i) for i, j in enumerate(flatImg) if flatImg[i] >= flatImg[i-1])


def compareImages(img1, img2, algo):
    bitstrlen = len(img1.flatten())
    if bitstrlen != len(img2.flatten()):
        return -1
    hash1 = algo(img1)
    hash2 = algo(img2)
    ham = 0
    for i in range(bitstrlen)[::-1]:
        bit1 = hash1 >> i
        bit2 = hash2 >> i
        if bit1 != bit2:
            ham += 1
        if bit1 == 1:
            hash1 -= (1 << i)
        if bit2 == 1:
            hash2 -= (1 << i)
    return ham
