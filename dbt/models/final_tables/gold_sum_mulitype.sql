{{ config(materialized='table')  }}

WITH pokemon_rowed AS (
	SELECT
		pt.pokemon_id,
		count(pt.type_id) AS total
	FROM {{  ref('pokemon_types')  }} pt
	GROUP BY pt.pokemon_id
	)
SELECT
	CASE
		WHEN pr.total = 1 THEN 'single_type'
		WHEN pr.total = 2 THEN 'double_type'
	END AS categoria,
	count(*) AS total_pokemons
FROM pokemon_rowed pr
GROUP BY categoria
ORDER BY total_pokemons
