from Lexer import Lexer

lexer = Lexer()
lexer.scan('./run/test_file')

lexer.show_tokens()