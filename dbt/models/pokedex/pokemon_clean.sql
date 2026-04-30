{{ config(materialized="view") }}

SELECT * FROM {{  source('pokedex_data', 'Raw_Pokemons')  }}
