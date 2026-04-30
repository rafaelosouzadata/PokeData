{{ config(materialized="table")}}

select
	"id",
	"name",
	"weight",
	"hight"
from {{ ref('pokemon_clean')}}