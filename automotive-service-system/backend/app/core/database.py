26184	postgres	DBeaver 25.3.3 - Main <symplicar_teste>	127.0.0.1	idle	2026-01-27 09:52:58.839 -0300	ALTER DATABASE symplicar_teste RENAME TO simplycar_teste
24996	postgres	DBeaver 25.3.3 - Metadata <symplicar_teste>	127.0.0.1	idle	2026-01-27 09:52:58.939 -0300	SELECT c.relname,a.*,pg_catalog.pg_get_expr(ad.adbin, ad.adrelid, true) as def_value,dsc.description,dep.objid
FROM pg_catalog.pg_attribute a
INNER JOIN pg_catalog.pg_class c ON (a.attrelid=c.oid)
LEFT OUTER JOIN pg_catalog.pg_attrdef ad ON (a.attrelid=ad.adrelid AND a.attnum = ad.adnum)
LEFT OUTER JOIN pg_catalog.pg_description dsc ON (c.oid=dsc.objoid AND a.attnum = dsc.objsubid)
LEFT OUTER JOIN pg_depend dep on dep.refobjid = a.attrelid AND dep.deptype = 'i' and dep.refobjsubid = a.attnum and dep.classid = dep.refclassid
WHERE NOT a.attisdropped AND c.relkind not in ('i','I','c') AND c.oid=$1
ORDER BY a.attnum
25748	postgres	DBeaver 25.3.3 - SQLEditor <Script.sql>	127.0.0.1	active	2026-01-27 10:25:13.588 -0300	"SELECT pid, usename, application_name, client_addr, state, backend_start, query
FROM pg_stat_activity
WHERE datname = 'symplicar_teste'
ORDER BY backend_start"