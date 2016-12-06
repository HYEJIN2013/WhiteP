# coding: utf-8
import ui
#HW: make traditional chessboard, also, when you tap a square, a queen appears there

v = ui.View(background_color=(0.50, 0.00, 1.00))
board = ui.View()
v.add_subview(board)
v.present('full_screen')
board.frame = ((v.width-v.height), 0, v.height, v.height)
board.corner_radius = 10
board.border_width = 3
board.border_color = (0.00, 1.00, 0.00)
border_color = (.51, .26, .0)

buttons = []

for r in range(8):
	for c in range(8):
		button = ui.Button(title = '')
		if c % 2 == 0 and r % 2 == 0 or r % 2 == 1 and c % 2 == 1:
			button.background_color = (.38, .0, .0)
		else:
			button.background_color = (1,1,1)	
		button.width = v.height/8
		button.height = button.width
		button.corner_radius = 5
		button.border_color = border_color
		button.border_width = 1
		button.x = button.width*c
		button.y = button.height*r
#		button.action = button_pressed 
		board.add_subview(button)
		buttons.append(button)
