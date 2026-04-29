

with "tipos_explodidos" as (
		select
			"id",
			unnest(string_to_array(types, ',')) as "type"
			from "Poke_Banco"."public"."Pokemons"
	)
select 
	te.id as "pokemon_id", 
	t.id as "type_id"
from "tipos_explodidos" te
	join "Poke_Banco"."public"."types" t on t."type" = te.type
order by te.id