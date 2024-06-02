WITH tmptb AS(
SELECT book_id, AVG(rating) avg_rating
FROM reviews
GROUP BY book_id
)
SELECT b.book_id, author, pyear, avg_rating
FROM books b
INNER JOIN tmptb USING book_id
WHERE b.book_id NOT IN ( SELECT book_id FROM borrowings);