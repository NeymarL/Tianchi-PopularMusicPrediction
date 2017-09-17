-- evaluation

drop table if exists middle_results;
create table if not exists middle_results as
select sqrt(sum(pow(C.diff, 2)) / 60) as sigma, sqrt(sum(C.plays)) as fi
from
(
    select A.artist_id as artist_id, ((A.Plays - B.plays) / B.plays) as diff, B.plays as plays
    from mean201410low A
    left outer join mean201410low B
    on A.artist_id = B.artist_id and A.Ds = B.Ds
) C
group by C.artist_id;


select sum((1 - sigma) * fi) as score
from middle_results;

-- 67   63995.85            56      63707.70            45  63515
-- 15   51151       79.9%           51511       80.9%       48815
-- 10   50812       79.4%           51999       81.6%       49718   78.3%
-- 20   51399       80.4%           51251       80.4%       48337
