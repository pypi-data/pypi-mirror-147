import re

class PreCond():

	####################################################################################
	# Field matches RE pattern
	# example: @matches_pattern( field = '[a-zA-Z]+' )
	@classmethod
	def matches_pattern(cls, **dict_fields ):
		def main_decorator(original_func):
			def wrapper_func(*args, **kwargs):
				test_ok = True
				for target_field in dict_fields.keys():
					if target_field in kwargs:
						# breakpoint()
						if not re.match( dict_fields[target_field], kwargs[target_field]):
							Exception( f"Field [{target_field}] with value [{kwargs[target_field]}] does no pattern [{dict_fields[dict_fields]}]")
					else:
						raise Exception( f"Field [{target_field}] not passed in as a KWarg (keyword argument - e.g. func(arg1='abc')")
				return original_func(*args, **kwargs)
			return wrapper_func
		return main_decorator



	####################################################################################
	# Ensure that minimum number of fields are not null
	# example: @minimum_not_null( 1) => at least one field must not be null
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
	# example: @dict_has_fields( ['a', 'b'] )
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
	# Make sure that the field has a specific value
	# @equals( a= 'apple')
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