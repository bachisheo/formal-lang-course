grammar Lagraph;
fragment WORD: [a-zA-Z_];
fragment DIGIT: [0-9];

prog: (statement)* EOF;

statement: bind | print;

bind: 'let' var '=' expr;
print: 'print' expr;

lambda: '\\' var_list '->' expr ;
foo: lambda | '(' lambda ')';
var_list: var (',' var_list)* | '(' var_list ')' (',' var_list)* ;

var: IDENT;
val: INT | STRING | intGenerator;

intGenerator:
	'{' INT '}'
	|'{' INT '..' INT '}' ;

expr:
    '(' expr ')'
  | var                             // variables
  | val                             // constraints
  | 'setStart' expr 'to' expr            // set the set of start states
  | 'setFinal' expr 'to' expr            // set the set of final states
  | 'addStart' expr 'to' expr            // add states to the set of start states
  | 'addFinal' expr 'to' expr            // add states to the set of final states
  | 'startOf' expr                  // get the set of start states
  | 'finalOf' expr                  // get the set of final states
  | 'reachableOf' expr              // get all pairs of reachable vertices
  | 'verticesOf' expr               // get all vertices
  | 'edgesOf' expr                  // get all edges
  | 'labelsOf' expr                 // get all the labels
  | 'map' foo 'on' expr               // classic map
  | 'filter' foo 'on' expr            // classic filter
  | 'load' ('path' STRING | 'graph' STRING)  // loading a graph from a file | by name
  | expr '&&' expr                  // intersection of languages
  | expr '++' expr                  // concatentation of languages
  | expr '||' expr                  // union of languages
  | expr '*'                        // closure of languages (Kleene star)
  | 'oneStep' expr                  // single transition
  | expr 'in' expr                  // check membership of set
;

COMMENT: '--'.*? ~[\n]* -> skip;
WHITESPACE : [ \t\r\n\u000C] -> skip;
INT: '0' | [1-9] DIGIT*;
IDENT: WORD (DIGIT | WORD)*;
STRING:  '"' .*? '"';
