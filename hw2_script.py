from hw2_207931536_208336321 import *


if __name__ == '__main__':
    wormhole = cv2.imread(r'blank_wormhole.jpg')
    im = cv2.cvtColor(wormhole, cv2.COLOR_BGR2GRAY)

    T = find_transform(src_points, dst_points)
    print(T)
    new_image = create_wormhole(im, T, iter=5)

    #new_image = trasnform_image(im, T)

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(im, cmap='gray')
    plt.title('original image')
    plt.subplot(1, 2, 2)
    plt.imshow(new_image, cmap='gray')
    plt.title('wormhole image')

    plt.show()
