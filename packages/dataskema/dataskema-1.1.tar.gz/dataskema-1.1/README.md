# `dataskema`
Data schema validation for python

- Validate types, formats, sizings, lines, etc. of incoming parameters
- Customizable types for own aplications
- Customizable validation messages
- Multi-language support
- Easy to use, minimum code using decorators

## Content  index

1. [How to use dataskema](##How to use `dataskema`)
2. [Data types definition](##Data types definition)
3. [Default data types](##Default data types)
4. [Inline keyword override](##Inline keyword override)


## How to use `dataskema`

1) Define your own data schema using `dataskema` default data types (`mydatatypes.py`) or using your own data types:


    from dataskema.data_types import DataTypes

    class MyDataTypes(DataTypes):

        address = DataTypes.type(DataTypes.title, {
            'label': 'Address',
            'regexp': '^[a-zA-Z0-9\\.\\@\\+\\-\\_]+$',
        })
        phone_number = {
            'type': 'str',
            'max-size: 20,
            'regexp': '^[0-9\\-]+]+$',
        }
        ...

2) Import your data schema and use it with `dataskema` validation decorators. Look that t.name is inherited from default data types of DataTypes class.


    import dataskeme
    from mydatatypes import MyDataTypes as t


    @dataskeme.args(name=t.name, address=t.address, phone_number=t.phone_number)
    def print_contact_data(name: str, address: str, phone_numer: str):
        print(f"Name: {name}"
        print(f"Address: {address}"
        print(f"Phone number: {phone_number}"


    def service_edit_contact():
        name = 'Lorenzo'
        addresss = 'C/ Costa Rica, 32'
        phone_number = '999-845-321'
        try:
            print_contact_data(name, address, phone_number)
        except SchemaValidationResult as res:
            print(res.get_message())

3) In the above example, before printing contact data, it is validated with own data schema. The data are correct and no errors will be shown. But if we modify `mydatatypes.py` to force a validation error, then:  


    phone_number = {
        'type': 'str',
        'max-size: 20,
        'regexp': '^[0-9]+$',
    })
    ...

The error will be: 

    'phone_number' has an invalid format

4) We can specify label for this paramente to show a better message:  


    phone_number = {
        'type': 'str',
        'label': 'Phone number',
        'max-size: 20,
        'regexp': '^[0-9]+$',
    })
    ...

The error will be: 

    'Phone number' has an invalid format

4) We can specify our own format error message too:  


    phone_number = {
        'type': 'str',
        'label': 'Phone number',
        'max-size: 20,
        'regexp': '^[0-9]+$',
        'message': '{name} has an invalid phone number format' 
    })
    ...

The error will be: 

    'Phone number' has an invalid phone number format
    

5Other test: Empty `name` value and change `name` type as mandatory using inline type change. Look `t.mandatory` method in the decorator:


    @dataskeme.args(name=t.mandatory(t.name), address=t.address, phone_number=t.phone_number)
    def print_contact_data(name: str, address: str, phone_numer: str):
        ...

The error will be: 


    'name' is mandatory
    ...and 1 error more

6) Want you see all errors? Change `dataskeme.MAX_VALIDATION_MESSAGES = 10` to see the 10 first validation messages o `dataskeme.MAX_VALIDATION_MESSAGES = 0` to see all


    'name' is mandatory
    'Phone number' has an invalid phone number format

7) Now, 'name' is a field name it is not a known name. Then, use t.label() to assign a new label o modify your data scheme to assign a label to this type.   


    @dataskeme.args(name=t.label(t.mandatory(t.name), 'Contact name'), address=t.address, phone_number=t.phone_number)
    def print_contact_data(name: str, address: str, phone_numer: str):
        ...

or create data type directly in your data schema:

    name = DataTypes.type(DataTypes.name, {
        'label': 'Contact name',
        'required': True,
    })
    ...

    @dataskeme.args(name=t.name, 'Contact name'), address=t.address, phone_number=t.phone_number)
    def print_contact_data(name: str, address: str, phone_numer: str):
        ...


8) The error:


    'Contact name' is mandatory
    'Phone number' has an invalid phone number format

9) "Well, but I want to show errors in each field. Is this possible?" Yes, it is. Validation exception (`SchemaValidationResult`) has a method to return validation info by field: `get_result_of(field_name)`. This method returns this data structure:


    {
        'valid': <boolean to indicate if this field is valid or not>
        'message': <validation message. Only valid=False>
        'label': <label assigned to field if was defined. Only valid=False>
    }


The method `get_results()` returns all validation results in a dict whose keys are the field names. The method `get_message()` returns all validation messages. In own example, the returning would be:

    get_results():
    {
        'name': {
            'valid': False,
            'message': 'It is mandatory',
            'label': 'Contact name'
        },
        'address': {
            'valid': True
        },
        'phone_number': {
            'valid': False,
            'message': 'It has an invalid phone number format',
            'label': 'Phone number'
        },
    }

    get_message():
    "'Contact name' is mandator\n'Phone number' has an invalid phone number format",

10) `dataskema` supports Spanish and English messages. Use `dataskema.lang.DEFAULT = dataskema.lang.ES` to show Spanish language. 

11) "Fine, but solution that I search is for Flask endpoints and its incoming parameters". No problem, `dataskema` is the solution. For example, look that Flask endpoint. Look that `user_id` parameter passed as `argument` for the next method.


    @flask_app.route('/api/user/<user_id>', methods=['PUT'])
    def update_user(user_id: str):
        json_data = request.get_json()
        ...


12) This example not validate `user_id` neither `json_data`. Now, we will use our decorators and our data schema (`mydatatypes.py`). Look as `update_user` method includes the json params that we need us. This params are defined by above decorator `flask_json`. If the incoming params not validate then a `SchemaValidationResult` will be raised. Look how `user_id` is validated with `arg` decorator. 


    @flask_app.route('/api/user/<user_id>', methods=['PUT'])
    @dataskema.args(user_id=t.user_id)
    @dataskema.flask_json(name=t.name, address.t.address, phone_number=t.phone_number)
    def update_user(user_id: str, name: str, address: str, phone_number: str):
        ...

13) "But, What happes if my GET method not contains JSON data because the data is in the query string?" Easy. Use `flask_query` decorator in the same way.


    @flask_app.route('/api/user/<user_id>', methods=['GET'])
    @dataskema.args(user_id=t.user_id)
    @dataskema.flask_query(name=t.name, address.t.address, phone_number=t.phone_number)
    def update_user(user_id: str, name: str, address: str, phone_number: str):
        ...

14) "And now, how catch the decorator exception to process validation result?" Use your own decorator (for example, `@my_json_result`) to catch this result and response with JSON data as this example is shown:


    @flask_app.route('/api/user/<user_id>', methods=['PUT'])
    @my_json_result()
    @dataskema.args(user_id=t.user_id)
    @dataskema.flask_json(name=t.name, address.t.address, phone_number=t.phone_number)
    def update_user(user_id: str, name: str, address: str, phone_number: str):
        ...

The code of `@my_json_result` could be something as this:


    def my_json_result():
        def inner_function(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except SchemaValidationResult as ve:
                    return {
                      'result': 'ERR',
                      'reason': ve.get_message(),
                      'errors': ve.get_results()
                    }
            return wrapper
        return inner_function

15) "All of this is bored for me. I hate decorators". Well, if you want to use the code for validate parameters in the traditional way, look this examples:


    @flask_app.route('/api/user/<user_id>', methods=['PUT'])
    def update_user(user_id: str):
        try:
            args_validator = Args()
            args_validator.validate(user_id=t.user_id)
            json_validator = JSON()
            json_validator.validate(name=t.name, address.t.address, phone_number=t.phone_number)
            return {result: 'OK'}
        raise SchemaValidatorResult as ex:
            error_msg = ex.get_message()
            errors = ex.get_result()
            return {result: 'ERR', reason: error_msg, errors: errors}
            
        
## Data types definition
You will define a struct data with some of that keywords. 

### All types
That keywords are for all types:

#### `'type': <keyword>`
Type of data. Possible types are: `'int'`, `'float'`, `'str'`, `'bool'`, `'list'`, `'dict'`, `'any'`.

If the data value cannot cast with the defined type then a format error message will be raised. This default message could be overriden using the `message` keyword. By default, the type will be `str`. If `default` keyword is defined, the default value type will be the type of this default value especified.

#### `'default': <any>`
Default value for the data when it is not passed.

#### `'mandatory': <bool>`
The data must be mandatory. If `type=str` the data will be empty if only had blank characters.

#### `'message': <str> or <dict>`
Override the default message for format errors. You can to use `{name}` to specify the data name. If you want to specify some languages, you can use a dict with the keys EN or ES for english or spanish languages respectively.    

#### `'label': <str>`
By default, the data name is the incoming paramenter name. You can overwrite using this keyword for better understanding.


### For `'type': 'str'`
Keywords only for type specified as `'str'` are:

#### `'white-list': [...]`
list of valid values for the data

#### `'icase': <bool>`
ignore case for matching the `white-list` 

#### `'regexp': <str>`
Regular expression to match de data value. The default format error message could be overriden using the `message` keyword.

#### `'min-size': <int>`
Limit the minimum number of characters for the data.  

#### `'max-size': <int>`
Limit the maximum number of characters for the data.  

#### `'max-lines': <int>`
Limit the maximum number of lines for the data.  

#### `'to': <keywords>`
Tranformation string functions. Several functions can be applied separating them by commas.
Possible values are:
- `'upper'`: Convert string to uppercase.
- `'lower'`: Convert string to lowercase.
- `'no-trim'`: No trim the string. By default, all strings are trimmed by both sides. 
- `'trim'`: Force trim (by default)


### For `'type': 'int' or 'float'`
Keywords only for type specified as `'int' or 'float'` are:

#### `'min-value': <int>`
Limit the minimum value for the data.  

#### `'max-value': <int>`
Limit the maximum value for the data.  


### For `'type': 'list'`
Keywords only for type specified as `'list'` are:

#### `'schema': <dict>`
Schema of data for list items. This data schema must be validated for each item list. The schema format
is the same of this schema and use the same keyword and constraints.


### For `'type': 'bool', 'dict' or 'any'`
That types have no specific keywords:


## Default data types 
That are the default data types defined by `dataskema` by the class `DataTypes` in `data_types.py` file. It's very illustrative as an example:


    class DataTypes:
    
        generic = {
            'type': 'any',
        }
        boolean = {
            'type': 'bool',
            'message': {
                lang.EN: "{name} must be a boolean",
                lang.ES: "{name} debe ser un booleano",
            }
        }
        integer = {
            'type': 'int',
            'message': {
                lang.EN: "{name} must be an integer number",
                lang.ES: "{name} debe ser un número entero",
            }
        }
        positive = {
            'type': 'int',
            'min-value': 1,
            'message': {
                lang.EN: "{name} must be an integer positive number",
                lang.ES: "{name} debe ser un número entero positivo",
            }
        }
        negative = {
            'type': 'int',
            'max-value': -1,
            'message': {
                lang.EN: "{name} must be an integer negative number",
                lang.ES: "{name} debe ser un número entero nagativo",
            }
        }
        zero_positive = {
            'type': 'int',
            'min-value': 0,
            'message': {
                lang.EN: "{name} must be an integer number or zero",
                lang.ES: "{name} debe ser un número entero positivo o cero",
            }
        }
        zero_negative = {
            'type': 'int',
            'max-value': 0,
            'message': {
                lang.EN: "{name} must be an integer negative number or zero",
                lang.ES: "{name} debe ser un número entero negativo o cero",
            }
        }
        decimal = {
            'type': 'float',
            'message': {
                lang.EN: "{name} must be a valid decimal number",
                lang.ES: "{name} debe ser un número decimal válido",
            }
        }
        hexadecimal = {
            'regexp': '^[A-Fa-f0-9]+$',
            'message': {
                lang.EN: "{name} must be a valid hexadecimal number",
                lang.ES: "{name} debe ser un número hexadecimal válido",
            }
        }
        alfanumeric = {
            'regexp': '^[A-Za-z0-9]+$',
            'message': {
                lang.EN: "{name} must be a alphanumeric string",
                lang.ES: "{name} debe ser una cadena alfanumérica",
            }
        }
        short_id = {
            'max-size': 20,
        }
        long_id = {
            'max-size': 40,
        }
        short_name = {
            'max-size': 50,
        }
        name = {
            'max-size': 100,
        }
        title = {
            'max-size': 200,
        }
        summary = {
            'max-size': 2000,
        }
        text = {
            'max-size': 500000,
            'max-lines': 10000,
        }
        version = {
            'regexp': '^[a-zA-Z0-9\\.\\-\\+]+$',
            'message': {
                lang.EN: "{name} must have a valid version format",
                lang.ES: "{name} debe tener un formato de versión válido",
            }
        }
        search = {
            'max-size': 50,
        }
        email = {
            'regexp': '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
            'max-size': 100,
            'message': {
                lang.EN: "{name} must have a valid e-mail format",
                lang.ES: "{name} debe tener un formato de e-mail válido",
            }
        }
        url = {
            'regexp': '^((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))(%[0-9A-Fa-f]{2}|[-()_.!~*\';/?:@&'
                      '=+$,A-Za-z0-9])+)([).!\';/?:,][[:blank:|:blank:]])?$',
            'max-size': 500,
            'message': {
                lang.EN: "{name} must have a valid URL format",
                lang.ES: "{name} debe tener un formato de URL válida",
            }
        }
        password = {
            'regexp': '^[a-zA-Z0-9_+&*\\$\\-\\(\\)]+$',
            'max-size': 50,
            'min-size': 8,
            'message': {
                lang.EN: "{name} must have a valid password (only alphanumeric chars and _, +, &, *, -, (, ) or $ symbols)",
                lang.ES: "{name} debe tener un formato de password válida (sólo caracters alfanuméricos y los símbolos _, +, &, *, -, (, ) o $",
            }
        }
            

## Inline keyword override  
The class `DataTypes` define some static methods to ease include keyword in a type without modify the type in particular cases. That methods are:
- `label(type, label)`: include a label for the type
- `default(type, default_value)`: include a default value for the type
- `upper(type)`: force incoming value to be uppercase
- `lower(type)`: force incoming value to be lowercase
- `mandatory(type)`: the value must be mandatory
- `type(type, newtype)`: One way to redefine inline a complex type. Useful for define our own data types using `DataTypes` class

Examples:

Importing `dataskema.data_types.DataTypes as t`:

`t.name` is not a mandatory type but `t.mandatory(t.name)`, yes

`t.name` name by default will be 'name' but `t.label(t.name,'Contact')` will be named 'Contact' 


For define own our types in a custom class:

    from dataskema.data_types import DataTypes as t

    class MyDataTypes(t):
    
        contact = t.mandatory(t.label(t.name, 'Contact'))
        contact_email = t.label(t.email, 'Contact e-mail')
        address = t.label(t.title, 'Address')
        postal_code = t.type(t.numeric, {
            label: 'Postal code'
            mandatory: true,
            min-size: 5,
            max-size: 5,
        })
        ...













