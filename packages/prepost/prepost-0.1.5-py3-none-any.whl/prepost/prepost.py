
class PreCond():



	####################################################################################
	@classmethod
	def minimum_not_null(cls, minimum_not_null_count ):
		assert( isinstance( minimum_not_null_count, int) )
		assert( minimum_not_null_count > 0 )

		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):

				count_not_null = 0
				for arg_item in args: 
					if arg_item: count_not_null += 1
				for arg_name in kwargs: 
					if kwargs[arg_name]: count_not_null += 1
				
				if count_not_null < minimum_not_null_count: raise Exception( f"At least {minimum_not_null_count} ## {count_not_null} ##{args} ##{kwargs}must be not null")
					
				return original_func(*args, **kwargs)
					
			return wrapper_func
		return main_decorator
	
	####################################################################################
	# Does {} have a [] of fields
	# @dict_has_fields( {'a':1, 'b':2, 'c':3} )
	@classmethod
	def dict_has_fields(cls, **dict_fields ):
		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):
				test_ok = True
				for dict_name in dict_fields.keys():
					if dict_name in kwargs:
						for expected_field in dict_fields[ dict_name ]:
							if not expected_field in kwargs[ dict_name ]:
								raise Exception(f"Error in args - could not find field {expected_field} in dictionary {dict_name}" )
				return original_func(*args, **kwargs)
			return wrapper_func
		return main_decorator

	####################################################################################
	@classmethod
	def equals(cls, **decorator_args ):
		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):

				test_ok = True
				for dec_arg_item in decorator_args:
					if dec_arg_item in kwargs:
						if kwargs[ dec_arg_item ] != decorator_args[ dec_arg_item ]:
							raise Exception(f"Error in args - for {dec_arg_item} expect [{decorator_args[ dec_arg_item ]}] input [{kwargs[ dec_arg_item ]}]" )
				return original_func(*args, **kwargs)
					
			return wrapper_func
		return main_decorator

	####################################################################################
	@classmethod
	def not_null(cls, decorator_args ):
		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):

				test_ok = True
				for dec_arg_item in decorator_args:
					if dec_arg_item in kwargs:
						if kwargs[ dec_arg_item ] == None and kwargs[ dec_arg_item ] == '' :
							raise Exception(f"Error in args - for {dec_arg_item} expect to be not empty" )
				
				return original_func(*args, **kwargs)
				
			return wrapper_func
		return main_decorator

class PostCond():
	####################################################################################
	@classmethod
	def not_null(cls ):
		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):
				ret_value = original_func(*args, **kwargs)
				if ret_value == None: raise Exception(f"Error in return value - expect not null" )
				return ret_value
			return wrapper_func
		return main_decorator