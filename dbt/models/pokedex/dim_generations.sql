{{ config(materialized="table")}}

WITH sorting_generation AS (
    SELECT
        id,
        generation,
        ROW_NUMBER()OVER(PARTITION BY generation ORDER BY id) AS index
    FROM {{  ref('species_clean')}}
)
SELECT 
    ROW_NUMBER()OVER(ORDER BY id) AS id_generation,
    generation
FROM sorting_generation
WHERE index = 1
ORDER BY 1