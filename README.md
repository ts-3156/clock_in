# clock_in

```
pip install nfcpy requests
```

```
sqlite3 clock_in.sqlite3
```

```
sqlite> create table users(id integer primary key autoincrement, name text, idm text, is_working boolean);
sqlite> create unique index idm_i on users(idm);
```



```
sqlite> insert into users (name, idm, is_working) values ('shino', 'iiddmm', '0');
```

```
SLACK_TOKEN=T SLACK_CHANNEL=C sudo --preserve-env python app.py
```
