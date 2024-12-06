import importlib

def call_function(module_name: str, function_name: str, function_params: str) -> any:
    """
    Dynamically call a function from a module with specified parameters.

    Args:
        module_name (str): The name of the module.
        function_name (str): The name of the function.
        function_params (str): The parameters to pass to the function, as a string.

    Returns:
        any: The result of the function call.
    """
    try:
        # Dynamically import the module
        module = importlib.import_module(module_name)
        
        # Get the function from the module
        func = getattr(module, function_name)
        
        # strip the parameters string of any whitespace
        function_params = function_params.strip()
        
        if len(function_params) > 0:
            # create a list of each parameter
            function_params = function_params.split(",") 
            
            # for each item on the parameter list, if it is non numerical, add quotes
            for i, param in enumerate(function_params):
                if not param.isnumeric():
                    function_params[i] = f"'{param.strip()}'"
                    
            # join the list of parameters into a string
            function_params = f'({",".join(function_params)},)'
            
            # Convert the function parameters from string to a tuple
            params = eval(function_params)
        else:
            params = ()
        
        # Call the function with the parameters and return the result
        result = func(*params)
        return result
    except Exception as e:
        return f"Error: {e}"

def hello_world(name: str) -> str:
    """
    Return a greeting message.

    Args:
        name (str): The name to include in the greeting.

    Returns:
        str: The greeting message.
    """
    return f"Hello, {name}!"

def hello_world_noparam() -> str:
    """
    Return a greeting message.

    Returns:
        str: The greeting message.
    """
    return "Hello World!"

# Example usage
if __name__ == "__main__":
    module_name = "math"
    function_name = "pow"
    function_params = "(2, 3)"  # Parameters as a string
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: 8.0

    # Example usage of hello_world function
    module_name = "util_functions"
    function_name = "hello_world"
    function_params = "('World',)"  # Parameters as a string
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: Hello, World!

    # Example usage of hello_world_noparam function
    module_name = "util_functions"
    function_name = "hello_world_noparam"
    function_params = "()"  # No parameters
    result = call_function(module_name, function_name, function_params)
    print(result)  # Output: Hello World!