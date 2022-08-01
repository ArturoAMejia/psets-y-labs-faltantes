SELECT title FROM movies
JOIN stars ON stars.movie_id=movies.id JOIN people ON stars.person_id=people.id
where people.name="Johnny Depp" and title IN (
SELECT title FROM movies
JOIN stars ON stars.movie_id=movies.id JOIN people ON stars.person_id=people.id
where people.name="Helena Bonham Carter"
)
