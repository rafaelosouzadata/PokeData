{{ config(materialized='table')}}

WITH types_counted AS (
	SELECT
		pt.id_type,
		count(pt.id_type) AS total_sum
	FROM
		{{  ref('int_pokemon_types')  }} pt
	GROUP BY pt.id_type
	)
SELECT
	t.type,
	tc.total_sum
FROM
	types_counted tc
JOIN {{  ref('dim_types')  }} t ON tc.id_type = t.id_type
ORDER BY tc.total_sum DESC