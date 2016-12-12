import turtle
t = turtle.Pen()
t.tracer(500)

LIMIT  = 12
SCALAR = 0.5 * (2 ** 0.5)


def drawTree(size, depth):
    drawSquare(size, depth / float(LIMIT))
    
    if depth + 1 <= LIMIT:
        t.left(90)
        t.forward(size)
        t.right(45)
        drawTree(size * SCALAR, depth + 1)
    
        t.forward(size * SCALAR)
        t.right(90)
        drawTree(size * SCALAR, depth + 1)
    
        t.left(90)
        t.backward(size * SCALAR)
        t.left(45)
        t.backward(size)
        t.right(90)
        

def drawSquare(sideLength, darkness):
#    t.fillcolor(1.0 - darkness, 0.5, 1.0 - darkness)
    
    t.fill(True)
    for i in range(4):
        t.forward(sideLength)
        t.left(90)
    t.fill(False)


t.up(); t.goto(-100, -350); t.down()
drawTree(170.0, 0)

raw_input()
