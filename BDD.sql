create table eleves(
	id INTEGER primary key autoincrement ,
	nom CHAR(30) NOT NULL,
	prenom CHAR(30) NOT NULL,
	date_naissance DATE,
	telephone INTEGER,
	option CHAR(30),
	ecole_origine CHAR(30),
	mathematiques int,
	informatique int
);


-- INSERT into eleves (nom,prenom,date_naissance,telephone,option,ecole_origine) values ('TESTA','Enzo','28-01-1995',0123456789,'GSI','Mines Nantes');