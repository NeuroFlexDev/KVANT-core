--name: get_section_cost_ratio_by_id^
select s.*,
    coalesce((select mi.section
        from omi_model.model_info mi
        where mi.name = s.section_code
        order by date_from desc
        limit 1), s.caption, s.section_code
    ) as section_name
from dir.sectioncostratio s
where s.id = :id;

--name: get_section_cost_ratio
select s.*,
    coalesce((select mi.section
        from omi_model.model_info mi
        where mi.name = s.section_code
        order by date_from desc
        limit 1), s.caption, s.section_code
    ) as section_name
from dir.sectioncostratio s
where s.state_id > -1
order by s.id;

--name: get_sections
select s.section_code, s.value, s.k1, s.k2, s.k3, s.k4, s.k5,
    coalesce((select mi.section
        from omi_model.model_info mi
        where mi.name = s.section_code
        order by date_from desc
        limit 1), s.caption, s.section_code
    ) as section_name
from dir.sectioncostratio s
where s.id > 0 and s.state_id > -1
order by s.id;

--name: get_section_cost_ratio_sum^
select sum(value) as count
from dir.sectioncostratio
where id > 0;

--name: update_section_cost_ratio<!
update dir.sectioncostratio
set state_id = 1,
    modifier_id = :user_id,
    modifydate = now(),
    value = :value
where id = :id
returning *;

--name: section_cost_ratio_sync^
with a as (
    select s.id, s.state_id, s.section_code, mi.name, :user_id as user_id
    from dir.sectioncostratio s
    full join (
        select name
        from omi_model.model_info mi
        where mi.date_to is null and (mi.model_type is null or mi.model_type = 'temp')
    ) mi on mi.name = s.section_code
    where s.id > 0 or s.id is null
),
b as (
    insert into dir.sectioncostratio
    (section_code, creator_id, value)
    select name, user_id, 0
    from a
    where a.section_code is null
),
c as (
    update dir.sectioncostratio s
    set state_id = 1,
    	modifier_id = user_id,
    	modifydate = now()
    from (select * from a where a.name is not null and a.state_id = -1) pr
    where s.id = pr.id
),
d as (
    update dir.sectioncostratio s
    set state_id = -1,
    	modifier_id = user_id,
    	modifydate = now()
    from (select * from a where name is null) pr
    where s.id = pr.id
)
select 1;