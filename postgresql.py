import psycopg2,time
from pprint import pprint

# 初始化连接
conn = psycopg2.connect(database='wcdma_mr', user='postgres', password='root', host="10.231.143.105", port='5432')

# 创建指针对象
cur = conn.cursor()


#  初始化数据库
def initTable():
    try:
        cur.execute("""
                -- 创建 postgis 插件
                -- create extension dblink;
                -- CREATE EXTENSION postgis;
                -- CREATE EXTENSION postgis_topology;

                -- 修改会话参数
                SET enable_seqscan TO on;
                SET enable_indexscan TO on;
                set force_parallel_mode =on;
                set max_parallel_workers_per_gather = 64;


                DROP TABLE IF EXISTS tdlte_mro;
                create table public."tdlte_mro"
                (	v_fposition_id integer,
                    object_fposition_id integer,
                    mroid integer,
                    enb_id integer,
                    object_id integer,
                    n_cellid integer,
                    object_id_detial integer,
                    object_mmeues1apid integer,
                    object_mmegroupid integer,
                    object_mmecode integer,
                    object_timestamp timestamp,
                    object_msec integer,
                    mr_ltescrsrp integer,
                    mr_ltescrsrq integer,
                    mr_ltesctadv integer,
                    mr_ltescphr integer,
                    mr_ltescaoa integer,
                    mr_ltescsinrul integer,
                    mr_ltescearfcn integer,
                    mr_ltescpci integer,
                    mr_ltencrsrp integer,
                    mr_ltencrsrq integer,
                    mr_ltencearfcn integer,
                    mr_ltencpci integer
                );
                alter table public."tdlte_mro" owner to postgres;
                """)
        return 1

    except Exception as error:
        print(str(error))
        return 0


# 导入csv数据到数据库
def inPg(csvFileName):
    cur.execute("""copy tdlte_mro 
        FROM {} 
        CSV HEADER ENCODING 'utf-8' DELIMITER ','  NULL '';
        """.format(csvFileName))


# 查询数据库 返回查询结果
def queryPg(sql):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return list(rows)
    except Exception as error:
        print(str(error))
        return 0


if __name__ == "__main__":
    # 初始化数据表
    if initTable():
        queryResult = queryPg('select *  from tdlte_mro limit 10')
        pprint(queryResult)