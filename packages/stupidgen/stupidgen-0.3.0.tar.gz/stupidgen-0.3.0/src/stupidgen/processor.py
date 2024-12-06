import sys
import re

class ProcessingError(Exception) : 
	"""
	Error thrown when the input does not have the expected format.
	Handler can omit the line_numer and file_name. These informations are set by the 
	Processor.
	
	Attributes:
	------------
	message : str 
		the message associated with this error
	line_number : int 
		line where the error occurs
	file_name : str 
		name of the file where the error occurs
	"""
	
	def __init__(self, message, line_number = 0, file_name = None) : 
		super().__init__(message)
		self.message = message
		self.line_number = line_number;
		self.file_name = file_name
		
	def __str__(self) : 
		"""
		Prints the error message, the file where the error occured and the line where it occured.
		"""
		return super().__str__() + " in file " + repr(self.file_name) + " at line " + str(self.line_number)
		
class ConfigError(Exception) : 
	"""
	Error thrown when the configuration of the processor is incorrect.
	"""
	
	def __init__(self, message) : 
		super().__init__(message)
	
class StupidProcessor : 
	"""
	Class handling the processing of the file. It is charge of reading each line of the file, passing the line to 
	the corresponding registered handler, grouping the lines by block, and finally printing the result provided 
	by the handlers.
	
	Two types of handlers can be registerd on the processor: 
		- Line handler, called for every new line of the type they are registered for, 
		- Block handler, called at the end of every block of lines 
	
	Attributes:
	------------
	_line_handlers : dict
		Gives the line handler associated to each starting symbol
	_allow_outer_indent : dict
		Indicates for each symbol if we allow whitespace before the symbol
	_block_handlers : dict
		Gives the block handler associated to each starting symbol
	current_symbol : str
		The symbol of the last processed line
	line_number : int
		The number of the currently processed line
	drop_empty : bool 
		Whether empty lines should be dropped or not
	outer_indent : str 
		The amount of space that appears before the first non-whitespace symbol in the line
	"""
	
	def __init__(self) : 
		self._line_handlers = dict() #the line handlers for each symbol
		self._allow_outer_indent = dict()
		self._block_handlers = dict() #the block handlers for each symbol
		self.current_symbol = None #the symbol from the previous line, or None if no line was read yet
		self.current_block = list() #the previous lines from the current block (lines with the same starting symbol)
		self.line_number = 0 #line number of the current line
		self.drop_empty = False
		self.default_symbol = None
		self.out_file = sys.stdout
		self.outer_indent = ""
	
	def process(self, f) :
		"""
		Processes the file f by passing the lines one by one to the relevant handlers.
		
		Arguments
		----------
		f : file
			the file which needs to be processed
		"""
		if self.default_symbol is not None and self.default_symbol not in self._line_handlers : 
			raise ConfigError("No handler setup for the default symbol " +  repr(self.default_symbol))
		
		self.line_number = 0
		for line in f : 
			self.line_number += 1
			self.outer_indent = re.match(r"\s*", line).group()
			
			start_symbol = line[len(self.outer_indent)] if len(line) > len(self.outer_indent) else None
			
			if start_symbol != self.current_symbol and self.current_symbol != None : 
				#Ending a block
				self._finalize_current_block()
				
			if start_symbol in self._line_handlers and (self._allow_outer_indent[start_symbol] or len(self.outer_indent) == 0): 
				line = line[len(self.outer_indent) + 1:]
			else :
				start_symbol = self.default_symbol
				self.outer_indent = ""
			
			self.current_symbol = start_symbol
			if start_symbol is None : 
				if len(line) == 0 : 
					raise ProcessingError("Empty line with no default behaviour", self.line_number, f.name)
				else :
					raise ProcessingError("Unexpected starting symbol " + repr(line[0]), self.line_number, f.name)
			
			
			try :
				processed_line = self._line_handlers[start_symbol](line)
			except ProcessingError as e : 
				e.line_number = self.line_number
				e.file_name = f.name
				raise e
			if processed_line != None : 
				self.current_block.append(processed_line)
		self._finalize_current_block()
		
		self.current_symbol = None
		self.current_block = list()
		self.line_number = 0
		
	@staticmethod
	def default_block_handler(b) : 
		"""
		Default block handler, returns the input block unmodified.
		"""
		return b
			
				
	def _finalize_current_block(self) :
		"""
		Called when the current block is finished. Pass it to the corresponding block handler, and then print the result
		to the standard output.
		""" 
		finished_block = self._block_handlers.get(self.current_symbol, StupidProcessor.default_block_handler)(self.current_block)
		if finished_block is not None : 
			self._write_block(finished_block)
		self.current_block = list()
		
	def _write_block(self, block) :
		"""
		Writes the given block to the standard output
		
		Argument
		------------
		block : list(str) | str
			the block to print to standard output
		"""
		if isinstance(block, str) : 
			print(block, end = "", file = self.out_file)
		else : 
			print("".join(block), end = "", file = self.out_file)
	
	def set_line_handler(self, symbol, line_handler, allow_ws = False) : 
		"""
		Sets the line handler for the provided symbol. If there was already a line handler for this symbol, it is 
		replaced by the one passed as argument.
		
		Arguments
		-------------
		symbol : str
			A string of lenght 1 representing the starting line symbol that this handler is registered for.
		handler : str -> str
			The handler which returns what should be printed for this line for the given input line. If handler is None
			the current handler for this symbol is removed.
		allow_ws : bool 
			Indicates if we allow whitespace to the left of the symbol
		"""
		assert(len(symbol) == 1)
		if line_handler is None : 
			del self._line_handlers[symbol]
			del self._allow_outer_indent[symbol]
		else : 
			self._line_handlers[symbol] = line_handler
			self._allow_outer_indent[symbol] = allow_ws
			
		
	def set_block_handler(self, symbol, block_handler) : 
		"""
		Sets the block handler for the provided symbol. If there was already a block handler for this symbol, it is 
		replaced by the one passed as argument.
		
		Arguments
		-------------
		symbol : str
			A string of lenght 1 representing the starting line symbol that this handler is registered for.
		handler : list(str) -> list(str) | str
			The handler which returns what should be printed for this block for the given input block. If handler is None
			the current handler for this symbol is removed.
		"""
		assert(len(symbol) == 1)
		if (block_handler is None) : 
			del self._block_handlers[symbol]
		else : 
			self._block_handlers[symbol] = block_handler
			
	def has_line_handler(self, symbol) : 
		"""
		Indicates if there is aready a line handler registered for the given symbol
		
		Arguments
		-----------
		symbol : str
			A string of lenght 1 reprensenting the line symbol for which we want to check if a line handler is registered.
		"""
		return symbol in self._line_handlers
		
	def has_block_handler(self, symbol) : 
		"""
		Indicates if there is aready a block handler registered for the given symbol
		
		Arguments
		-----------
		symbol : str
			A string of lenght 1 reprensenting the line symbol for which we want to check if a block handler is registered.
		"""
		return symbol in self._block_handlers
