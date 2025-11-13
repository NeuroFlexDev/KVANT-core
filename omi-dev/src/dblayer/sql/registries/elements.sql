--name: get_elements
select uid, element_name, element_type, unit, price
from omi_model.d_omi_classifier
where state_id > -1
group by uid, element_name, element_type, unit, price
order by element_name, element_type;

--name: get_element_by_id
select * from omi_model.d_omi_classifier
where id = :id;

-- name: create_element<!
insert into omi_model.d_omi_classifier (state_id, creator_id, createdate, guid, class_type, element_name, element_type, unit, price)
values(0, :user_id, now(), upper(uuid_generate_v4()::text), :class_type, :element_name, :element_type, :unit, :price)
returning *;

--name: update_element
update omi_model.d_omi_classifier
set modifier_id = :user_id,
    modifydate = now(),
--    class_type = coalesce(:class_type, class_type),
--    element_name = coalesce(:element_name, element_name),
--    element_type = coalesce(:element_type, element_type),
--    unit = coalesce(:unit, unit),
    price = coalesce(:price, price)
where uid = CAST(:uid AS UUID)
returning *;

-- name: delete_element<!
update omi_model.d_omi_classifier
set state_id = -1
where id = :id
returning *;
