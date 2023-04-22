{{config(materialized='table')}}

select 	int64_field_0 as Id,
        case when operator = 'Privatperson' then 'Private_person' 
        else operator end as operator,
        Street,	
        House_number,
        cast(Postal_code as string) as Postal_code,

        --Berlin
        case when ort = 'Überlingen' then 'Überlingen' 
        when CONTAINS_SUBSTR(ort, 'berlin') then 'Berlin'
        -- Hamburg
        when CONTAINS_SUBSTR(ort, 'hamburg') then 'Hamburg'
        -- Munchen
        when ort = 'Schwabmünchen' then 'Schwabmünchen'
        when ort = 'Waldmünchen' then 'Waldmünchen'
        when CONTAINS_SUBSTR(ort, 'münchen') then 'München'
        -- Köln
        when CONTAINS_SUBSTR(ort, 'köln') then 'Köln' 
        -- Frankfurt
        when ort = 'Frankfurt (Oder)' then 'Frankfurt (Oder)'
        when ort = 'Frankfurt/Oder)' then 'Frankfurt/Oder)'
        when CONTAINS_SUBSTR(ort, 'frankfurt') then 'Frankfurt'
        -- Essen
        when ort = 'Essen-Kettwig' or ort = 'Essen-Altenessen' or ort = 'Essen' then 'Essen'
        -- Dortmund
        when CONTAINS_SUBSTR(ort, 'dortmund') then 'Dortmund'
        -- Stuttgart
        when CONTAINS_SUBSTR(ort, 'stuttgart') then 'Stuttgart'
        -- Düsseldorf
        when CONTAINS_SUBSTR(ort, 'düsseldorf') then 'Düsseldorf'
        -- Bremen
        when CONTAINS_SUBSTR(ort, 'bremen') then 'Bremen'
        else ort end as City_Town,

        case when Federal_State is null then 'Mecklenburg-Vorpommern' else Federal_State 
        end as Federal_State,
        District_district_free_city,
        latitude,
        longitude,
        commissioning_date,
        connected_load,

        case when Type_of_charging_device = 'Normalladeeinrichtung' then 'Normal' 
                when Type_of_charging_device ='Schnellladeeinrichtung' then 'Fast'
                else 'Fast' end as Type_of_charging_device,
        number_of_charging_points,
        Connector_Types1,
        Power_point_1_KW,
        Connector_Types2,
        Power_point_2_KW,
        Connector_Types3,
        Power_point_3_KW,
        Connector_Types4,
        
        cast(Power_point_4_KW as float64) as Power_point_4_KW

from {{ source('raw_to_stg','raw') }}