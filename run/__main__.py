from Lexer import Lexer
from Syntax import Syntax
import os

lexer = Lexer()
# lexer.scan('./run/test_file')
# lexer.show_tokens()

#test_dir = './run/lexer_tests/'
#out_dir = './run/out/lexer/'
#for filename in os.listdir(test_dir):
#    file_path = test_dir + filename
#    lexer.scan(file_path)

#    with open(out_dir + filename + '.tk', 'w') as out:
#        lexer.scan(file_path)
#        for tokens in lexer.tokens:
#            print(str(tokens), file=out)

lexer.scan('./run/test_syntax_file')
syntax = Syntax(lexer.tokens)
lexer.show_tokens()
print(syntax.start())
