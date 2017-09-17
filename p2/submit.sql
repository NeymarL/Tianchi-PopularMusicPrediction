-- susubbmit result

drop table if exists mars_tianchi_artist_plays_predict;
create table mars_tianchi_artist_plays_predict as
select artist_id, Plays, Ds from mean201410low;
