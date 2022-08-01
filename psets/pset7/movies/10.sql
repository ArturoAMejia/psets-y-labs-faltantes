SELECT name FROM people
JOIN directors
ON people.id = directors.person_id
WHERE movie_id IN
(SELECT id FROM movies JOIN ratings
ON movies.id = ratings.movie_id
WHERE rating >= 9);