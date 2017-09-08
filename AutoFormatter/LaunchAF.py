import os
cwd = os.getcwd()
dirlist = os.listdir(cwd)

with open('zero-header.txt', 'r') as f:
    header_text = f.read()

with open('zero-footer.txt', 'r') as f:
    footer_text = f.read()

write_state = False
##print(dirlist)

for file in dirlist:
    if str(file)[-5:]=='.html' and str(file)[:5].lower()!='zero-':
        print('modding {}'.format(file))
##        base_file = open(file, 'r+')
        with open(file, 'r+') as base_file:
            str_content_data = ''
            for line in base_file:
                if line.strip()[:7].lower()=='<title>':
                    print('Page Title: {}'.format(line.strip()[7:-8]))
                    page_title = line.strip()[7:-8]
                if line.strip()=="<div class='content'>":
                    write_state = True
                if line.strip()=="<div class='footer'>":
                    write_state = False
                if write_state==True:
                    str_content_data += line

            base_file.seek(0)
            base_file.truncate()
            base_file.write(header_text.format(page_title) +'\n')
            base_file.write(str_content_data +'\n')
            base_file.write(footer_text +'\n')
##            str_content_data = ''
##            base_file.close()
