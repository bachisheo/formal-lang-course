grammar Lagraph;
fragment WORD: [a-zA-Z_];
fragment DIGIT: [0-9];

prog: (s+=statement)* EOF;

statement: bind   #st_bind
          | print #st_print
          ;

bind: 'let' name=var '=' value=expr;
print: 'print' expr;

lambda: '\\' var_list '->' expr ;
foo: lmb=lambda | '(' lmb=lambda ')';
var_list: v1=var (',' v+=var_list)* | '(' v+=var_list ')' (',' v+=var_list)* ;

var: value=IDENT  #var_node
  ;
val: value=INT    #int_literal
  | value=STRING  #string_literal
  | value=arr     #arr_literal
  ;

arr:
	'{' INT '}'
	|'{' INT '..' INT '}' ;

expr:
    '(' e=expr ')'                                        #expr_brace
  | e=var                                                 #expr_var
  | e=val                                                 #expr_val
  | 'setStart' v=expr 'to' g=expr                         #expr_set_start
  | 'setFinal' v=expr 'to' g=expr                         #expr_set_final
  | 'addStart' v=expr 'to' g=expr                         #expr_add_start
  | 'addFinal' v=expr 'to' g=expr                         #expr_add_final
  | 'startOf' l=expr                                  #expr_starts
  | 'finalOf' l=expr                                  #expr_finals
  | 'reachableOf' l=expr                              #expr_reach
  | 'verticesOf' l=expr                               #expr_get_vertex
  | 'edgesOf' g=expr                                  #expr_get_edges
  | 'labelsOf' g=expr                                 #expr_get_labels
  | 'map' f=foo 'on' e=expr                             #expr_map
  | 'filter' f=foo 'on' e=expr                          #expr_filter
  | 'load' ('path' path=STRING | 'graph' gname=STRING)         #expr_load
  | e1=expr '&&' e2=expr                                  #expr_intersect
  | e1=expr '++' e2=expr                                  #expr_concat
  | e1=expr '||' e2=expr                                  #expr_union
  | e1=expr '*'                                        #expr_star
  | 'oneStep' e=expr                                  #expr_one_step
  | e=expr 'in' set=expr                                  #expr_in_set
;

COMMENT: '--'.*? ~[\n]* -> skip;
WHITESPACE : [ \t\r\n\u000C] -> skip;
INT: '0' | [1-9] DIGIT*;
IDENT: WORD (DIGIT | WORD)*;
STRING:  '"' .*? '"';
