{{config(materialized='table')}}

select cast(City_rank as int) as City_rank, 
               city,
               Federal_state,
        cast(Population as numeric) as Population

        
from {{ source('raw_to_stg','cities') }}
order by City_rank
limit 10