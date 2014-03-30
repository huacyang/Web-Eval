##############################################################################
# CustomClass Rules                                                          #
# =================                                                          #
#                                                                            #
#1. All custom classes must inherit sreb.EBObject and the constructor        #
#   must call sreb.EBObject's constructor. If a class starts with _ then it  #
#   is considered internal and will not be treated as a custom class.        #
#                                                                            #
#2. The custom class will only use the default constructor.                  #  
#   ie. a constructor with no parameters.                                    #
#                                                                            #
#3. To add a property provide getter and have an attribute that does not     #
#   starts with an underscore(_) or an upper case letter, and have the       #
#   attribute of a know type. Known types are int,float,str,EBPoint,EBColor, #
#   tuple, and list.                                                         #
#   If an attribute's default value is of type tuple and only has two        #
#   items, the property will be treated as an EBPoint. Similarly, if an      #
#   attribute's default value is a tuple of 3 items the property will be     #
#   treated as an EBColor.  The input type of the setter and the output type #
#   of the getter is expected to be the same as the type of the attribute.   #
#                                                                            #
#4. If only getter is provided, the property will be a readonly property.    # 
#                                                                            #
#6. The custom class may be instanciated during development to obtain        # 
#   class info. Avoid such things as display mode change, remote connections # 
#   in the constructor.                                                      #
#                                                                            # 
#7. Any method in the custom class can be called using the Execute action    #
#   By default, the return type of the method is string unless a doc string  #
#   with the following constraint is available                               #
#	a. The doc string starts with "RETURN:" (case matters)               #
#       b. Following the text "RETURN:" provide a default value of the type  #
#          or the __repr__ value of the class. eg. str for string            #
#8. If a property's setter metthod has default values for it's parameters,   #
#    the property will not accept references or equation.                    #
##############################################################################


import sreb




class CustomClassTemplate(sreb.EBObject):
	def __init__(self):
		sreb.EBObject.__init__(self)
		self.hotspotsPosition = list();	# List used to store the clickable area for a page.
		self.hotspotsImages = list();		# List used to store the next page to be displayed corresponding to the click area.
	
	
	# Method used to check the validity of the datasource
	def checkDataValidity(self, trialData):
		'''RETURN: 0'''
		
		if len(trialData) < 1:
			print "No valid trial is included!"
			return 0;
		else:
			# Compile the whole list of pages;
			pageList = list();
			for line in trialData:
				if len(line) != 3: 
					print "incomplete data!";
					return 0;
				else:
					pageList.append(line[0])
			
				#Check the length of the clickable area and the lens of the linked pages.
				if len(line[1]) != len(line[2]):
					print "check the content of the datasource"
					print "the number of clickable areas does not match the linked pages!"
					return 0;
			
			# For each page corresponds to the clickable area;
			# check whetrher the target page exists at all.
			for line in trialData:
				for page in line[2]:
					if pageList.index(page) < 0:
						print "error in line: ", trialData.index(line)
						print "data: ", line
						print "page ", page, " does not exist!"
						return 0
				
		return 1;
		
		
	# Method used to read in the trial data for the current page.		
	def buildHotspots(self, trialData, currentPage):
		'''RETURN: 0'''
		
		self.hotspotsPosition = list();	# List used to store the clickable area for a page.
		self.hotspotsImages = list();		# List used to store the next page to be displayed corresponding to the click area.
			
		if len(trialData) > currentPage:
			if len(trialData[currentPage]) > 2:
				self.hotspotsPosition = trialData[currentPage][1]
				self.hotspotsImages = trialData[currentPage][2]
				return 1;
			else:
				print "error: the current trial data is incomplete - missing clickable area or next page info"
				return 0;
		else:
			print "error: the current trial index exceeds the maximum of possible trials"
			return 0;
		
		
		
	# Method used to check whether the mouse is currently on top of one of the clickable area.
	def checkCurrentMousePosition(self, x, y):
		'''RETURN: 0'''
		
		current_position = -1;
		temp = 0 ;
		for position in self.hotspotsPosition:
			if x>=position[0] and x<position[2] and y>=position[1] and y<position[3]:
				current_position = temp;
			temp += 1;
				 
		return current_position;
		

	def processMouseClick(self, trialData, x, y):
		'''RETURN: abc'''
		current_position = self.checkCurrentMousePosition(x, y)
		
		if current_position == -1:
			return -1;
		else:
			page_index = 999;
			
			# Get the image that links to the next hotspots.
			nextImage = self.hotspotsImages[current_position]
			
			# Find out the index of the current hotspot;
			for trial in trialData:
				if  nextImage == trial[0]:
					page_index = trialData.index(trial)

			# Gives a warning if an invalid page is pointed to.
			if page_index == 999:
				print "an invalid page is linked to ",  nextImage
			
			return page_index;
			
			
			
			
		
		
