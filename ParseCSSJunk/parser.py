f = open('parseme.txt', 'r')
base_string = f.read()
f.close()
lump_string = ''
g = open('fillme.txt', 'w')
div_count=0
for i in base_string:
    lump_string = lump_string + i
    if i == '{' or i == '}' or i==';' :
        print(lump_string)
        if lump_string[-1:]=='{':
            div_count+=1
        elif lump_string[-1:]=='}':
            if div_count>0:
                div_count-=1
            else:
                div_count=0
        g.write(' '*(div_count*2) + lump_string + '\n')
        lump_string = ''
g.close()
