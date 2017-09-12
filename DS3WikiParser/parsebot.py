stat_array = []
grand_array = []
number_array = []
stat_marker = False
count = 0
with open('parseme.txt', 'r') as source_file:
    for line in source_file:
##        print(count)
        if line[:12]=='<td style="w':
##            print(stat_array)
            found_trigger = False
            reverse_count = 1
            new_string = ''
            str_length = len(line)
            right_carrots = 0
            while found_trigger == False:
                letter = line[str_length-reverse_count]
                new_string += letter
                reverse_count += 1
                if letter == '>':
                    right_carrots += 1
                if right_carrots == 3:
                    found_trigger = True
            new_string = new_string[::-1][1:-10]
            print(stat_array)
            grand_array.append(stat_array)
            stat_array=[]
            stat_array.append(new_string)
            print(stat_array)
##            if count != 0: stat_array = []
        if line[:12]=='<td style="t':
            stat_array.append(line.strip()[45:-5])
        count += 1
    grand_array.append(stat_array)
    print(stat_array)
##    print(grand_array)
del grand_array[0]
##print(grand_array)

count2 = 0
##for i in grand_array:
##    numero = round(float(i[9])/float(i[14]), 2)
##    number_array.append(numero)
    
##    print(numero)
##print(number_array)
##print(max(number_array))
##print(grand_array[number_array.index(max(number_array))][0], '@', max(number_array))
