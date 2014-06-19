"""UniquePits by Dennis Coufal <dennis.coufal@gmail.com>

Assigns one car to one (unique) pit and one (unique) garage. 
Ideal for leagues, since everyone needs their own pit.

You just have to add enough pit spots in DevMode and
this script will take care of the rest.

Excess pits and garage spots will be removed to avoid confusion.
"""

import re
import sys, os

class Position:	
	def __init__(self, pos, orientation):
		self.pos=pos
		self.orientation=orientation
		
	def get_pos(self):
		return self.pos
		
	def get_orientation(self):
		return self.orientation
		
class AIW_Parser():
	def __init__(self, fname):
		self.lines = [line.strip() for line in open(fname)]

	#divides AIW in 3 sections: pit related section, pre pit section
	#and post pit section
	def get_sections(self):
		pitList	= []
		pre_pit_section = []
		post_pit_section = []
		ret=[]
		pitSectionReached=0
		pitSectionOver=0
		for line in self.lines:
			if(line.lower() == "[pits]"):
				pitSectionReached=1
			if(pitSectionReached and line.lower() == ""): #end of section
				pitSectionOver=1
			
			if(pitSectionReached and not pitSectionOver):
				pitList.append(line)
				
			elif(not pitSectionReached):
				pre_pit_section.append(line)
			elif(pitSectionOver):
				post_pit_section.append(line)
		
		ret.append(pre_pit_section)
		ret.append(pitList)
		ret.append(post_pit_section)
		return ret
		
class UniquePits():
	def __init__(self, fname, fname_output):
		sections=AIW_Parser(fname).get_sections()
		self.pre_pit_section=sections.pop(0)
		self.pit_section=sections.pop(0)
		self.post_pit_section=sections.pop(0)
		self.fname=fname
		self.fname_output=fname_output		
		#self.fname_output=fname.replace(".AIW", "_new.AIW").replace(".aiw", "_new.AIW")
		self.pits=[]
		self.garages=[]
		self.print_start_msg()
		
	def print_start_msg(self):
		version="1.0"
		print("rFactor2 Unique Pits v{} by Dennis Coufal\n".format(version))
	
	#approximation of an empty position automatically created by DevMode
	def is_empty_position(self, str):
		return not re.match("GarPos\=\([0-9]{0,3},[-]{0,1}0\.000,[-]{0,1}[0-9]\.[0-9]{3},[-]{0,1}[0-9]\.[0-9]{3}\)", str)

	#parse AIW section related to pits/garages and write positions to of pits/garages to arrays
	def parse_pit_section(self):
		for x in range(0,len(self.pit_section)):
			#is pit information
			if(self.pit_section[x].startswith("PitPos")):
				self.pits.append( Position(self.pit_section[x], self.pit_section[x+1]) )
				
			#is garage information
			if(self.pit_section[x].startswith("GarPos") and self.is_empty_position(self.pit_section[x])):
				self.garages.append( Position(self.pit_section[x].replace("(1", "(0").replace("(2", "(0"), self.pit_section[x+1].replace("(1", "(0").replace("(2", "(0")) )
				
		print( "pits: {}, garages: {}".format(len(self.pits), len(self.garages)) )
		
		#remove excess pits and garages (actual removal happens when file is written)
		if(len(self.pits) < len(self.garages)):
			print( "Removing some garages, since there are not enough pits." )
			print( "New garage count: {}".format(len(self.pits)) )
			
	def run(self):		
		self.parse_pit_section()
		self.write_sections_to_file()
		
	# write the processed data to file
	def write_sections_to_file(self):
		f = open(self.fname_output,'w')	
		
		#pre pit section
		for line in self.pre_pit_section:
			if( re.match("garagespots\=[0-9]{0,3}", line) ):
				f.write( "garagespots=1\n")
			elif( re.match("pitspots\=[0-9]{0,3}", line) ):
				f.write( "pitspots={}\n".format(len(self.pits)))
			else:
				f.write( line+"\n")
				
		#position section
		f.write( "[PITS]\n")
		for x in range(0,len(self.pits)):
			if(x<len(self.garages)):
				f.write( "TeamIndex={}\n".format(x))
				f.write(self.pits[x].get_pos()+"\n")
				f.write(self.pits[x].get_orientation()+"\n")
				f.write(self.garages[x].get_pos()+"\n")
				f.write(self.garages[x].get_orientation()+"\n")
				
		#post pit section
		for line in self.post_pit_section:
			f.write( line+"\n")
			
		f.close()		
		print("Success! file written: {}".format(self.fname_output))

def main():
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		print("ERROR: Wrong number of arguments!\nUsage: {} FILENAME.AIW".format(os.path.basename(sys.argv[0])))
		sys.exit()
	
	if "-h" in sys.argv or "--help" in sys.argv:
		print("Usage: {} track.AIW \t//(will overwrite the input)".format(os.path.basename(sys.argv[0])))
		print("\n(optional) Provide an output file: {} track.AIW Output.AIW".format(os.path.basename(sys.argv[0])))
		sys.exit()
		
	output_file=sys.argv[1] if(len(sys.argv)<3) else sys.argv[2]		

	UniquePits( sys.argv[1], output_file ).run()
if  __name__ =='__main__':main()
	

