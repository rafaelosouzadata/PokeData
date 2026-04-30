{{ config(materialized="table")}}

with "tipos_separados" as (
		select distinct 
			unnest(string_to_array(types, ',')) as "type"
			from {{ ref('pokemon_clean')}}
	)
select 
	row_number()over(order by type) as "id", "type" 
	from "tipos_separados"
where "type" is not Null