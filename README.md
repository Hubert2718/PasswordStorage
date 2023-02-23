# PasswordStorage
A simple program for storing passwords. Passwords are encrypted using the Blowfish cipher and stored in this form together with logins in an XML file.
To display the decrypted password, the user must enter the password with which it was encrypted. The user can add new passwords and edit existing ones.

To run the program correctly, copy the passwordEncoded.xml file and assign the path to it to the **PATH** variable.
The values for **<platform>, <login> and <password>** provided in the file are examples and can be deleted.

To use the program effectively, you need to create an alias or function that will allow you to quickly call it from the terminal level.
Example in PowerShell using functions.
1. Open the **$Profile** file
2. Add the lines below:
```
  function PasswordStorage {
      python PATH
  }
 ```
Where PATH is the path to your **.py** file.
3. Restart ps and enter the PasswordStorage command.
