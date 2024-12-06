import argparse
import sys
import inspect
import stupidgen.languages
from .processor import StupidProcessor, ProcessingError
from .basichandlers import BasicSetup

def main():
	supported_languages = dict()
	supported_extensions = dict()

	# Use introspection to find all the classes defined in language.py, and register them as supported languages.
	for obj in stupidgen.languages.__dict__.values() :
		if inspect.isclass(obj) and issubclass(obj, BasicSetup) and obj.file_type != None :
			supported_languages[obj.file_type] = obj
			for ext in obj.file_extensions : 
				supported_extensions[ext] = obj.file_type

	argparser = argparse.ArgumentParser(prog = "stupidgen", description = 'A very simple tool for text files generation.')
	argparser.add_argument('--code-symbol', metavar = "<symbol>", help = 'The stating symbol used for lines of code.' 
		+ ' Defaults usually \'.\', but depends on the language.')
	argparser.add_argument('--string-symbol', metavar = "<symbol>", help = 'The stating symbol used for string lines.' 
		+ ' Defaults usually \'>\', but depends on the language')

	default_action = argparser.add_mutually_exclusive_group()

	default_action.add_argument('--default-code', '-C', action = 'store_true', help = "Lines without an expected starting symbol are treated as code lines")
	default_action.add_argument('--default-text', '-T', action = 'store_true', help = "Lines without an expected starting symbol are treated as text lines")
	default_action.add_argument('--default-drop', '-D', action = 'store_true', help = 'Drop lines which start with an unexpected symbol')

	output_group = argparser.add_mutually_exclusive_group()	
	output_group.add_argument('--output', '-o', metavar = '<path>', help = "Path to the file where the result is stored. By default, the output file is named like the input file, but without .multi extension.")
	output_group.add_argument('--print', action = "store_true", help = "Prints the result to standard output")

	argparser.add_argument('--language', metavar = "<lang>", help = 'The language used as control flow in the generated file. Supports one of ' 
		+ ", ".join(supported_languages.keys()) + ".", choices = supported_languages.keys())

	argparser.add_argument('--run', action = 'store_true', help = 'Directly run the generated file.')
	argparser.add_argument('file', help = 'The file to process')

	argparser.add_argument('--version', action = 'version', version = stupidgen.__version__)
	#Note: argparse.REMAINDER is not documented, but this is the best I could come up with to make sure
	#that arguments coming after --run-args are not treated as optional arguments, and wrong arguments would not be mistaken as
	#positional arguments.
	argparser.add_argument('--run-args', nargs=argparse.REMAINDER, help = 'Additional arguments passed to the script if --run is specified')

	args = argparser.parse_args()
	if len(args.run_args) > 0 : 
		if not args.run: 
			print("Additional argument are only valid when the --run option is specified", file = sys.stderr)
		
	if args.output is None and not args.print : 
		#No output specified. If the input is a .multi file, we strip the extension and write to this file.
		if args.file.endswith(".multi") : 
			args.output = args.file[:-6]
		else : 
			if args.run and args.language is not None: 
				#Just pick one extension compatible with the language, and write to a.<extension>
				if args.language in supported_languages : 
					args.output = "a." + supported_languages[args.language].file_extensions[0]
				else : 
					print("Unknown language ", repr(args.language), file = sys.stderr)
					print("Expected one of " + str(supported_languages.keys()), file = sys.stderr)
					sys.exit(1)
			else :
				print("Input does not have the .multi extension, so the output could not be determined.", file = sys.stderr)
				print("Use one of the --print or --output <file> options to indicate where to store the result.", file = sys.stderr)
				sys.exit(1)
				
	if args.print and args.run : 
		print("--print and --run options cannot be specified at the same time", file = sys.stderr)
		sys.exit(1)
		
	if args.language is None : 
		#Detect the language from either the extension of the output file (.py, .cpp...) or the extension of the 
		#input file (.py.multi, .cpp.multi...)
		if args.print : 
			split_name = args.file.split(".")
			if len(split_name) >= 2 and split_name[-2] in supported_extensions :
				args.language = supported_extensions[split_name[-2]]
			else : 
				print("Could not detect the language to use from file extensions. Please specify the --language option.", file = sys.stderr)
				sys.exit(1)
		else : 
			#args.output is not None 
			extension = args.output.split(".")[-1]
			if extension in supported_extensions : 
				args.language = supported_extensions[extension] 
			else : 
				print("Unknown file extension: " + repr("." + extension) + ". please specify the --language option.")
			
	if args.code_symbol is None : 
		args.code_symbol = "." if args.language != "meta" else "~"
	if args.string_symbol is None : 
		args.string_symbol = ">"

	try : 
		if args.output is None : 
			args.out_file = sys.stdout
		else : 
			args.out_file = open(args.output, "w")
			
		with open(args.file) as f : 
			proc = StupidProcessor()
			if args.language in supported_languages : 
				supported_languages[args.language](proc, args)
			else :
				print("Unknown language ", repr(args.language), file = sys.stderr)
				print("Expected one of " + str(supported_languages.keys()), file = sys.stderr)
				sys.exit(1)
			try :
				proc.process(f)
			except ProcessingError as e:
				print(e, file=sys.stderr)
				sys.exit(1)
	except Exception as e :
		import traceback
		traceback.print_exception(*sys.exc_info())
		sys.exit(1)

	finally : 
		if args.output is not None : 
			args.out_file.close()

	if args.run : 
		try : 
			supported_languages[args.language].execute(args.output, args.run_args)
		except NotImplementedError as e : 
			print("--run option is not supported for language " + repr(args.language), file = sys.stderr)

if __name__ == "__main__" : 
	main()