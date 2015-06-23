import os
from modules.domain_analysis.Domain import Domain

from modules.lexical_analyzer.Lexer import Lexer
from modules.syntactical_analyzer.Syntax import Syntax


lexer = Lexer()
# lexer.scan('./run/test_file')
# lexer.show_tokens()

cwd = os.getcwd()
#test_dir = cwd + '/lexer_tests/'
#out_dir = cwd + '/out/lexer/'
#for filename in os.listdir(test_dir):
    # file_path = test_dir + filename
    # lexer.scan(file_path)
    #
    # with open(out_dir + filename + '.tk', 'w') as out:
    #     lexer.scan(file_path)
    #     for tokens in lexer.tokens:
    #         print(str(tokens), file=out)
    #
    # syntax = Syntax(lexer.tokens)
    # print("%s => %s" % (filename, str(syntax.start())))


lexer.scan(cwd + '/test_da')
domain = Domain(lexer.tokens)
lexer.show_tokens()
print("\n\n")
domain.start()


# lexer.scan('./run/test_syntax_file')
# syntax = Syntax(lexer.tokens)
# lexer.show_tokens()
# print(syntax.start())
