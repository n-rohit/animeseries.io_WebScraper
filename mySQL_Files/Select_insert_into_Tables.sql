select * from animeapp_anime
select * from animeapp_episodes

desc animeapp_anime
desc animeapp_episodes

insert into animeapp_anime values ('ANIME0001','.Hack//G.U. Returner','https://gogocdn.net/images/anime/5745.jpg',
'hack//G.U. Returner is a single-episode OVA offered to fans who completed all three GU Games, featuring characters from the .hack//G.U. Games and .hack//Roots.',
'Completed',2007,'Adventure,Drama,Game,Harem,Martial Arts,Seinen','.Hack//G.U. Returner Episode 1',date_format('2009-12-31 16:00:00','%Y-%m-%d %H:%i:%S'),
'//streamani.net/streaming.php?id=NDA1OTI=&title=.Hack%2F%2FG.U.+Returner+episode+1&typesub=SUB')

-- insert into animeapp_anime values('ANIME0001','A1','tlink','desc','Completed',2009,'Action,Adventure','epsiode 1',date_format('2009-12-31 16:00:00','%Y-%m-%d %H:%i:%S'),'vidlink')
-- select date_format(NOW(), '%Y-%m-%d %H:%i:%S')
-- desc animeapp_anime
