# Graph Query Language
## Abstract syntax of language `Lagraph` (concrete syntax is in file `Lagraph.g4`)
```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | RangeSet of int * int   // set of int numbers in range

expr =
    Var of var                   // variables
  | Val of val                   // constants
  | Set_start of Set<val> * expr // set the set of start states
  | Set_final of Set<val> * expr // set the set of final states
  | Add_start of Set<val> * expr // add states to the set of start states
  | Add_final of Set<val> * expr // add states to the set of final states
  | Get_start of expr            // get the set of start states
  | Get_final of expr            // get the set of final states
  | Get_reachable of expr        // get all pairs of reachable vertices
  | Get_vertices of expr         // get all vertices
  | Get_edges of expr            // get all edges
  | Get_labels of expr           // get all labels
  | Map of lambda * expr         // classic map
  | Filter of lambda * expr      // classic filter
  | Load of path                 // loading a graph
  | Intersect of expr * expr     // intersection of languages
  | Concat of expr * expr        // concatenation of languages
  | Union of expr * expr         // union of languages
  | Star of expr                 // closure of languages (Kleene star)
  | Smb of expr                  // single transition

lambda = \ list of abstractors -> expr
```

## Some script examples
``` haskell
-- load the graph with name "wine"
let f = load graph "wine"

-- get the reachable vertices
let rchbl = reachableOf f

-- load graph from file at path "g.dot"
let f2 = load graph "g.dot"

let g = setStart (setFinal f to (verticesOf f)) to {0..100}

-- union of "l1" and "l2"
let l1 = "l1" || "l2"

-- closure of the union of languages
let q1 = ("type" || l1)*

-- concatenation
let q2 = "sub_class_of" ++ l1

-- union
let res1 = g && q1
let res2 = g && q2

-- print the result (returns a string representation)
print res1

-- use of filter and map
let v1 = filter (\ v -> v in s) on (map (\ (u_g,u_q1),l,(v_g,v_q1) -> u_g) on (edgesOf res1))
let v2 = filter (\ v -> v in s) on (map (\((u_g,u_q2),l,(v_g,v_q2)) -> u_g) on (edgesOf res2))
let v = v1 && v2

-- print the list of vertices
print (startOf g)
```
