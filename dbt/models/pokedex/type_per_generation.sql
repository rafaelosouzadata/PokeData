SELECT
    p.id_generation,
    pt.type_id,
    COUNT(p.id_pokemon) AS qty_type
FROM {{  ref('pokedex')}} p
JOIN {{  ref('pokemon_types')}} pt ON p.id_pokemon = pt.pokemon_id
GROUP BY 1, 2
