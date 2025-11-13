--name: get_prices
with price_base as (
	select *
	from dir.price p
	where p.period = :period and p.creator_id is null
),
price_user as (
	select p.*
	from dir.price p
	join (
		select element_name, max(id) as max_id
		from dir.price
		where creator_id = :user_id and createdate > concat_ws('-', left(:period, 4), (right(:period, 1)::int * 3 - 2)::text, '01')::date
		group by element_name) pr on pr.max_id = p.id
),
price_common as (
	select coalesce(pu.id, pb.id) as id,
		coalesce(pu.state_id, pb.state_id) as state_id,
		coalesce(pu.creator_id, pb.creator_id) as creator_id,
		coalesce(pu.createdate, pb.createdate) as createdate,
		coalesce(pu.modifier_id, pb.modifier_id) as modifier_id,
		coalesce(pu.modifydate, pb.modifydate) as modifydate,
		coalesce(pu.guid, pb.guid) as guid,
		coalesce(pu.elementtype_name, pb.elementtype_name) as elementtype_name,
		coalesce(pu.element_name, pb.element_name) as element_name,
		coalesce(pu.unit, pb.unit) as unit,
		coalesce(pu.value_ws, pb.value_ws) as value_ws,
		coalesce(pu.quantity_ws, pb.quantity_ws) as quantity_ws,
		coalesce(pu.ratio, pb.ratio) as ratio,
		coalesce(pu.url, pb.url) as url,
		coalesce(pu.period, pb.period) as period,
		pb.value_ws / pb.quantity_ws as base_value
	from price_base pb
	full join price_user pu on pu.element_name = pb.element_name
)
select id, state_id, creator_id, createdate, modifier_id, modifydate, guid,
	elementtype_name, element_name, unit,
	 value_ws, quantity_ws, value_ws / quantity_ws as value, ratio, url, "period", base_value
from price_common
where case when :full then 1=1
           else id is null
      end
UNION
select NULL, NULL, NULL, NULL, NULL, NULL, NULL,
    elementtype_name, NULL, unit,
     NULL, NULL, sum(round(value_ws / quantity_ws * ratio * 100) / 100), sum(ratio), NULL, NULL, NULL
from price_common
group by elementtype_name, unit
order by elementtype_name, element_name desc, unit;
