
  
    

  create  table "Poke_Banco"."public"."types__dbt_tmp"
  
  
    as
  
  (
    

with "tipos_separados" as (
		select distinct 
			unnest(string_to_array(types, ',')) as "type"
			from "Poke_Banco"."public"."Pokemons"
	)
select 
	row_number()over(order by type) as "id", "type" 
	from "tipos_separados"
where "type" is not Null
  );
  