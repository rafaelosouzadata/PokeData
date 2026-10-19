SELECT
    p.id_generation,
    pt.id_type,
    COUNT(p.id_pokemon) AS qty_type
FROM {{  ref('dim_pokemons')}} p
JOIN {{  ref('int_pokemon_types')}} pt ON p.id_pokemon = pt.id_pokemon
GROUP BY 1, 2
