# Ejercicio 3

Insertando datos: 

```bash
docker run --interactive --rm --network cp-platform_default   confluentinc/cp-kafkacat   kafkacat -b broker:9092  -t t1 -P <<EOF
1:11,111
2:22,222
3:33,333
1:1:1
2:2:2
1:1,1
2:2,2
3:3,3
3:2,1
2:3,1
1:3,2
EOF

docker run --interactive --rm --network cp-platform_default   confluentinc/cp-kafkacat   kafkacat -b broker:9092  -t t2 -P <<EOF
1:22,333  
2:33,111
3:11,222
1:2,3
2:3,1
3:1,2
EOF

```

Ejemplos de consultas

```
create stream t1_s(id bigint, word varchar) with (kafka_topic='t1', value_format='DELIMITED');
create stream t2_s(id bigint, word varchar) with (kafka_topic='t2', value_format='DELIMITED');
create table t1_t(id bigint, word varchar) with (kafka_topic='t1', value_format='DELIMITED', key='id');
create table t2_t(id bigint, word varchar) with (kafka_topic='t2', value_format='DELIMITED', key='id');

select * from t1_s inner join t2_s on t1_s.word = t2_t.word;
select * from t1_s inner join t2_s on t1_s.id = t2_t.word;


select * from t1_s inner join t2_t on t1_s.id = t2_t.id;
select * from t1_s left join t2_t on t1_s.id = t2_t.id;
select * from t1_s left join t2_t on t1_s.rowkey = t2_t.id;

select * from t1_s left join t2_t on t1_s.id = t2_t.id;
select * from t1_s left join t2_t on t1_s.word = t2_t.id;
select * from t1_s left join t2_t on t1_s.word = t2_t.word;
select * from t1_s left join t2_t on id = id;
select * from t1_s left join t2_t on t1_s.id = t2_t.id;
select * from t1_s inner join t2_t on t1_s.id = t2_t.id;
select * from t1_s inner join t2_t on t1_s.rowkey = t2_t.id;

create stream ts as select 't1' as o, * from t1_s;
select * from ts;
insert into ts select 't2' as o, * from t2_s;
select * from ts;
insert into ts select 't2_t' as o, * from t2_t;

create table ts as select 't1' as o, * from t1_s;
create table ts_t as select 't1' as o, * from t1_t;
select * from ts_t

insert into ts_t select 't2_t' as o, * from t2_t;

show tables
show tables;
show streams;
```
