{{ config(materialized="table")}}

with "tipos_explodidos" as (
	select
		"id",
		unnest(string_to_array(types, ',')) as "type"
	from {{ ref('stg_pokemon')}}
	)
select 
	te.id as "id_pokemon", 
	t.id_type
from "tipos_explodidos" te
	join {{ref("dim_types")}} t on t."type" = te.type
order by 1
