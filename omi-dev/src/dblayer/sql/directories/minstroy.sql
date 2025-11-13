--name: get_minstroy_by_params^
select *
from dir.minstroy
where region = :region and period = :period;
