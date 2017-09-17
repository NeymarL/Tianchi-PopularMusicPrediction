-- track feature

drop table if exists lh_feats1;
create table if not exists lh_feats1 as
select A.artist_id, A.plays, A.ds, B.wday, floor(C.mday) as mday, D.flag as holiday, A.artist_id as aid,
       E.weekend as weekend, J.gender as gender, (F.song_init_plays + 1) as publish
from all_data A
left outer join
(
    select Ds, weekday(to_date(Ds, 'yyyymmdd')) as wday  from lh_alds
) B
on A.ds = B.ds
left outer join
(
    select Ds, to_char(to_date(Ds, 'yyyymmdd'), 'dd') as mday from lh_alds
) C
on A.ds = C.ds
left outer join
(
    select Ds, 1 as flag from lh_alds 
    where Ds = 20150305 or (Ds >= 20150404 and Ds <= 20150406) or
        (Ds >= 20150501 and Ds <= 20150503) or (Ds >= 20150620 and Ds <= 20150622) or 
        (Ds >= 20150926 and Ds <= 20150928) or (Ds >= 20151001 and Ds <= 20151007)
) D
on A.ds = D.ds
left outer join 
(
    select Ds, 1 as weekend from lh_alds
    where weekday(to_date(Ds, 'yyyymmdd')) = 5 or weekday(to_date(Ds, 'yyyymmdd')) = 6
) E
on A.ds = E.ds
left outer join mars_tianchi_songs F
on A.artist_id = F.artist_id and A.ds = F.publish_time
left outer join mars_tianchi_songs J
on A.artist_id = J.artist_id;

drop table if exists lh_feats2;
create table if not exists lh_feats2 as
select /*+ mapjoin(G, H, I)*/ distinct A.artist_id, A.plays, A.ds,
       G.flag as publish_week, H.flag as publish_half_mon, I.flag as publish_one_mon
from all_data A
left outer join song_data1 G
on A.artist_id = G.artist_id and A.ds <= G.publish_time + 7
left outer join song_data1 H
on A.artist_id = H.artist_id and A.ds <= H.publish_time + 15
left outer join song_data1 I
on A.artist_id = I.artist_id and A.ds <= I.publish_time + 30;

drop table if exists lh_feats;
create table if not exists lh_feats as
select distinct A.artist_id, A.plays, A.ds, A.wday, A.mday, A.holiday, A.aid, A.weekend,
       A.publish, B.publish_week, B.publish_half_mon, B.publish_one_mon, A.gender
from lh_feats1 A
left outer join lh_feats2 B
on A.artist_id = B.artist_id and A.ds = B.ds; 
