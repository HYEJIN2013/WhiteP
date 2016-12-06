from __future__ import print_function
import giantbomb
gb = giantbomb.Api('fe35a7029d3d80722ab9d05d4a9a4c53e115f4f8')

f = open('games.txt', 'w')
for num in range(1,41000):
  try:
    game = gb.getGame(num)
    print('"'+str(game.id)+'"'+',"'+str(game.name)+'","'+str(game.deck)+'"', file=f)
  except Exception, error:
    pass
f.close
