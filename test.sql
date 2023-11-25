-- Création d'une table "utilisateurs"
CREATE TABLE utilisateurs (
	    id INT PRIMARY KEY,
	    nom VARCHAR(50),
	    age INT
);

-- Insertion de quelques données
INSERT INTO utilisateurs (id, nom, age) VALUES
(1, 'Alice', 25),
(2, 'Bob', 30),
(3, 'Charlie', 22);

