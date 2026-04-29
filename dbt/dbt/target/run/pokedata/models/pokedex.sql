
  
    

  create  table "Poke_Banco"."public"."pokedex__dbt_tmp"
  
  
    as
  
  (
    

select
	"id",
	"name",
	"weight",
	"hight"
from "Poke_Banco"."public"."Pokemons"
  );
  