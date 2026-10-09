{{ config(materialized="table") }}

SELECT * FROM {{  source('pokedex_data', 'raw_species')  }}
