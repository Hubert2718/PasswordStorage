import blowfish
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
from getpass import getpass
import os, time

#Add path to xml file where you want to store your passwords
PATH = ""


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def encode_passwords(path, paswd):
    cipher = blowfish.Cipher(bytes(paswd, 'utf-8'))
    dictionary = {}
    with open(path, 'r') as f:
        data = f.read()
    xml = BeautifulSoup(data, "xml")
    for t in xml.find_all('credentials'):
        name = t.find('platform').string
        credentials = []
        login =  t.find('login').string
        password = t.find('password').string
        credentials.append(login.string)
        encoded = b"".join(cipher.encrypt_ecb_cts(bytes(password, 'utf-8')))
        credentials.append((str(encoded)))
        dictionary[name] = credentials
    return dictionary

def create_dictionary(path):
    dictionary = {}
    with open(path, 'r') as f:
        data = f.read()
    xml = BeautifulSoup(data, "xml")
    for t in xml.find_all('credentials'):
        name = t.find('platform').string
        credentials = []
        login =  t.find('login').string
        password = t.find('password').string
        credentials.append(login)
        credentials.append(password)
        dictionary[name] = credentials
    return dictionary

def create_xml(dict):
    data = ET.Element('Package')
    for key in dict:
        credentials = ET.SubElement(data, 'credentials')
        platform = ET.SubElement(credentials, 'platform')
        platform.text = key
        login = ET.SubElement(credentials, 'login')
        login.text = (dict[key])[0]
        passwd = ET.SubElement(credentials, 'password')
        passwd.text = (dict[key])[1]

    # writing xml
    b_xml = minidom.parseString(ET.tostring(data)).toprettyxml()
    with open(PATH, "w") as f:
        f.write(b_xml)

def decode_password(platform, paswd, path):
    dict = create_dictionary(path)
    cipher = blowfish.Cipher(bytes(paswd, 'utf-8'))
    decrypted = b"".join(cipher.decrypt_ecb_cts(eval((dict[platform])[1])))
    return ((dict[platform])[0], decrypted.decode())
    

def add_password():
    dict = create_dictionary(PATH)
    print("Platforms saved:")
    for key in dict:
        print(key)
    platform = input("enter the name of the platform for which you want to create/change a password\n$ ")
    if platform in dict:
        choice = input("A password for this platform already exists. Do you want to change them? (y - yes, n - no)\n$ ")
        if choice == 'y':
            password = input("Enter a new password for the platform: {} and username: {}.\n$ ".format(platform, (dict[platform])[0]))
            paswd = getpass("Enter a encoding password: \n$ ")
            cipher = blowfish.Cipher(bytes(paswd, 'utf-8'))
            encoded = b"".join(cipher.encrypt_ecb_cts(bytes(password, 'utf-8')))
            (dict[platform])[1] = str(encoded)
            create_xml(dict)
        elif choice == "n":
            print("Please prowide unique platform name")
        else:
            print("No such option as: " + choice)
    else:
        login = input("Enter a login\n$ ")
        password = input("Enter a new password\n$ ")
        cls()
        paswd = getpass("Enter a encoding password: \n$ ")
        cipher = blowfish.Cipher(bytes(paswd, 'utf-8'))
        encoded = b"".join(cipher.encrypt_ecb_cts(bytes(password, 'utf-8')))
        credentials = (login, str(encoded))
        dict[platform] = credentials
        create_xml(dict)

def show_password():
    dict = create_dictionary(PATH)
    print("Platforms saved:")
    for key in dict:
        print(key)
    platform = input("Enter the name of the platform for which you want to see the password\n$ ")
    if platform in dict:
        paswd = getpass("Enter a encoding password: \n$ ")
        (login, password) = decode_password(platform, paswd, PATH)
        print("LOGIN: {}".format(login))
        print("PASSWORD: {}".format(password))
        time.sleep(5)
        cls()
    else:
        print("I can't find the password for this platform")


while True:
    cls()
    print("1 - Add/Change password")
    print("2 - Show password")
    print("3 - Exit")
    choice = input("What you want to do?\n$ ")

    if choice == "1":
        add_password()
    elif choice == "2":
        show_password()
    else:
        exit()
