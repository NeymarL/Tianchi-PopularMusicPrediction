-- mean
drop table if exists liuhe_midmean1;
create table liuhe_midmean1 as
select artist_id, avg(ln(favors)) as Plays
from favor_data
where Ds >= 20150611 and ds <= 20150701
group by artist_id;

-- merge
drop table if exists liuhe_midmean2;
create table liuhe_midmean2 as
select A.artist_id, B.Plays, A.ds from
(
select artist_id, to_date(Ds, 'yyyymmdd') as Ds
from liuhe_arts_data
where Ds >= 20150702 and Ds <= 20150830
)A
left outer join liuhe_midmean1 B
on B.artist_id = A.artist_id;

-- output
drop table if exists p2_fmean20_78;
create table p2_fmean20_78 as
select artist_id, floor(exp(plays)) as favors, to_char(Ds, 'yyyymmdd') as Ds
from liuhe_midmean2;
