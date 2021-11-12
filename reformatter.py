# A reformatter. This is for Pascal but with the notes in the comments it should
# just take a couple of minutes to change it to whatever language you please.

# It's written to automatically apply itself to all the .pas files in the
# directory it finds itself in. It goes through them and applies the whitespace
# rules found in the function rewhitespace, and the rules for changing the names
# of variables and functions found in the dictionary tdic. It prints out the name
# of each file it's procesing as it goes to let you know it's doing something.

# Finally it prints out a list of all the variable/function names so you can
# use this to plan futher refactoring. (It will also include all the keywords
# of the language like if and else and so on unless you put some sort of filter
# in to tell it not to.)

import os

# My whitespace rules: spaces before and after :=, =, <, >, <>, +, and -.
# Spaces after but not before , and :

# This is a very crude way of doing it but the program runs so fast I don't care.

def rewhitespace(s):
    s = s.replace('=',' = ')
    s = s.replace('  =',' =')
    s = s.replace('=  ','= ')
    s = s.replace(': =',':=')
    s = s.replace(':',': ')
    s = s.replace(':  ',': ')
    s = s.replace(': =',':=')
    s = s.replace(' :', ':')
    s = s.replace(': =',': =')
    s = s.replace(':=', ' :=')
    s = s.replace('+',' + ')
    s = s.replace('  +',' +')
    s = s.replace('+  ','+ ')
    s = s.replace('-',' - ')
    s = s.replace('  -',' -')
    s = s.replace('-  ','- ')
    s = s.replace('<',' < ')
    s = s.replace('  <',' <')
    s = s.replace('<  ','< ')
    s = s.replace('>',' > ')
    s = s.replace('  >',' >')
    s = s.replace('>  ','> ')
    s = s.replace('< >','<>')
    s = s.replace('< =','<=')
    s = s.replace('> =','>=')
    s = s.replace(' ,', ',')
    s = s.replace(',',', ')
    s = s.replace(',  ',', ')
    return s;

# The dictionary for changing the names of functions and variables, e.g.
# if you want to change qp to QuantityOfPorcupines you would add
# 'qp' : 'QuantityOfPorcupines' to the dictionary.

tdic = {
        
       }

tokens = []
files = os.listdir(os.curdir)
for filename in files:
    if filename[-4:] == '.pas':    # Cos I'm looking for Pascal files.
        print(filename)
        text_file = open(filename, "r", encoding = "utf8")
        data = text_file.read()
        text_file.close()
        output = ''
        i = 0
        mode = 'plain'
        # By 'plain' I mean not in comments or quotes.
        while i < len(data):
            new_mode = 'plain'
            if mode == 'plain':
                # ... then we look for the start of non-plain text.
                min_c1 = data.find('{',i) # The start of a multiline comment.
                if min_c1 == -1:
                    min_c1 = len(data)
                min_c2 = data.find('//',i) # The start of a single-line comment
                if min_c2 == -1:
                    min_c2 = len(data)
                min_qu = data.find('\'',i) # The start of a string literal
                if min_qu == -1:
                    min_qu = len(data)
                min_al = min([min_c1, min_c2, min_qu])
                new_i = min_al
                if min_al == len(data):
                    pass
                elif min_al == min_c1:
                    new_mode = 'multiline_comment'
                elif min_al == min_c2:
                    new_mode = 'single_line_comment'
                elif min_al == min_qu:
                    new_mode = 'string_literal'
            elif mode == 'multiline_comment':
                new_i = data.find('}',i+1) + 1
            elif mode == 'single_line_comment':
                new_i = data.find('\n',i+1) + 1
            elif mode == 'string_literal':
                new_i = data.find('\'',i+1) + 1
                        
            if mode == 'plain':
                respaced = rewhitespace(data[i:new_i])

                # We tokenize the plain text.
                #
                # I think the rules for variable/function names are pretty much the same for every language:
                # they must begin with an alphabetic character or an underscore and subsequent characters can
                # be alphabetic, numeric, or an underscore. If your favorite language is different it's easy
                # to fix.
                
                tkn = False
                retokened = ''
                for j in range(len(respaced)+1):
                    if tkn:
                        if j == len(respaced) or not (respaced[j].isalnum() or respaced[j] == '_'):
                            token = respaced[tknstart:j]
                            if token in tdic.keys(): # Instead of these two lines,
                                token = tdic[token]  # in my original version I had:
                            #
                            # cf = token.casefold()
                            # if cf in tdic.keys():
                            #    token = tdic[cf]
                            #
                            # This is because Pascal is a case-insensitive language, and consistent casing
                            #  is something I was trying to enforce. If you combine this with making all the 
                            # keys in the tdic lower-case, it lets you do that.
                            # 
                            # This would be bad if applied to a case-sensitive language, so I have commented
                            # it out for your safety, 'cos most languages are case-sensitive.
                            # 
                            if not token in tokens:
                                tokens.append(token)
                            retokened = retokened + token
                            tkn = False
                            if j != len(respaced):
                                retokened = retokened + respaced[j]
                    else:
                        if j == len(respaced):
                            break
                        if respaced[j].isalpha() or respaced[j] == '_':
                            tknstart = j    
                            tkn = True
                        else:
                            retokened = retokened + respaced[j]
                    

                output = output + retokened
            else: # Else we're in a comment or a string literal and mustn't process it.
                output = output + data[i:new_i]

            i = new_i
            mode = new_mode

        text_file = open(filename, "w", encoding = "utf8")
        text_file.write(output)
        text_file.close()

# Finally we print out the list of variable/function names (and of course the keywords of the language
# like if and else, unless you filter them out.)

tokens.sort()
print(tokens)

# It can be useful to print these out in such a form that they can for the basis for entries in your tdic
# For example my code ended like this because that's a fair start on what I was trying to achieve with the
# capitalization:

# for t in tokens:
#    print('    \''+t.casefold()+'\' : \''+t[0].capitalize()+t[1:]+'\',')
