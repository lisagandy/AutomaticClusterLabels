Create table collocate_1 (main_id int primary key auto_increment, id_word1 int, word1 varchar(50), pos1 varchar(10) ,word2 varchar(50),pos2 varchar(10), freq float(5), MI float(5), coll_before_node float(5), id_collocate_maybe int)

CREATE INDEX index_word1 ON collocate_1 (word1);
CREATE INDEX index_word2 ON collocate_1 (word2);
create index index_word1_pos1 on collocate_1 (word1,pos1);
create index index_word1_pos2 on collocate_1 (word2,pos2);
create index index_pos on collocate_1(pos1);
create index index_pos2  on collocate_1(pos2);

load data local infile '/Users/lisa/Desktop/misc/coca_60k_new.txt' into table collocate_1
fields terminated by '\t'
lines terminated by '\n'
(id_word1,word1,pos1,word2,pos2,freq,MI,coll_before_node, id_collocate_maybe);

#enclosed by '"'
#Create table collocate_2 (main_id int primary key auto_increment, id_word1 int, word1 varchar(50), pos1 varchar(10) ,word2 varchar(50),pos2 varchar(10), freq float(5), MI float(5), coll_before_node float(5), id_collocate_maybe int)

