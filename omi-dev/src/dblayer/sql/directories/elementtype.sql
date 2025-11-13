--name: get_elementtypes
select *
from dir.elementtype
where state_id > -1
order by name;

--name: get_elementtype_by_id^
select * from dir.elementtype
where id = :id;

--name: refresh_elementtypes
with sel as (
	select element_name as name, unit
	from omi_model.d_omi_classifier
	group by element_name, unit
	order by element_name
),
del as (
	update dir.elementtype
	set state_id = -1,
		modifydate = now()
	where elementtype.id not in (select id from dir.elementtype et join sel on (sel.name, sel.unit) = (et.name, et.unit)) and elementtype.state_id > -1
	returning 'delete', id, name, unit
),
/*upd as (
	update dir.elementtype
	set state_id = 0,
		modifydate = now()
	where elementtype.id in (select id from dir.elementtype et join sel on (sel.name, sel.unit) = (et.name, et.unit)) and elementtype.state_id = -1
	returning 'update', id, name, unit
),*/
ins as (
	insert into dir.elementtype
	(name, unit)
	select *
	from (select sel.* from sel left join dir.elementtype et on (et.name, et.unit) = (sel.name, sel.unit) where et.id is null) pp
	returning 'insert', id, name, unit
)
select * from del
union
--select * from upd
--union
select * from ins;
