{{ config(materialized="table")}}

SELECT
	pc."id" AS "id_pokemon",
	pc."name",
	pc."weight",
	pc."height",
    dg.id_generation,
    sc."gender_rate",
    sc."capture_rate",
    sc."is_baby",
    sc."is_legendary",
    sc."is_mythical"
FROM {{  ref("pokemon_clean")}} pc
JOIN {{  ref("species_clean")}} sc ON pc.id = sc.id
JOIN {{  ref("dim_generations")}} dg ON sc.generation = dg.generation