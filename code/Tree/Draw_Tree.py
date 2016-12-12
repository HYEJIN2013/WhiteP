import canvas

def draw_tree(x,y, trunk_thickness, leaf_h, tree_w, trunk_h):
  canvas.begin_path()
  canvas.move_to(x-tree_w/2,y+trunk_h) 
  canvas.add_line(x+tree_w/2,y+trunk_h)
  canvas.add_line(x,y+trunk_h+leaf_h)
  canvas.close_path()
  canvas.set_fill_color(0.25,0.50,0.00)
  canvas.fill_path()
  canvas.set_stroke_color(0.50, 0.25, 0.00)
  canvas.set_line_width(trunk_thickness)
  canvas.draw_line(x,y+trunk_h, x,y)
  
canvas.set_size(1000,600) 
#for i in range(9):
draw_tree(500, 100, 30, 300,150, 120)
