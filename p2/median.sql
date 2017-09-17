-- median
drop table if exists temp1;
create table temp1 as
select artist_id, median(Plays) as Plays
from liuhe_arts_data
where ds >= 20150801
group by artist_id;

-- merge
drop table if exists temp2;
create table temp2 as
select A.artist_id, B.Plays, dateadd(A.Ds, 61, 'dd') as Ds from
(
select artist_id, to_date(Ds, 'yyyymmdd') as Ds
from liuhe_arts_data
where Ds >= 20150702 and Ds <= 20150830
)A
left outer join temp1 B
on B.artist_id = A.artist_id;

-- output
drop table if exists lh_median30;
create table lh_median30 as
select artist_id, to_char(floor(Plays)) as Plays, to_char(Ds, 'yyyymmdd') as Ds
from temp2
order by ds, artist_id limit 10000;
