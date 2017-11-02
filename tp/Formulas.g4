grammar Formulas ;

/*
 * Parser Rules
 */
 
formula         : CHAR
                | '{' formula '}'
                | '(' formula ')'
                | formula '^' formula
                | formula '_' formula
                | formula '^' formula '_' formula
                | formula '_' formula '^' formula // aca deberiamos ocuparnos de que no son asociativos los indices
                | formula formula
                | formula '/' formula
                ;

/*
 * Lexer Rules
 */

CHAR    : ~('^' | '_' | '/' | '{' | '}' | '(' | ')') ;