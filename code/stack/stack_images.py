size = (10, 10)
imgs = imgs[:size[0] * size[1]].reshape(size[0], size[1], 28, 28)
result = np.vstack(tuple([np.hstack(tuple(img)) for img in imgs]))

imsave('a.png', result)
