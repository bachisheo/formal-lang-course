grammar Lagraph;
fragment WORD: [a-zA-Z_];
fragment DIGIT: [0-9];

prog: (s+=statement)* EOF;

statement: bind   #st_bind
          | print #st_print
          ;

bind: 'let' name=var '=' value=expr;
print: 'print' exp=expr;

lambda: '\\' var '->' expr ;
var_list: v1=var (',' v+=var_list)* | '(' v+=var_list ')' (',' v+=var_list)* ;

var: value=IDENT
  ;
val: value=INT    #int_literal
  | value=STRING  #string_literal
  | value=set     #set_literal
  ;

set:
	'{' INT '}'
	|'{' INT '..' INT '}'
  ;

expr:
  '(' e=expr ')'                                          #expr_brace
  | e=var                                                 #expr_var
  | e=val                                                 #expr_val
  | op=set_operator v=expr 'to' g=expr                       #expr_set
  | op=get_operator g=expr                                   #expr_get
  | e1=expr op=binary_operator e2=expr                       #expr_binop
  | op='map' '(' l=lambda ')' 'on' e=expr                               #expr_map
  | op='filter' '(' l=lambda ')' 'on' e=expr                            #expr_filter
  | 'load' ('path' path=STRING | 'graph' gname=STRING)    #expr_load
  | e1=expr '*'                                           #expr_star
  | 'oneStep' e=expr                                      #expr_one_step
  | e=expr 'in' s=expr                                  #expr_in_set
;

set_operator:
  'setStart'
  | 'setFinal'
  | 'addStart'
  | 'addFinal'
  ;

get_operator:
  'startOf'
  | 'finalOf'
  | 'reachableOf'
  |'verticesOf'
  | 'edgesOf'
  | 'labelsOf'
  ;

binary_operator:
  '&&'
  | '++'
  | '||'
  ;


COMMENT: '--'.*? ~[\n]* -> skip;
WHITESPACE : [ \t\r\n\u000C] -> skip;
INT: '0' | [1-9] DIGIT*;
IDENT: WORD (DIGIT | WORD)*;
STRING:  '"' .*? '"';
