# MySQL Command Line Cheatsheet 

## Launch MySQL from command line

Once MySQL is installed, open your terminal and type the following command.
```
$ mysql -u root -p
```
Then enter your password and ENTER.

## Locate

Find the location of the databases of the current server
```
mysql> select @@datadir;
```

## Explore

Show the databases of the running server
```
mysql> SHOW DATABASES;
```

Show the tables of a database.
```
mysql> USE name_database;
mysql> SHOW TABLES;
```
