{{ config(materialized='table')}}

WITH types_counted AS (
	SELECT
		pt.type_id,
		count(pt.type_id) AS total_sum
	FROM
		{{  ref('pokemon_types')  }} pt
	GROUP BY pt.type_id
	)
SELECT
	t.type,
	tc.total_sum
FROM
	types_counted tc
JOIN {{  ref('types')  }} t ON tc.type_id = t.id
ORDER BY tc.total_sum DESC