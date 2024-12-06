import abc
import re
import subprocess
import sys

from .processor import ProcessingError

def drop_line() : 
	"""
	Returns a handler which simply drops the line it is passed.
	"""
	def handler(l) : 
		return None
	return handler
	
def print_line() : 
	"""
	Returns a handler which just prints the line unmodified.
	"""
	def handler(l) : 
		return l
	return handler
	
def join_lines(*, start = "", end = "", sep = "", drop_newline = False) : 
	"""
	Returns a block handler which concatenates together all the lines of a block using the provided separator. A prefix and 
	a suffix can be added to the resulting output by setting the start and end arguments appropriately.
	
	Arguments:
	----------------
	start : str
		String which is prepended to the result (Default: "")
	end : str
		String which is appended to the result (Default: "")
	sep : str
		String used to concatenante all the lines
	drow_newline : bool
		Whether the newline at the end of each line should be dropped or not before the concatenation (Default : False)
	"""
	
	def handler(block) :
		if drop_newline : 
			return start + sep.join((l[0:] if l[-1] != '\n' else l[0:-1]) for l in block) + end
		else : 
			return start + sep.join(l[0:] for l in block) + end
	return handler

class BasicSetup : 
	"""
	Basic class to setup the line processor for a specific language.
	
	Attributes:
	------------------
	file_type : str
		the name of the language supported by this class. This setup will be called if the --language
		argument passed corresponds to this value.
	file_extensions : List[str]
		list of file extensions that this class can handle by default. This setup will be called if no --language
		was specfied, and the file extension is in the list provided by this object.
	"""
	
	file_type = None
	file_extensions = tuple()
	

class CodeSetup(BasicSetup) : 
	"""
	Class to setup a Stupidprocessor based on the arguments passed to the command lines.
	Different languages can subclass this class and override the handle_code_line and handle_text_line 
	methods to provide an easy way to implement all the possible options command line arguments provided 
	by the tool.
	
	Attributes:
	------------
	proc : StupidProcessor 
		the object handling the processing of the lines
	"""
	
	def __init__(self, proc, options) : 
		self.proc = proc
		if self.proc.has_line_handler(options.code_symbol) : 
			raise ConfigError("Several languages registered for the symbol: " + repr(options.code_symbol)) 
		#Don't allow whitespace before the start symbol for code lines
		self.proc.set_line_handler(options.code_symbol, self.handle_code_line, False) 
		if self.proc.has_line_handler(options.string_symbol) : 
			raise ConfigError("Several languages registered for the symbol: " + repr(options.string_symbol)) 
		#Allow whitespace before the start symbol for text lines
		self.proc.set_line_handler(options.string_symbol, self.handle_text_line, True)
		
		if options.default_code : 
			self.proc.default_symbol = options.code_symbol
		elif options.default_text : 
			self.proc.default_symbol = options.string_symbol
			
		self.proc.out_file = options.out_file

		
	def handle_code_line(self, l) : 
		"""
		Handler for 'code' lines.
		Default implem returns the line unmodified
		"""
		return l
		
	def handle_text_line(self, l) : 
		"""
		Handler for 'text' lines.
		Default implem returns the line unmodified.
		"""
		return l
	
	@staticmethod 
	def execute_command(action, command) : 
		"""
		Executes the given command (provided as a list which is forwarded to subprocess.run).
		Exits the program if the command fails.
		
		Arguments
		-----
		action : str
			A name for the action we are trying to do
		command : list[str]
			The command to execute
		"""
		res = subprocess.run(command)
		if res.returncode != 0 : 
			print("Failed to " + action, file = sys.stderr)
			sys.exit(1)
	
	@staticmethod
	def execute(file_name) : 
		"""
		Directly run the file after it was generated.
		The default implementation just throws an error.
		"""
		raise NotImplementedError()
	
	
