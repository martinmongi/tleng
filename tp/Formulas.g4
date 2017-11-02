grammar Formulas ;

/*
 * Parser Rules
 */
 
formula         : expression NEWLINE ;

expression         : CHAR
                | '{' expression '}'
                | '(' expression ')'
                | expression '^' expression
                | expression '_' expression
                | expression '^' expression '_' expression
                | expression '_' expression '^' expression // aca deberiamos ocuparnos de que no son asociativos los indices
                | expression expression
                | expression '/' expression
                ;

/*
 * Lexer Rules
 */

NEWLINE : '\n'+ ;
CHAR    : ~('^' | '_' | '/' | '{' | '}' | '(' | ')' | '\n') ;
