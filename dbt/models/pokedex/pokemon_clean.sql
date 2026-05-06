{{ config(materialized="table") }}

SELECT * FROM {{  source('pokedex_data', 'Raw_Pokemons')  }}
