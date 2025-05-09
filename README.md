# repo explore

## getting started

1. run the database: `docker compose up -d`
2. run the application: 

```
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     python src/main.py # download repo and process .git folder TAKES A LONG TIME
```
3. as soon as the python starts running, you can access the neo4j localhost w/ user: neo4j password: password `http://localhost:7474/browser/preview/`

4. you only need to successfully run the application one time (so far).

## the "plan" from here
  - improve the `neo4j_driver.py` methods
    add functionality for various other types of Nodes and Edges
  - add more and more data into the thing (duplicate some of the data into relations and nodes for easier query)
  - design some queries we think help us out
  - create some routes that can display these type of results
  - create a front end to show the results we like

## start learning neo4j

Cypher cheatsheet https://neo4j.com/docs/cypher-cheat-sheet/5/all/

### Query with the interface at localhost

access the neo4j localhost w/ user: `neo4j` password: `password` `http://localhost:7474/browser/preview/`

You can get a nice pattern match from: `MATCH (n1:Actor)-[r:Authored]->(n2:Commit) RETURN n1, r, n2`

You can get a simple result from: `MATCH (c:Commit) RETURN c.hexsha, c.message LIMIT 10`

```
match (a)-[aa:AUTHORED]->(c:Commit)
// where not c.summary CONTAINS "Merge"
// WITH DISTINCT a 
MATCH (a:Actor)-[aa:AUTHORED]->(c:Commit)<-[ar:COMMITTED]->(a)
where aa.authored_date < 1542067894  // note we are limiting the time here
return  a, ar, aa, c 
```

## neo4j python driver

https://pypi.org/project/neo4j/

see `neo4j_driver.py` in this repo for more details.

## dependencies

these are found in requirements.txt
`GitPython` https://gitpython.readthedocs.io/en/stable/reference.html#api-reference-toplevel
<!-- `gitdb` https://gitdb.readthedocs.io/en/latest/ -->


## indexes created

`CREATE INDEX index_name IF NOT EXISTS FOR (p:Actor) ON (p.name, p.email)`