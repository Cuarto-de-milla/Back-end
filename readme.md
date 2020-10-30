# Cuarto de Milla - API

## Pagination

The api provides a pagination system for make querys. 

### Query:
```
{
  allStations(first:2, after: "YXJyYXljb25uZWN0aW9uOjE=" ){
    pageInfo{
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
    edges{
      cursor
      node{
        name
        register
        state
      }
    }
  }
}

```
### Response

```
{
  "data": {
    "allStations": {
      "pageInfo": {
        "startCursor": "YXJyYXljb25uZWN0aW9uOjI=",
        "endCursor": "YXJyYXljb25uZWN0aW9uOjM=",
        "hasNextPage": true,
        "hasPreviousPage": false
      },
      "edges": [
        {
          "cursor": "YXJyYXljb25uZWN0aW9uOjI=",
          "node": {
            "name": "CIRCULO DOS, S.A. DE C.V.",
            "register": "PL/635/EXP/ES/2015"
          }
        },
        {
          "cursor": "YXJyYXljb25uZWN0aW9uOjM=",
          "node": {
            "name": "Becktrop Operadora SA de CV",
            "register": "PL/708/EXP/ES/2015"
          }
        }
      ]
    }
  }
}

```

### More Information:
See the documentation [here](https://github.com/graphql-python/graphene/wiki/Relay-Pagination-example)