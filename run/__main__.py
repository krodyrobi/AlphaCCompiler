from Lexer import Lexer
import os

lexer = Lexer()
#lexer.scan('./run/test_file')
#lexer.show_tokens()

test_dir = './run/tests/'
out_dir = './run/out/'
for filename in os.listdir(test_dir):
    file_path = test_dir + filename
    lexer.scan(file_path)

    with open(out_dir + filename + '.tk', 'w') as out:
        lexer.scan(file_path)
        for tokens in lexer.tokens:
            print(str(tokens), file=out)