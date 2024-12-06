
import json

from .processor import ProcessingError

def string_lit_escape(subline) : 
	"""
	Escapes the string passed as input and adds double quotes at the beginning and the end. 
	This is done using json.dumps method, and the resulting string should be valid for any programming language which accept at least 
	as much as json.
	
	Argument:
	------------
	subline : str
		the string that needs escaping.
	"""
	return json.dumps(subline)
	
def find_one_of(input_string, pattern_list, start = 0) : 
	"""
	Tries to find the first position which matches any one of the strings in the pattern list. Returns a pair composed of the string 
	matched and its position in the input string. If no string from the pattern list is in the input, returns the pair (None, -1)
	
	Arguments:
	------------
	input_string : str	
		The string on which we are trying to find patterns
	pattern_list : List[str]
		The list of patterns we are trying to find in the input string
	start : int 
		The position of the input string where we start the search
		
	Returns
	------------
	A pair (str, int) composed of the matched string and its index in the input string, or (None, -1) if no pattern was found
	in the input string.
	"""
	if len(set(pattern_list)) != len(pattern_list) : 
		raise RuntimeError("Argument pattern_list contains repeated values: " + repr(pattern_list))
	
	if start > 0 : 
		res = find_one_of(input_string[start:], pattern_list)
		if res[0] is None : 
			return res
		else :
			return (res[0], res[1] + start)
	
	found_pos = -1 
	found_pattern = None
	for pattern in pattern_list : 
		index = input_string.find(pattern)
		if index == -1 : 
			continue
		if found_pos == -1 : 
			found_pos = index 
			found_pattern = pattern 
			continue 
		if index > found_pos : 
			continue 
		if index < found_pos : 
			found_pos = index 
			found_pattern = pattern 
			continue 
		#At this point index == found_pos
		#We keep the longest matching pattern
		#The two patterns cannot have the same length otherwise they would be equal.
		if len(found_pattern) < len(pattern) : 
			found_pos = index 
			found_pattern = pattern 
			
	return (found_pattern, found_pos)	
	
def is_character_escaped(line, character_pos) :
	"""
	Indicate if the character at position character_pos is escaped or not (by counting the number of '\'
	appearing before it
	"""
	pos = character_pos - 1
	while pos >=0 and line[pos] == '\\' :
		pos -= 1
	return ((character_pos - pos) % 2) == 0
	
def string_interpolation(line, start_symbol = "{%", end_symbol = "%}", code_map = None, string_map = None, string_delimiters = ("\"")) :
	"""
	Interpolates the provided string such that everything that is between 'start_symbol' and 'end_symbol' is treated as code, and the
	rest is treated as raw string.
	Nesting of the start_symbol end_symbol pairs is not supported, and will raise a ProcessingError, unless they are inside a string literals (that can start or end with any of the string_delimiters given as argument).
	
	All the code_fragments will be passed to the code_map function, while all the raw string fragments are passed to string_map.
	The function returns a list with the results of these two functions.
	
	Arguments:
	----------------
	line : str
		the string that we wish to interpolate
	start_symbol : str
		the string which marks the beginning of a code fragment (Default : "{%")
	end_symbol : str 
		the string which marks the end of a code fragment (Default : "%}"
	code_map : str -> str
		the function which is called on every code fragment. By default it returns the its input enclosed in parentheses.
	string_map : str -> str
		the function which is called on every raw string fragment. By default it escapes its input with string_lit_escape
	string_delimiters : Tuple[str]
		the list of symbols which can be used to start or end a string litteral.
	""" 
	if code_map is None : 
		code_map = lambda s : "(" + s + ")"
	if string_map is None : 
		string_map = string_lit_escape
	
	result = list()
	i = line.find(start_symbol)
	while i != -1 :
		if i > 0 : 
			sub = line[:i]
			if sub.find(start_symbol) != -1 : 
				raise ProcessingError("Nesting of escape symbols " + start_symbol + "  " + end_symbol + " is not supported")
			result.append(string_map(sub))
			
		j = line.find(end_symbol)
		
		if j == -1 : 
			raise ProcessingError("Missing closing symbol " + repr(end_symbol))
		if j < i : 
			raise ProcessingError("Unexpected closing symbol " + repr(end_symbol))
		
		#Check if the closing symbol we found is inside a string literal or not.
		(string_start, string_start_pos) = find_one_of(line, string_delimiters, i + len(start_symbol))
		while (string_start != None) and (string_start_pos < j) :
			#We found a string literal starting before j, try to see where it ends.
			end_delim = line.find(string_start, string_start_pos + len(string_start))
			# TODO : look at the number of \ to check wether the symbol is escaped.
			while end_delim != -1 and is_character_escaped(line, end_delim): 
				#The end delimiter we found is escaped. Try to find the next one
				end_delim = line.find(string_start, end_delim + 1)
			if end_delim == -1 : 
				raise ProcessingError("Unclosed string literal : " + repr(string_start))
			if end_delim < j : 
				#The string literal ends before j, try to find the next one.
				(string_start, string_start_pos) = find_one_of(line, string_delimiters, start = end_delim + len(string_start))
			else : 
				#The end_symbol we found is inside a string literal, try to find the next one;
				j = line.find(end_symbol, end_delim + len(string_start))
				if j == -1 : 
					raise ProcessingError("Missing closing symbol " + repr(end_symbol))
					(string_start, string_start_pos) = find_one_of(line, string_delimiters, start = end_delim + len(string_start))
			
		code_sub = line[(i + len(start_symbol)):j]
		result.append(code_map(code_sub))
		line = line[(j + len(end_symbol)):]
		i = line.find(start_symbol)
	if line.find(end_symbol) != -1 : 
		raise ProcessingError("Unexpected additional closing symbol " + repr(end_symbol))
	result.append(string_map(line))
	return result
