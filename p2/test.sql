
drop table if exists song_data;
create table song_data as
select *, 1 as flag from mars_tianchi_songs;


drop table if exists rolling_sum7;
create table rolling_sum7 as
select artist_id, sum(plays) over (partition by artist_id, plays, ds order by artist_id, ds ROWS 10 FOLLOWING) as plays, ds
from liuhe_arts_data 
order by artist_id, ds limit 100000000;
