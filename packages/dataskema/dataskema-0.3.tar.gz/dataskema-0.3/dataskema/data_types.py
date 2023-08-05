# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
from dataskema import lang


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

    @staticmethod
    def type(ptype: dict, ptyp2: dict) -> dict:
        ptype = dict(ptype)
        ptype.update(ptyp2)
        return ptype

    @staticmethod
    def mandatory(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'mandatory': True})

    @staticmethod
    def lower(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'lower'})

    @staticmethod
    def upper(ptype: dict) -> dict:
        return DataTypes.type(ptype, {'to': 'upper'})

    @staticmethod
    def default(ptype: dict, value: any) -> dict:
        return DataTypes.type(ptype, {'default': value})

    @staticmethod
    def label(ptype: dict, label: str) -> dict:
        return DataTypes.type(ptype, {'label': label})
