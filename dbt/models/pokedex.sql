{{ config(materialized="table")}}

select
	"id",
	"name",
	"weight",
	"hight"
from {{ source('pokedex_data','Pokemons') }}