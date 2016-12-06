bulletX = 0
bulletY = 0
bulletUp = 0
targetX = 640
targetY = random(50,400)
score = 0
lives = 3

def setup():
    size(640,480)
    textSize(32)
  
def draw():
    global bulletX, bulletY, bulletUp, targetX, targetY, score, lives
    if lives <= 0:
        background("#000000")
    else:
        background("#FFFFFF")
        fill("#000000")
        text(score, 0, 470)
        text(lives, 600, 470)
        fill("#00FF00")
        rectMode(CENTER)
        rect(25,mouseY,50,50)
        if bulletUp == 1:
            fill("#0000FF")
            ellipse(bulletX,bulletY,10,10)
            bulletX = bulletX + 10
            if dist(bulletX,bulletY,targetX,targetY) < 5+25:
                bulletUp = 0
                targetX = 640
                targetY = random(50,400)
                score = score + 10
            if bulletX > width:
                bulletUp = 0
        targetX = targetX - 5
        if targetX < 0:
            targetX = 640
            targetY = random(50,400)
            lives = lives - 1
        fill("#FF0000")
        ellipse(targetX,targetY,50,50)
        
def mousePressed():
    global bulletX, bulletY, bulletUp
    if bulletUp == 0:
        bulletUp = 1
        bulletX = 50
        bulletY = mouseY
