stat_array = []
grand_array = []
number_array = []
stat_marker = False
count = 0


stat_list = {'Name':0, 'Pysical Resistance':1, 'Strike Defense':2, 'Slash Defense':3,
             'Thrust Defense':4, 'Magic Defense':5, 'Fire Defense':6, 'Lightning Defense':7,
             'Dark Defense':8, 'Bleed Resistance':9, 'Poison Resistance':10, 'Frost Resistance':11,
             'Curse Resistance':12, 'Poise':13, 'Weight':14, 'Durability':15}

with open('parseme.txt', 'r') as source_file:
    for line in source_file:
        if line.strip()[:12]=='<td style="w' and 'margin-left' not in line and '&amp' not in line:
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
            grand_array.append(stat_array)
            stat_array=[]
            stat_array.append(new_string)
        if line[:12]=='<td style="t':
            stat_array.append(line.strip()[45:-5])
    grand_array.append(stat_array)
del grand_array[0]

def stat_value(key, array):
    num = array[stat_list[key]]
    return num

count2 = 0
for i in grand_array:
##    if float(stat_value('Weight', i))>20:
##        numero = round(float(stat_value('Poise', i))/float(stat_value('Weight', i)), 2)
##        if numero>1.2:
        numero=round(float(stat_value('Weight', i)))
        print(stat_value('Name', i))
        number_array.append(numero)

print(grand_array[number_array.index(max(number_array))][0], '@', max(number_array))
