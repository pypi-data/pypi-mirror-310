
from pathlib import Path

from stupidgen.processor import ProcessingError, ConfigError
from stupidgen.stringprocessing import string_interpolation
from stupidgen.basichandlers import BasicSetup, CodeSetup

class CppSetup(CodeSetup) : 
	
	file_type = "C++"
	file_extensions = ("cpp", "cxx", "c++", "hpp", "hxx", "h++")
			
	def handle_text_line(self, line) :
		return self.proc.outer_indent + "std::cout << " + " << ".join(string_interpolation((line))) + ";\n"
		
	@staticmethod
	def execute(file_name, args) : 
		exec_name = Path(file_name).with_suffix("")
		CodeSetup.execute_command("Compile " + repr(file_name), ["g++", "-o", exec_name, file_name])
		CodeSetup.execute_command("Run " + str(exec_name), [exec_name.resolve(), *args])

class GroovySetup(CodeSetup) : 
	
	file_type = "groovy"
	file_extensions = ("groovy", "gvy", "gy", "gsh")
			
	def handle_text_line(self, line) :
		return self.proc.outer_indent + "println(\"\" + " + " + ".join(string_interpolation((line[:-1]))) + ");\n"
		
	@staticmethod
	def execute(file_name, args) : 
		CodeSetup.execute_command("Run " + str(file_name), ["groovy", file_name, *args])

class JavaSetup(CodeSetup) : 
	
	file_type = "java"
	file_extensions = ("java",)
			
	def handle_text_line(self, line) :
		return self.proc.outer_indent + "System.out.println(\"\" + " + " + ".join(string_interpolation((line[:-1]))) + ");\n"
		
	@staticmethod
	def execute(file_name, args) : 
		CodeSetup.execute_command("Run " + str(file_name), ["java", file_name, *args])
		
class JavascriptSetup(CodeSetup) : 
	
	file_type = "javascript"
	file_extensions = ("js", "mjs")
			
	def handle_text_line(self, line) :
		return self.proc.outer_indent + "console.log(\"\" + " + " + ".join(string_interpolation((line[:-1]))) + ");\n"
		
	@staticmethod
	def execute(file_name, args) : 
		CodeSetup.execute_command("Run " + str(file_name), ["node", file_name, *args])

class MetaSetup(BasicSetup) : 
	
	file_type = "meta"
	file_extensions = ("meta",)
	
	def __init__(self, proc, options) : 
		self.proc = proc
		self.proc.out_file = options.out_file
		proc.set_block_handler(options.code_symbol, self.meta_block_handler(proc))		
		proc.set_line_handler(options.code_symbol, lambda l : l)

	def meta_block_handler(self, proc) : 
		def handler(block) :
			exec("".join(block), { "proc" : proc })
			return None
		return handler

class PythonSetup(CodeSetup) : 
	
	file_type = "python"
	file_extensions = ("py",)
		
	def handle_text_line(self, line) :
		#Note: removing trainling \n.
		return self.proc.outer_indent + "print(" + " + ".join(
			string_interpolation(line[:-1], 
				string_delimiters=("\"", "'", "\"\"\""), 
				code_map = lambda c : "str( " + c + ")" )) + ")\n"
			
	@staticmethod
	def execute(file_name, args) : 
		CodeSetup.execute_command("Run " + str(file_name), ["python", file_name, *args])
		
		
class LuaSetup(CodeSetup) : 
	
	file_type = "lua"
	file_extensions = ("lua",)
		
	def handle_text_line(self, line) : 
		return self.proc.outer_indent + "print(" + " .. ".join(string_interpolation(line[:-1])) + ")\n";

	@staticmethod
	def execute(file_name, args) : 
		CodeSetup.execute_command("Run " + str(file_name), ["lua", file_name, *args])