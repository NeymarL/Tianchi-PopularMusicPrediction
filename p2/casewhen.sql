drop table if exists testcase;
create table if not exists testcase as
select A.artist_id, 
    case least(abs(B.plays - A.plays), abs(C.plays - A.plays), abs(D.plays - A.plays), abs(E.plays - A.plays), abs(F.plays - A.plays))
        when (abs(B.plays - A.plays)) then B.plays
        when (abs(C.plays - A.plays)) then C.plays
        when (abs(D.plays - A.plays)) then D.plays
        when (abs(E.plays - A.plays)) then E.plays
        when (abs(F.plays - A.plays)) then F.plays
    end as plays, A.ds
from meanlast A
left outer join mean10 B
on A.artist_id = B.artist_id and A.ds = B.ds
left outer join mean14 C
on A.artist_id = C.artist_id and A.ds = C.ds
left outer join mean20 D
on A.artist_id = D.artist_id and A.ds = D.ds
left outer join mean30 E
on A.artist_id = E.artist_id and A.ds = E.ds
left outer join mean60 F
on A.artist_id = F.artist_id and A.ds = F.ds
order by artist_id, ds limit 100000;

select * from testcase;
