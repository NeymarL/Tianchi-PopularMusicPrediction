-- group by
drop table if exists favor_data;
create table favor_data as
select A.artist_id, count(A.action_type) as favors, A.Ds
from big_data A
where A.action_type = 2 and A.artist_id is not null 
group by A.artist_id, A.Ds;

drop table if exists liuhe_arts_data;
create table if not exists liuhe_arts_data as
select artist_id, count(action_type) as Plays, Ds
from big_data
where action_type = 1 and artist_id is not null 
group by artist_id, Ds
order by artist_id, Ds limit 1000000000;
