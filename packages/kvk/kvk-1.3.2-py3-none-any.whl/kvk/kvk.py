class KvK:
    def __init__(self, filePath):
        self.filePath = filePath
        self.__startingContent__()
        self.pos = 0
    
    # private methods
    def __startingContent__(self):
        if self.filePath[len(self.filePath) - 4: len(self.filePath)] != '.kvk':
            raise Exception('File extension must be \".kvk\"')
        else:
            try: #if file already exists reads content
                self.file = open(self.filePath, 'r')
            except: # if doesn't exist creates it and puts standard content
                self.file = open(self.filePath, 'w')
                self.content = '<#\n#>'
            else:
                self.content = self.file.read()

    def __getClass__(self):
        tmpDict = {} # container for class and attributes

        self.pos += 5 # +5 <-- len('class') = 5

        while self.text[self.pos] == ' ': # ignores spaces
            self.pos += 1

        if self.text[self.pos] == '"': # if " is found

            self.pos += 1
            className = '' # class name initialiser

            while self.text[self.pos] != '"': # scans until the following "
                className += self.text[self.pos] # addts chars to class name
                self.pos += 1

            self.pos += 1
            while self.text[self.pos] == ' ':  # ignores spaces
                self.pos += 1

            self.insideDict = {} # container for attributes
            if self.text[self.pos:self.pos + 3] == '::>': # attributes signalator
                self.pos += 3 # +3 <-- len('::>') = 3

                while self.text[self.pos:len(self.text)] != '#>' and self.text[self.pos:self.pos + 5] != 'class':
                    if self.text[self.pos] == ' ' or self.text[self.pos] == '\t' or self.text[self.pos] == '\n': # ignores spaces, new lines and tabs
                        self.pos += 1

                    elif self.text[self.pos] == '(': # if founds parentheses, which initialises an attribute
                        self.__attr__()

                    tmpDict[className] = self.insideDict # adds attributes inside container

                return tmpDict # returns the container with the attributes
            else:
                raise SyntaxError('Expected "::>" after class name.')
        else:
            raise SyntaxError('Expected \'\"\' after class declaration.')

    def __attr__(self):
        self.pos += 1
        attrName = '' # attribute name initialiser

        while self.text[self.pos] == ' ' or self.text[self.pos] == '\t' or self.text[self.pos] == '\n':
            self.pos += 1 # skips spaces, tabs and new lines

        while self.text[self.pos] != ')': # until il founds )
            attrName += self.text[self.pos] # adds chars to attribute name
            self.pos += 1

        self.pos += 1

        while self.text[self.pos] == ' ' or self.text[self.pos] == '\t' or self.text[self.pos] == '\n':
            self.pos += 1 # skips spaces, tabs and new lines

        if self.text[self.pos:self.pos + 2] == '->': # initialiser for attribute content
            self.pos += 2 # +2 <-- len('->') = 2

            while self.text[self.pos] == ' ': # skips spaces
                self.pos += 1

            if self.text[self.pos] == '"': # attribute content initialiser
                attr = ''
                self.pos += 1

                while self.text[self.pos] != '"':
                    attr += self.text[self.pos] # adds chars to attribute content
                    self.pos += 1

                self.insideDict[attrName] = attr # replaces return
                self.pos += 1
            else:
                raise SyntaxError('Expected '"' after ->")
        else:
            raise SyntaxError('Expected -> after attribute name')

    def __repr__(self):
        return f'< KvK handle class >'

    def __str__(self):
        return '< KvK handle class >'

    # public methods

    def read(self):
        try: # try to read the file, if it exists
            with open(self.filePath, 'r') as fp:
                self.text = fp.read()
        except:
            raise Exception(f'Cannot read the file. \"{self.filePath}\" not existing yet.')

        res = [] # main array (return)

        # checks proper SOF
        if self.text[self.pos:self.pos + 2] == '<#':
            self.pos += 2

            while self.pos < len(self.text): # goest through the whole file
                if self.text[self.pos] == ' ' or self.text[self.pos] == '\t' or self.text[self.pos] == '\n':
                    self.pos += 1

                if self.text[self.pos:self.pos + 5] == 'class': # if a class starter is found
                    point = self.__getClass__() # class scanning
                    res.append(point) # adds class to main array

                if self.text[self.pos:len(self.text)] == '#>': # if EOF, stops scanning
                    break

            return res

    def get(self, element, className=None):
        self.pos = 0 # restarts counter for read
        dict = self.read() # reads the KvK file
        try:
            if className == None: # if class name is not specified, it looks for a class named as element variable
                for classCont in dict: # scans class containers
                    for classname in classCont: # scans class names
                        if classname == element: # if the class name equals to the wanted one
                            return classCont[classname] # returns the content of a class
            else: # looks for a specific attribtute in a specific class
                for classCont in dict:  # scans class containers
                    for classname in classCont: # scans class names
                        if classname == className: # if the class is the wanted one
                            for attr in classCont[classname]: # scans the attributes
                                if attr == element: # if the attribute is the wanted one
                                    return classCont[classname][attr] # returns the content of the attribute
        except:
            return None

    def write(self, content):
        toWrite = '' # content initialiser
        toWrite += '<#\n' # adds SOF

        for classCont in content: # for each class container
            for className in classCont: # takes the class name
                toWrite += f'    class "{className}" ::>\n' # writes the class name in the proper way
                for attr in classCont[className]: # scans the attributes and takes name
                    cont = (classCont[className])[attr] # takes attribute content
                    toWrite += f'        ({attr}) -> "{cont}"\n' # writes the whole attribute in the proper way
        toWrite += '#>' # adds EOF

        self.file.write(toWrite) # writes on the file

    def addClass(self, className):
        oldContent = self.content[0:len(self.content)-2] # takes out the EOF from content
        EOF = '#>' # variable containing EOF

        # puts in the content the old one, the new class, and the EOF
        self.content = oldContent + f'    class "{className}" ::>\n' + EOF

        # writes the new content in the file
        with open(str(self.filePath), 'w') as file:
            file.write(self.content)

    def addAttr(self, className, attrName, attrContent):
        try: # checks if the specified class exists
            index = self.content.index(f'class "{className}" ::>')
        except:
            raise Exception('Class not found')
        else:
            endIndex = (index + (len(f'class "{className}" ::>')))

            # makes new content
            self.content = self.content[0:endIndex] + f'\n        ({attrName}) -> "{attrContent}"' + \
                           self.content[endIndex:len(self.content)]

            # writes new content in the file
            with open(self.filePath, 'w') as file:
                file.write(self.content)

    def editClass(self, oldClassName, newClassName):
        try: # checks if the class exists
            startIndex = self.content.index(f'class "{oldClassName}" ::>') # takes the starting index of class declaration
        except:
            raise Exception('Class not found. You might want to use "addClass" method to add it.')
        else:
            endIndex = startIndex + len(f'class "{oldClassName}" ::>') # takes ending index of class declaration

            # puts all togeter
            self.content = self.content[0:startIndex] + f'class "{newClassName}" ::>' + self.content[endIndex:len(self.content)]

            # writes new content in the file
            with open(self.filePath, 'w') as file:
                file.write(self.content)

    def editAttr(self, className, oldAttrName, newAttrName, attrContent=None):
        try: # checks if the class exists
            classIndex = self.content.index('class \"' + className + '\" ::>')
        except:
            raise Exception('Class not found')
        else:
            preClass = self.content[0:classIndex]  # what's before the class
            tmp = self.content[classIndex + 5:len(self.content)]
            # temporary variable to check if there are other classes after the current one or EOF

            try: # sets the ending index of the class
                endClassIndex = tmp.index('class')
            except:
                endClassIndex = tmp.index('#>')

            isolatedClass = self.content[classIndex:endClassIndex + classIndex + len('class')]  # isolated class

            afterClass = tmp[endClassIndex:len(tmp)]  # what's after the class

            try: # checks if the attribute exists
                oldAttrIndex = isolatedClass.index(oldAttrName)
            except:
                raise Exception('Attribute not found')
            else:
                # edits attribite name
                isolatedClass = isolatedClass[0:oldAttrIndex] + \
                                newAttrName + isolatedClass[
                                  oldAttrIndex + len(oldAttrName):len(isolatedClass)]

                if (attrContent != None): # of the new attribute content is specified
                    virgStart = oldAttrIndex
                    while isolatedClass[virgStart] != '"': # scans until it finds the first "
                        virgStart += 1

                    virgEnd = virgStart + 1
                    while isolatedClass[virgEnd] != '"': # scans until it finds the second "
                        virgEnd += 1

                    # edits attribute content
                    isolatedClass = isolatedClass[0:virgStart + 1] + attrContent + \
                                    isolatedClass[virgEnd:len(isolatedClass)]

                # edits the content
                self.content = preClass + isolatedClass + afterClass

                # writes the new content in the file
                with open(self.filePath, 'w') as file:
                    file.write(self.content)

    def removeClass(self, className):
        try: # checks if the class exists
            classIndex = self.content.index('class \"' + className + '\" ::>')
        except:
            raise Exception('Class not found')
        else:
            tab = len('    ')
            preClass = self.content[0:classIndex - tab] # what's before the class

            # checks if there are other classes after the current one or EOF
            tmp = self.content[classIndex + 5:len(self.content)]
            try:
                endClassIndex = tmp.index('class')
            except:
                # if EOF, it writes on "afterClass" the EOF itself
                endClassIndex = tmp.index('#>')
                afterClass = '#>'
            else:
                afterClass = tmp[endClassIndex:len(tmp)] # takes what's after the current class

            self.content = preClass + afterClass # writes new content

            # writes the new content in the file
            with open(self.filePath, 'w') as file:
                file.write(self.content)

    def removeAttr(self, className, attrName):
        try:
            classIndex = self.content.index('class \"' + className + '\" ::>')
        except:  # se non trova la classe
            raise Exception('Class not found')
        else:  # se trova la classe
            preClass = self.content[0:classIndex]  # prima della classe
            tmp = self.content[classIndex + 5:len(self.content)]
            try:
                endClassIndex = tmp.index('class')
            except:
                endClassIndex = tmp.index('#>')
            isolatedClass = self.content[classIndex:endClassIndex + classIndex + 5] # isolated class
            afterClass = tmp[endClassIndex:len(tmp)]  # self.content[endClassIndex:len(self.content)] # dopo la classe
            try:
                attrIndex = isolatedClass.index(attrName)
            except:
                raise Exception('Attribute not found')
            else:
                # temporary variable containingthe isolate class. Removed the attribute name, not yet the content
                tmp = isolatedClass[0:attrIndex - 1] + isolatedClass[attrIndex + len(attrName):len(isolatedClass)]

                virgStart = attrIndex
                while tmp[virgStart] != '"': # scans until it finds the first "
                    virgStart += 1

                virgEnd = virgStart + 1
                while tmp[virgEnd] != '"': # scand until it finds the last "
                    virgEnd += 1

                # writes new isolatec lass
                isolatedClass = isolatedClass[0:attrIndex - 10] + isolatedClass[virgEnd+1:len(
                    isolatedClass)]

                # writes new content
                self.content = preClass + isolatedClass + afterClass

                # writes new content in the file
                with open(self.filePath, 'w') as file:
                    file.write(self.content)

    def isEmpty(self):
        content = self.content
        content = content.split('\n')

        i = 0
        for element in content:
            if element == '' or element == ' ':
                content.pop(i)
            i += 1
        try:
            if content[0] == '<#' and content[1] == '#>':
                return True
            return False
        except:
            if content == '':
                return True
            return False