# Graph Query Language
## Абстрактный синтаксис языка `Lagraph` (конкретный синтаксис определен в `Lagraph.g4`)
```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Set of expr

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
  | expr in expr                 // check that element in set after calculation
  | expr == expr                 // check that two values are equals

lambda = \ abstractor -> expr
```



Система типов:
В данном языка используются типы-обертки

* `FSMType` для конечного автомата (pyformlang.finite_automaton.EpsilonNFA)
* `LambdaType` для обертки над лямбда функцией

Для типа списка и множества используются стандартные типы языка питон (`set` и `list`). Логических типов нет, булева операция возвращает целочисленный 0 при ложном результате и 1 при истинном

Логика интерпретатора разделена: обход AST реализован как наследник класса `Visitor` от `ANTLR`. При обходе он вызывает семантический подпрограммы, которые используют методы, реализованные в предыдущих работах (`Semantic.py`). В семантических же подпрограммах происходит проверка корректности типов аргументов.

Из-за особенностей библиотек, стандартно используемых для работы с `dot` форматом, при загрузке графа из внешнего источника по умолчанию все его вершины помечаются как стартовые и финальные. Файл загружается с помощью команды `loadFrom` из файла, по имени из датасета `cfpq_data` или командой `fromExpr` из регулярного выражения в виде строки (используется `PythonRegex`)

Вершины, метки и грани графов являются множествами.

Операции объединения, пересечения, конкатенации и замыкания клини определены для графов.

При ошибках типизации бросается исключение `InterpretingError`, во время интерпретации кода из файла оно перехватывается, выдается сообщение об ошибке и работа завершается.

Для множеств определены операции `map` и `filter`. Как аргумент они принимают лямбда-функцию в заданном формате.


## Примеры запросов на языке (больше в тестах `tests/interpreter`)
``` python
-- load the graph with name "wine"
let w = loadFrom name "wine"

-- get the reachable vertices
let rchbl = reachableOf f1

-- load graph from file at path "g.dot"
let f1 = loadFrom path "g.dot"
let f2 = loadFrom path "f.dot"
print f1

let g = setStart {"a", "b", "c"} to f2

-- union of "l1" and "l2"
let u = f2 || f1

-- concatenation
let c = f1 ++ f2

-- intersect
let i = f1 && f2


-- use of filter and map
let forty = filter (\\x -> x == 42) on {1, 2, 3, 4, 42}
let forty = map (\\x -> 42) on {1, 2, 3, 4}

```

## Алгоритмы
* Для пересечения конечных автоматов используется алгоритм тензорного произведения, так как он  является единственным реализованным алгоритмом для данной задачи в рамках курса.
* Пересечение рекурсивного автомата и конечного автомата не было реализовано, поэтому не поддерживается.
*
## Запуск
Скрипт для запуска интерпретатора на файле находится в файле `scripts/lagraph.py`. Первым аргументом скрипта необходимо передать путь к файлу с кодом. Например:
```
python scripts/lagraph.py tests/interpreter/script.lg
```
