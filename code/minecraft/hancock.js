function hancock() {  var d = new Drone(), i, j, k;
  d.up();
  // structure  for (i = 0; i < 36; ++i) { // floors    d.box(blocks.iron, 37, 1, 37).up();    for (j = 0; j < 4; ++j) { // sides      for (k = 0; k < 6; ++k) { // columns         d.box(blocks.iron, 1, 5, 1).fwd();        d.box(blocks.glass_pane, 1, 5, 5).fwd(5);      }      d.turn();    }    d.up(5);  }
  d.box(blocks.iron, 37, 1, 37);  d.move('start').up();
  // faces  for (i = 0; i < 6; ++i) {    for (j = 0; j < 4; ++j) { // sides      // this makes the diamond shape      d.fwd(18);      for (k = 0; k < 18; ++k) {        d.box(blocks.iron).fwd().up();      }      for (k = 0; k < 18; ++k) {        d.box(blocks.iron).up().back();      }      for (k = 0; k < 18; ++k) {        d.box(blocks.iron).back().down();      }      for (k = 0; k < 18; ++k) {        d.box(blocks.iron).down().fwd();      }      d.fwd(18).turn();    }    d.up(36);  }}
