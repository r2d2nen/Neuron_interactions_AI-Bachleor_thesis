import fileinput

class EditText:
    def fix_file(self, fileToSearch, oldLine, newLine):
        for line in fileinput.input(fileToSearch, inplace=True): 
              print line.replace(oldLine, newLine),
