extern void object::Tetris()
{
	/*
	  ######### ####### ######### #######   ###  #######
	  ######### ####### ######### ########  ### ########
	     ###    ###        ###    ###   ### ### ####
	     ###    #####      ###    ########  ###  ######
	     ###    ###        ###    #######   ###     ####
	     ###    #######    ###    ### ###   ### ########
	     ###    #######    ###    ###  ###  ### #######
	
	              #######   ######  #########
	              ######## ###  ### #########
	              ##   ### ###  ###    ###
	              #######  ###  ###    ###
	              ##   ### ###  ###    ###
	              ######## ###  ###    ###
	              #######   ######     ###
	                       BY CLARK
	
	    Commandes:
	      - Touches gauche et droite pour diriger le tetrimino
	      - Touche haut pour faire tourner le tetrimino
	      - Touche bas pour accélérer la chute
	
	      Bon jeu !
	*/
	
	////////////////////////////////////////////////
	////////////// Variables ///////////////////////
	
	int i, j, k;
	int cases[][];
	for(i=0;i<10;i++){
		for(j=0;j<20;j++){
			cases[i][j] = 0;
		}
	}
	
	int tetrimino_tombe = 0;
	int lignes_completees = 0;
	int partie_finie = 0;
	int tetrimino_choisi ,peut_tomber, ligne_incomplete, couleur_tetrimino, couleur_a_peindre, cases_a_colorier;
	float position_x, position_y, rotation_tetrimino, nouvelle_rotation, vitesse;
	string type_tetrimino;
	float score = 0;
	float combo;
	
	dialog("Appuyez sur Enter pour commencer");
	
	while(partie_finie == 0){
		
		// on affiche le score
		message("- - - - - - -");
		message("Score: " + score);
		message("- - - - - - -");
		
		//////////////////////////////////////////////////
		/////////// Création d'un tetrimino //////////////
		
		// on choisit un nouveau tetrimino au hasard
		if(tetrimino_tombe == 0){
			
			tetrimino_choisi = 0;
			while(tetrimino_choisi < 1 or tetrimino_choisi > 7){
				tetrimino_choisi = rand()*7.5;
			}
			
			if(tetrimino_choisi == 1){
				type_tetrimino = "i";
				couleur_tetrimino = 15;
			}
			if(tetrimino_choisi == 2){
				type_tetrimino = "o";
				couleur_tetrimino = 8;
			}
			if(tetrimino_choisi == 3){
				type_tetrimino = "t";
				couleur_tetrimino = 6;
			}
			if(tetrimino_choisi == 4){
				type_tetrimino = "l";
				couleur_tetrimino = 7;
			}
			if(tetrimino_choisi == 5){
				type_tetrimino = "j";
				couleur_tetrimino = 14;
			}
			if(tetrimino_choisi == 6){
				type_tetrimino = "z";
				couleur_tetrimino = 4;
			}
			if(tetrimino_choisi == 7){
				type_tetrimino = "s";
				couleur_tetrimino = 13;
			}
			
			tetrimino_tombe = 1;
			position_x = 5;
			position_y = 17;
			rotation_tetrimino = 0;
		}
		
		for(i=0;i<2;i++){
			
			////////////////////////////////////////////////////
			//////// Ajout des tetriminos dans le tableau //////
			
			if(i == 0){
				couleur_a_peindre = 0;
			}else{
				couleur_a_peindre = couleur_tetrimino;
			}
			
			cases[Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 1, "x")][Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 1, "y")] = couleur_a_peindre;
			cases[Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 2, "x")][Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 2, "y")] = couleur_a_peindre;
			cases[Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 3, "x")][Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 3, "y")] = couleur_a_peindre;
			cases[Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 4, "x")][Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 4, "y")] = couleur_a_peindre;
			
			// les contrôles ont lieu uniquement au premier passage
			if(i == 0){
				
				/////////////////////////////////////////////////////
				////////////// Contrôles claviers ///////////////////
				
				// on teste si la touche haut est enfoncée
				if(keypushed( VK_UP )){
					
					nouvelle_rotation = rotation_tetrimino + 90;
					while(nouvelle_rotation >=360){
						nouvelle_rotation -= 360;
					}
					if(EstValide(Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 1, "x")) and EstValide(Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 2, "x")) and EstValide(Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 3, "x")) and EstValide(Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 4, "x")) and Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 1, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 2, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 3, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 4, "y") >= 0){
						if(cases[Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 1, "x")][Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 1, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 2, "x")][Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 2, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 3, "x")][Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 3, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 4, "x")][Tetrimino(type_tetrimino, position_x, position_y, nouvelle_rotation, 4, "y")] == 0){
							rotation_tetrimino = nouvelle_rotation;
						}
					}
				}
				
				// on teste les touches gauche et droite
				if(keypushed( VK_LEFT )){
					if(EstValide(Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 1, "x")) and EstValide(Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 2, "x")) and EstValide(Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 3, "x")) and EstValide(Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 4, "x"))){
						
						if(cases[Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 1, "x")][Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 1, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 2, "x")][Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 2, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 3, "x")][Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 3, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 4, "x")][Tetrimino(type_tetrimino, position_x-1, position_y, rotation_tetrimino, 4, "y")] == 0){
							position_x -= 1;
						}
					}
				}
				if(keypushed( VK_RIGHT )){
					if(EstValide(Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 1, "x")) and EstValide(Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 2, "x")) and EstValide(Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 3, "x")) and EstValide(Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 4, "x"))){
						if(cases[Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 1, "x")][Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 1, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 2, "x")][Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 2, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 3, "x")][Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 3, "y")] == 0 and
						cases[Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 4, "x")][Tetrimino(type_tetrimino, position_x+1, position_y, rotation_tetrimino, 4, "y")] == 0){
							position_x += 1;
						}
					}
				}
				if(keypushed( VK_DOWN )){
					vitesse = 0.05;
				}else{
					vitesse = 0.2;
				}
				
				/////////////////////////////////////////////////////
				////////////// Gestion de la chute //////////////////
				
				// on regarde si on peut faire tomber le tetrimino
				peut_tomber = 0;
				
				if(Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 1, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 2, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 3, "y") >= 0 and Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 4, "y") >= 0){
					if(cases[Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 1, "x")][Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 1, "y")] == 0 and
					cases[Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 2, "x")][Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 2, "y")] == 0 and
					cases[Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 3, "x")][Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 3, "y")] == 0 and
					cases[Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 4, "x")][Tetrimino(type_tetrimino, position_x, position_y-1, rotation_tetrimino, 4, "y")] == 0){
						peut_tomber = 1;
					}
				}
				
				// si on peut baisser la pièce, on diminue sa position y
				if(peut_tomber == 1){
					position_y -= 1;
				}else{
					//sinon on arrête la chute et on demande un nouveau tetrimino
					tetrimino_tombe = 0;
					
					if(Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 1, "y") >= 17 and Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 2, "y") >= 17 and Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 3, "y") >= 17 and Tetrimino(type_tetrimino, position_x, position_y, rotation_tetrimino, 4, "y") >= 17){
						message("Fin de la partie !");
						message("Score: " + score + " - Lignes complétées: " + lignes_completees);
						message("Cliquez sur rafraîchir avant de commencer une nouvelle partie");
						partie_finie = 1;
					}
				}
			}
		}
		
		//////////////////////////////////////////////////////
		////////// Détection des lignes complètes ////////////
		
		combo = 0;
		
		if(tetrimino_tombe == 0){
			for(i=0;i<16;i++){
				
				ligne_incomplete = 0;
				for(j=0;j<10;j++){
					if(cases[j][i] == 0){
						ligne_incomplete = 1;
					}
				}
				
				// si la ligne est remplie complètement, on copie le contenu de chaque ligne dans la ligne du dessous à partir de la ligne complétée précédemment
				if(ligne_incomplete == 0){
					
					for(k=i;k<16;k++){
						for(j=0;j<10;j++){
							cases[j][k] = cases[j][k+1];
						}
					}
					
					lignes_completees++;
					combo++;
					i -= 1;
				}
			}
		}
		
		// on compte les combos
		if(combo == 1){
			score += 40;
		}
		if(combo == 2){
			score += 100;
		}
		if(combo == 3){
			score += 300;
		}
		if(combo == 4){
			score += 1200;
		}
		
		////////////////////////////////////////////////////
		//////////// Impression de la grille ///////////////
		
		// on met l'arrière-plan en blanc
		clear();
		white();
		fillall();
		penwidth(1);
		
		// remplir la zone selon le tableau - moteur graphique par défaut
		for(i=0;i<10;i++){
			goto(2.5+i,2);
			lookat(90);
			
			// on compte le nombre de cases à colorier. lorsqu'on en a colorié autant, on passe à la ligne suivant
			// ceci évite d'imprimer les cases blanches au-dessus du reste
			cases_a_colorier = 0;
			for(j=0;j<16;j++){
				if(cases[i][j] != 0){cases_a_colorier++;}
			}
			
			j = 0;
			
			while(cases_a_colorier > 0){
				if(cases[i][j] != 0){
					cases_a_colorier -= 1;
				}
				pencolor(cases[i][j]);
				pendown();
				move(1);
				penup();
				
				j++;
			}
		}
		
		// on dessine la zone de jeu
		black();
		penwidth(0.1);
		
		for(i=0;i<=10;i++){
			goto(2+i,2);
			lookat(90);
			pendown();
			move(16);
			penup();
		}
		
		for(i=0;i<=16;i++){
			goto(2,2+i);
			lookat(0);
			pendown();
			move(10);
			penup();
		}
		
		goto(16,16);
		lookat(0);
		wait(vitesse);
	}
}
//////////////////////////////////////////////////
/////////// Définition des tetriminos ////////////

int Tetrimino(string type, float position_x, float position_y, float rotation, float position_n, string x_ou_y){
	if(type == "t"){
		if(rotation == 0){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
		}
		if(rotation == 90){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
		}
		if(rotation == 180){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
		}
		if(rotation == 270){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
		}
		
	}
	if(type == "i"){
		if(rotation == 0 or rotation == 180){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+2;}
			}
		}
		if(rotation == 90 or rotation == 270){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x+2;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
		}
		
	}
	if(type == "o"){
		if(position_n == 1){
			if(x_ou_y == "x"){return position_x;}
			else{return position_y;}
		}
		if(position_n == 2){
			if(x_ou_y == "x"){return position_x+1;}
			else{return position_y;}
		}
		if(position_n == 3){
			if(x_ou_y == "x"){return position_x;}
			else{return position_y+1;}
		}
		if(position_n == 4){
			if(x_ou_y == "x"){return position_x+1;}
			else{return position_y+1;}
		}
		
	}
	if(type == "l"){
		if(rotation == 0){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y-1;}
			}
		}
		if(rotation == 90){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y+1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
		}
		if(rotation == 180){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y+1;}
			}
		}
		if(rotation == 270){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
		}
		
	}
	if(type == "j"){
		if(rotation == 0){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y-1;}
			}
		}
		if(rotation == 90){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
		}
		if(rotation == 180){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y+1;}
			}
		}
		if(rotation == 270){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y+1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
		}
		
	}
	if(type == "z"){
		if(rotation == 0){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y+1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
		}
		if(rotation == 90){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y-1;}
			}
		}
		
	}
	if(type == "s"){
		if(rotation == 0){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x-1;}
				else{return position_y-1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y-1;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
		}
		if(rotation == 90){
			if(position_n == 1){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y+1;}
			}
			if(position_n == 2){
				if(x_ou_y == "x"){return position_x;}
				else{return position_y;}
			}
			if(position_n == 3){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y;}
			}
			if(position_n == 4){
				if(x_ou_y == "x"){return position_x+1;}
				else{return position_y-1;}
			}
		}
	}
}

bool EstValide(float valeur){
	
	if(valeur >= 0 and valeur <= 9){
		return true;
	}else{
		return false;
	}
	
}
