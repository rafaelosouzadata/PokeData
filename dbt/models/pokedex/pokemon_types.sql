{{ config(materialized="table")}}

with "tipos_explodidos" as (
		select
			"id",
			unnest(string_to_array(types, ',')) as "type"
			from {{ ref('pokemon_clean')}}
	)
select 
	te.id as "pokemon_id", 
	t.id as "type_id"
from "tipos_explodidos" te
	join {{ref("types")}} t on t."type" = te.type
order by te.id
