WITH prepare_pivot AS (
    SELECT
        tpg.id_generation,
        dt.type,
        tpg.qty_type
    FROM {{ ref('type_per_generation')}} tpg
    JOIN {{ ref('dim_types')}} dt ON dt.id = tpg.type_id
), 
pivoted_types AS (
    SELECT 
        id_generation,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'normal'), 0) AS normal,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'fire'), 0) AS fire,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'water'), 0) AS water,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'grass'), 0) AS grass,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'electric'), 0) AS electric,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'ice'), 0) AS ice,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'fighting'), 0) AS fighting,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'poison'), 0) AS poison,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'ground'), 0) AS ground,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'flying'), 0) AS flying,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'psychic'), 0) AS psychic,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'bug'), 0) AS bug,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'rock'), 0) AS rock,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'ghost'), 0) AS ghost,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'dragon'), 0) AS dragon,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'dark'), 0) AS dark,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'steel'), 0) AS steel,
        COALESCE(SUM(qty_type) FILTER (WHERE type = 'fairy'), 0) AS fairy
    FROM prepare_pivot
    GROUP BY 1
), 
prepare_specials AS (
    SELECT
        id_generation,
        COUNT(id_pokemon) AS qty_pokemon,
        COUNT(id_pokemon) FILTER (WHERE is_legendary = True) AS qty_legendary,
        COUNT(id_pokemon) FILTER (WHERE is_mythical = True) AS qty_mythical,
        COUNT(id_pokemon) FILTER (WHERE is_baby = True) AS qty_baby
    FROM {{ ref('pokedex')}}
    GROUP BY 1
)
SELECT 
    ps.id_generation,
    ps.qty_pokemon,
    ps.qty_legendary,
    ps.qty_mythical,
    ps.qty_baby,
    pt.normal,
    pt.fire,
    pt.water,
    pt.grass,
    pt.electric,
    pt.ice,
    pt.fighting,
    pt.poison,
    pt.ground,
    pt.flying,
    pt.psychic,
    pt.bug,
    pt.rock,
    pt.ghost,
    pt.dragon,
    pt.dark,
    pt.steel,
    pt.fairy
FROM prepare_specials ps
LEFT JOIN pivoted_types pt ON pt.id_generation = ps.id_generation
ORDER BY 1
