# `dataskema`
Data schema validation for python

- Validate types, formats, sizings, lines, etc. of incoming parameters
- Customizable types for own aplications
- Customizable validation messages
- Multi-language support
- Easy to use, minimum code using decorators

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

- `'type'`: type of data: `'int'`, `'float'`, `'str'`, `'bool'`, `'list'`, `'dict'`, `'any'`. It would be a type that could be casting to python type without raise an exception. 

- `mandatory`: the data must be mandatory

For `'type'`: `'str'`

- `'white-list'`: [...]
list of valid values for the data

- `'icase'`: <bool>
ignore case for matching the `white-list` 






