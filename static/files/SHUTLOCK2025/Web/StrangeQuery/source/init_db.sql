-- init_db.sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    pronouns VARCHAR(500),
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT false,
    is_admin BOOLEAN NOT NULL DEFAULT false
);

-- Create the 'movies' table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    image_link VARCHAR(200),
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the 'comments' table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some users
INSERT INTO users ( username, pronouns, email, password, verified, is_admin) VALUES
( 'Administrateur', 'them', 'admin@netflute.fr', '', true, true),
( 'Timmy', 'him', 'timmy@netflute.fr', '', true, false),
( 'Bob', 'Him/his', 'bob@netflute.fr', '', true, false),
( 'Alice', 'She/her', 'alice@netflute.fr', '', true, false),
('Charlie', 'they/them', 'charlie@netflute.fr', '', true, false),
('Diana', 'she/her', 'diana@netflute.fr', '', true, false),
('Élodie', 'she/her', 'elodie@netflute.fr', '', true, false),
('Maxime', 'he/him', 'maxime@netflute.fr', '', true, false),
('Léa', 'she/they', 'lea@netflute.fr', '', true, false),
('Yassine', 'he/they', 'yassine@netflute.fr', '', true, false);

-- Insert some Movies
INSERT INTO movies ( title, content, image_link, user_id, created_at) VALUES
('Spider-Man: Sans retour', 'L''identité de Spider-Man étant désormais révélée, Peter demande de l''aide au docteur Strange. Lorsqu''un sort tourne mal, des ennemis commencent à apparaître, forçant Peter à découvrir ce que signifie vraiment être Spider-Man.', 'https://m.media-amazon.com/images/M/MV5BMmFiZGZjMmEtMTA0Ni00MzA2LTljMTYtZGI2MGJmZWYzZTQ2XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', 1, '2021-12-15'),
('Pirates des Caraïbes : La malédiction de la Perle Noire', 'Le forgeron Will Turner fait équipe avec le pirate excentrique Capitaine Jack Sparrow pour sauver la fille du gouverneu, dont il tombe en amour, des anciens alliés pirates de Jack, à présent devenus morts-vivants.', 'https://fr.web.img4.acsta.net/medias/nmedia/18/35/07/46/affiche2.jpg', 2, '2003-08-13'),
('No Country for Old Men', 'Violence and mayhem ensue after a hunter stumbles upon the aftermath of a drug deal gone wrong and over two million dollars in cash near the Rio Grande.', 'https://m.media-amazon.com/images/M/MV5BMjA5Njk3MjM4OV5BMl5BanBnXkFtZTcwMTc5MTE1MQ@@._V1_FMjpg_UX1000_.jpg', 1, '2018-01-23'),
('Toy Story', 'A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy''s bedroom.', 'https://i.servimg.com/u/f20/11/38/13/05/tm/1995-t10.jpg', 3, '1996-03-27'),
('Fast & Furious: Tokyo Drift', 'Un adolescent devient un concurrent niveau mondiale dans la course à la dérive, après avoir emménagé avec son père à Tokyo afin déviter la prison aux États-Unis.', 'https://m.media-amazon.com/images/M/MV5BMTQ2NTMxODEyNV5BMl5BanBnXkFtZTcwMDgxMjA0MQ@@._V1_FMjpg_UX1000_.jpg', 2, '2006-07-19');

-- Insert some Comments
INSERT INTO comments (content, movie_id, user_id, created_at) VALUES
-- Spider-Man
('J’ai adoré l’action et les effets spéciaux !', 1, 3, '2022-01-10 14:25:00'),
('La fin m’a fait pleurer. Un chef-d’œuvre.', 1, 4, '2022-01-12 09:03:00'),
('Trop de fan service, j’ai été un peu déçu.', 1, 5, '2022-01-15 17:45:00'),
('Le multivers est une idée brillante, j’ai adoré !', 1, 7, '2022-01-18 19:22:00'),
('Mon Spider-Man préféré reste celui de Tobey.', 1, 8, '2022-01-20 13:47:00'),
('Ils auraient pu mieux développer certains méchants.', 1, 9, '2022-01-22 10:18:00'),
('Ce film est trop cool, merci @tag(Timmy,him,2) pour le partage <3', 1, 9, '2025-02-13 10:18:00'),


-- Pirates des Caraïbes
('Jack Sparrow est iconique, quel personnage !', 2, 2, '2004-01-05 11:00:00'),
('La bande-son est incroyable, je l’écoute encore.', 2, 6, '2004-01-06 16:30:00'),
('Un classique que je ne me lasse jamais de revoir.', 2, 3, '2005-06-21 20:15:00'),
('Ce film est une aventure de bout en bout !', 2, 10, '2004-02-10 09:40:00'),
('J’ai toujours rêvé d’être un pirate en le regardant.', 2, 7, '2004-03-15 18:25:00'),
('Johnny Depp est né pour ce rôle !', 2, 8, '2004-04-01 15:50:00'),

-- No Country for Old Men
('Très intense, l’ambiance est pesante du début à la fin.', 3, 4, '2018-02-10 22:00:00'),
('J’ai rien compris à la fin, mais j’ai quand même aimé.', 3, 5, '2018-03-01 13:45:00'),
('Un film qui te reste en tête plusieurs jours après.', 3, 6, '2018-03-12 18:05:00'),
('Le suspense est insoutenable tout du long.', 3, 9, '2018-04-01 20:35:00'),
('Le silence dans certaines scènes est plus fort que la musique.', 3, 10, '2018-04-07 21:50:00'),
('Anton Chigurh est l’un des meilleurs méchants du cinéma.', 3, 7, '2018-04-15 10:00:00'),
('Salut @tag(Alice,She/her,4), comment ça va ?? <3', 3, 3, '2025-02-12 11:45:00'),
('Oh, salut @tag(Bob,Him/his,3), on peut tagger des gens maintenant ?', 3, 3, '2025-02-12 11:45:00'),

-- Toy Story
('Les jouets ont une âme… j’ai pleuré.', 4, 2, '1996-04-02 08:00:00'),
('Le début d’une grande saga !', 4, 3, '1996-04-10 14:30:00'),
('Mon enfance résumée en un film.', 4, 5, '1996-05-01 10:10:00'),
('Buzz et Woody, duo légendaire !', 4, 8, '1996-05-15 12:45:00'),
('C’était magique à regarder en tant qu’enfant.', 4, 9, '1996-06-02 09:30:00'),
('Ça me rappelle mes vieux jouets.', 4, 10, '1996-06-20 14:05:00'),

-- Fast & Furious: Tokyo Drift
('Le drift à Tokyo, c’est du pur style !', 5, 7, '2006-08-10 21:00:00'),
('J’ai appris ce qu’était le drift grâce à ce film.', 5, 8, '2006-09-01 10:10:00'),
('L’histoire est pas ouf mais les voitures sont folles !', 5, 9, '2006-09-15 19:30:00'),
('Han est vraiment trop classe. RIP !', 5, 10, '2006-10-01 22:15:00');


-- Flag section

-- Create the 'secrets' table
CREATE TABLE IF NOT EXISTS secrets (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    classification TEXT NOT NULL
);

-- Insert some secret and flag

INSERT INTO secrets ( content, classification) VALUES
( 'this_is_the_flag', 'SHLK{S3CoNd_0RDeR_4rEN7_AwE50me_?}'),
( 'Ce challenge est fait par un étudiant épitéen.', 'Secret'),
( 'La solution du challenge se trouve dans cette table.', 'Très secret');
