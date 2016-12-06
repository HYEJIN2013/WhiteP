def do_turn(pw):
    source = None

    source_num_ships = 0
    my_planets = pw.my_planets()
    dest = -1
    dest_score = -999999
    srcR = -1
    list = pw.not_my_planets()
    if(0 < len(list) < 2):
        for p in my_planets:
            if(p.num_ships() > 100):
                pw.issue_order(p, list[0], 3 * p.num_ships() / 5)
        return None            
    for p in list:
        source_score = -999999
        for p1 in my_planets:
            score = 1.0 * p1.num_ships() * (p.growth_rate() + 1) / (1 + pw.distance(p, p1)) / (1 + p.num_ships())
            if score > source_score:
                source_score = score
                source = p1.planet_id()
                source_num_ships = p1.num_ships()

        if source_score > dest_score:
            dest_score = score
            dest = p.planet_id()
            srcR = source
            srcRN = source_num_ships
    if srcR >= 0 and dest >= 0:
        if(srcRN > 1000):
            num_ships = 4 * srcRN / 5
        elif(srcRN > 100):
            num_ships = 3 * srcRN / 4
        else:
            num_ships = srcRN / 2
        pw.issue_order(srcR, dest, num_ships)
