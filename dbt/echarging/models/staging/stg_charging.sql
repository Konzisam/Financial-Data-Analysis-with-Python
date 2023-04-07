{{config(materialized='view')}}

select * from {{ source('staging','raw') }}