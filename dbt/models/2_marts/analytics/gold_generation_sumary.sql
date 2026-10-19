{{ config(materialized='table')}}

{% set pokemon_types = dbt_utils.get_column_values(table=ref('dim_types'), column='type') %}

WITH prepare_pivot AS (
    SELECT
        tpg.id_generation,
        dt.type,
        tpg.qty_type
    FROM {{ ref('fct_type_by_generation')}} tpg
    JOIN {{ ref('dim_types')}} dt ON dt.id_type = tpg.id_type
), 

pivoted_types AS (
    SELECT 
        id_generation,
        {{ dbt_utils.pivot(
            column='type',
            values=pokemon_types,
            agg='sum',
            then_value='qty_type',
            else_value=0
        ) }}
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
    FROM {{ ref('dim_pokemons')}}
    GROUP BY 1
)

SELECT 
    ps.id_generation,
    ps.qty_pokemon,
    ps.qty_legendary,
    ps.qty_mythical,
    ps.qty_baby,
    {% for type in pokemon_types %}
    pt.{{ type }}{% if not loop.last %},{% endif %}
    {% endfor %}
FROM prepare_specials ps
LEFT JOIN pivoted_types pt ON pt.id_generation = ps.id_generation
ORDER BY 1
