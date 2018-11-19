USE sakila;

-- 1a. Display the first and last names of all actors from the table `actor`.
SELECT first_name, last_name 
FROM actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. 
-- Name the column `Actor Name`. 
SELECT UPPER(CONCAT(first_name, ' ', last_name)) as 'Actor Name'
FROM actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
-- What is one query would you use to obtain this information?
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name='Joe';

-- 2b. Find all actors whose last name contain the letters `GEN`
SELECT * FROM actor
WHERE last_name LIKE '%gen%';

-- 2c. Find all actors whose last names contain the letters `LI`. 
-- This time, order the rows by last name and first name, in that order.
SELECT last_name, first_name FROM actor
WHERE last_name LIKE '%li%'
ORDER BY last_name, first_name;

-- 2d. Using `IN`, display the `country_id` and `country` columns of the following countries: 
-- Afghanistan, Bangladesh, and China.
SELECT country_id, country
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, 
-- so create a column in the table `actor` named `description` 
-- and use the data type `BLOB` (Make sure to research the type `BLOB`, as the difference between it and `VARCHAR` are significant).
ALTER TABLE actor
ADD description BLOB;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the `description` column.
ALTER TABLE actor
DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name, count(*) as 'Last Name Count'
FROM actor
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, 
-- but only for names that are shared by at least two actors.
SELECT last_name, COUNT(*) as 'Last Name Count'
FROM actor
GROUP BY last_name
HAVING COUNT(*) > 1;

-- 4c. The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`. 
-- Write a query to fix the record.
SELECT * FROM actor
WHERE first_name='Groucho' AND last_name='Williams';

UPDATE actor
SET first_name = 'HARPO'
WHERE actor_id = 172;

-- 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! 
-- In a single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`.
UPDATE actor
SET first_name = 'GROUCHO'
WHERE actor_id = 172;

-- 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

-- 6a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. 
-- Use the tables `staff` and `address`.
SELECT first_name, last_name, address
FROM staff
INNER JOIN address ON
staff.address_id=address.address_id;

-- 6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment`.
SELECT first_name, last_name, sum(amount) as 'Total Rung Up (Aug 2005)'
FROM staff
INNER JOIN payment 
USING (staff_id)
WHERE payment_date LIKE '2005-08%'
GROUP BY staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join.
SELECT title, COUNT(*) as 'Number of Actors'
FROM film
INNER JOIN film_actor
USING (film_id)
GROUP BY film.title;

-- 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system?
SELECT title, COUNT(*) as 'Copies in Inventory'
FROM film
INNER JOIN inventory
USING (film_id)
WHERE title ='Hunchback Impossible';

-- 6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer. 
-- List the customers alphabetically by last name.
SELECT first_name, last_name, SUM(amount) as 'Total Amount Paid'
from customer
INNER JOIN payment
USING (customer_id)
GROUP BY last_name
ORDER BY last_name;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
-- As an unintended consequence, films starting with the letters `K` and `Q` have also soared in popularity. 
-- Use subqueries to display the titles of movies starting with the letters `K` and `Q` 
-- whose language is English.
SELECT title 
FROM film
WHERE (title LIKE 'K%') or (title like'Q%') IN(
SELECT language_id
FROM language
WHERE language_id = 1
);

-- 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.
SELECT first_name, last_name
FROM actor
WHERE actor_id IN 
(
SELECT actor_id
FROM film_actor
WHERE film_id IN 
(
SELECT film_id
FROM film
WHERE title='Alone Trip'
)
);

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email 
-- addresses of all Canadian customers. Use joins to retrieve this information.
SELECT * from country
WHERE country = 'Canada'; -- 20 is Canada

SELECT first_name, last_name, email
FROM customer 
INNER JOIN address
USING (address_id) 
WHERE city_id IN 
(
SELECT city_id
FROM city
WHERE country_id = 20
);

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
-- Identify all movies categorized as _family_ films.
SELECT * from category; -- 8 is Family

SELECT title as 'Family Films'
FROM film
INNER JOIN film_category
USING (film_id)
WHERE category_id IN 
(
SELECT category_id
FROM category
WHERE category_id = 8
);

-- 7e. Display the most frequently rented movies in descending order.
SELECT title, COUNT(*) as 'Number of Times Rented'
FROM film, rental, inventory
WHERE film.film_id=inventory.film_id AND rental.inventory_id=inventory.inventory_id
GROUP BY title
ORDER BY COUNT(*) desc;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT s.store_id, SUM(amount) as 'Revenue'
FROM payment p
JOIN rental r
ON (p.rental_id=r.rental_id)
JOIN inventory i
ON (i.inventory_id=r.inventory_id)
JOIN store s
ON (s.store_id=i.store_id)
GROUP BY s.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT s.store_id, city.city, c.country
FROM store s 
JOIN address a
ON (s.address_id=a.address_id)
JOIN city
ON (a.city_id=city.city_id)
JOIN country c
ON (city.country_id=c.country_id);

-- 7h. List the top five genres in gross revenue in descending order. 
-- (**Hint**: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT c.name, SUM(p.amount) AS 'Gross_revenue'
FROM category c 
JOIN film_category fc
ON (c.category_id=fc.category_id)
JOIN inventory i
ON (fc.film_id=i.film_id)
JOIN rental r
ON (i.inventory_id=r.inventory_id)
JOIN payment p
ON (r.rental_id=p.rental_id)
GROUP BY c.name
ORDER BY Gross_revenue DESC LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres 
-- by gross revenue. Use the solution from the problem above to create a view. 
-- If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW top_5_genre AS 
SELECT c.name, SUM(p.amount) AS 'Gross_revenue'
FROM category c 
JOIN film_category fc
ON (c.category_id=fc.category_id)
JOIN inventory i
ON (fc.film_id=i.film_id)
JOIN rental r
ON (i.inventory_id=r.inventory_id)
JOIN payment p
ON (r.rental_id=p.rental_id)
GROUP BY c.name
ORDER BY Gross_revenue DESC LIMIT 5;

-- 8b. How would you display the view that you created in 8a?
SELECT * from top_5_genre;

-- 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.
DROP VIEW top_5_genre;

