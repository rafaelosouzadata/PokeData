{{ config(materialized="table")}}

select
	"id",
	"name",
	"weight",
	"height"
from {{ ref('pokemon_clean')}}