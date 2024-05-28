grammar MyLanguage;


INT : [0-9]+ ;
FLOAT : [0-9]+'.'[0-9]+ ;
ID : [a-zA-Z]+ ;

PLUS : '+' ;
MINUS : '-' ;
MULT : '*' ;
DIV : '/' ;
EQ : '=' ;

LPAREN : '(' ;
RPAREN : ')' ;

RCORNER: '{';
LCORNER: '}';

GT: '>';
LT: '<';
EQ_EQ: '==';
NOT_EQ: '!=';

END_STATE: ';';

INCREMENT: PLUS PLUS;
DECREMENT: MINUS MINUS;



WS : [ \t\r\n]+ -> skip ;
NEWLINE:'\r'? '\n' ;

program : statement+ ;

statement : assignmentStatement |ifStatement|ifElseStatement|forStatement|whileStatement|printState|functionStatement|functionCall|return;



assignmentStatement : ID EQ expr END_STATE ;



ifStatement: 'if' equation RCORNER ifBody LCORNER END_STATE;
ifElseStatement: 'if' equation RCORNER ifBody LCORNER 'else' RCORNER elseBody LCORNER END_STATE;
//оператор для отслеживания тела
ifBody:  (statement)* ;
//Оператор отслеживания тела иначе
elseBody: (statement)* ;



forStatement: 'for' LPAREN forInit equation END_STATE forModify RPAREN RCORNER forBody LCORNER END_STATE;
//Оператор инициализации
forInit:  ID EQ expr END_STATE;
//Оператор декримента/инкремента
forModify: ID (INCREMENT|DECREMENT);
forBody: (statement)*;



whileStatement: 'while' LPAREN equation RPAREN RCORNER  whileBody LCORNER END_STATE;
whileBody: (statement)*;



functionStatement
   : funcType functionName LPAREN functionArgs? RPAREN RCORNER functionBody return? LCORNER END_STATE;

return
    : 'return' functionExpr END_STATE;

functionArgs: (ID (','ID)*)?;
functionBody: (statement)*;
functionName: ID;
funcType:
   | 'void'
   | 'int'
   | 'float'
   ;
functionExpr: ID
            | INT
            | FLOAT
            | functionCall
            | expr
            ;
functionParams: expr (',' expr)* ;
functionCall: functionName LPAREN functionParams? RPAREN END_STATE?;





printState
    :'print' LPAREN printBody RPAREN END_STATE;
printBody
    : ID| INT| FLOAT;



equation
   : expr op=comparison expr;


comparison
   : EQ_EQ| GT| LT| NOT_EQ;



expr : expr (MULT | DIV) expr
     | expr (PLUS | MINUS) expr
     | INT
     | FLOAT
     | ID
     | LPAREN expr RPAREN
     ;
