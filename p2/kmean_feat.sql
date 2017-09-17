
drop table if exists kmean_feats;
create table if not exists kmean_feats as
select distinct A.artist_id, B.plays as mean30, C.plays as mean15, D.plays as meanall, E.plays as std,
                ((F.plays - D.plays) / D.plays) as maxdiff
from liuhe_arts_data A
left outer join
(
    select artist_id, avg(Plays) as Plays
    from liuhe_arts_data
    where Ds >= 20150801
    group by artist_id
) B
on A.artist_id = B.artist_id
left outer join
(
    select artist_id, avg(Plays) as Plays
    from liuhe_arts_data
    where Ds >= 20150815
    group by artist_id
) C
on A.artist_id = C.artist_id
left outer join
(
    select artist_id, avg(Plays) as Plays
    from liuhe_arts_data
    group by artist_id
) D
on A.artist_id = D.artist_id
left outer join
(
    select artist_id, stddev(Plays) as Plays
    from liuhe_arts_data
    group by artist_id
) E
on A.artist_id = E.artist_id
left outer join
(
    select artist_id, max(Plays) as Plays
    from liuhe_arts_data
    group by artist_id
) F
on A.artist_id = F.artist_id;
