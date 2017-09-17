drop table  if exists mars_tianchi_user_actions;
Create table if not exists mars_tianchi_user_actions
as select * from odps_tc_257100_f673506e024.p2_mars_tianchi_user_actions;

drop table if exists mars_tianchi_songs;
create table if not exists mars_tianchi_songs
as select * from odps_tc_257100_f673506e024.p2_mars_tianchi_songs;
