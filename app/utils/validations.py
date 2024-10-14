from app.config.common import re


def emailValidation(mail):
    patternEmail = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patternEmail, mail)

def telValidation(tel):
    patterTel = r'^\d{1,10}$'
    return re.match(patterTel, tel)

def userValdiation(user):
    patterUser = r'^[a-zA-Z0-9_-]{3,16}$'
    return re.match(patterUser, user)

def nameValidation(name):
    patternName = r'^[a-zA-Z\s]{3,}(?:\s[a-zA-Z]+)*$'
    return re.match(patternName, name)

def spaceValidation(value):
    patternSpace = r'^[a-zA-Z0-9_-]+(\s[a-zA-Z0-9_-]+)*\S$'
    return re.match(patternSpace,value)

def validar_digitosDecimales(value):
    patron_digitos = r'^\d{1,4}(\.\d{1,2})?$'
    return re.match(patron_digitos, value)

def docValidation(value):
    patterDoc = r'^\d{7,10}$'
    return re.match(patterDoc, value)

def passwordValidation(value):
    patternPassword = r'^\d{4}$'
    return re.match(patternPassword, value)