__version__ = '0.1.9'

import re
import pyperclip as pc
from chilitools.utilities.backoffice import backofficeURLInput
from chilitools.api.connector import ChiliConnector
from chilitools.api.mycp import generateLoginTokenForURL, generateOAuthTokenFromCredentials, setUserType
from chilitools.utilities.defaults import STAFF_TYPE

def getConnector():
    url = backofficeURLInput()
    return ChiliConnector(backofficeURL=url)

def menu():
  clipboard = True
  while (True):

    print("\nCHILI Publish Testing Tools")
    print("--------------------------\n")
    print("1) Generate Login Token for BackOffice URL")
    print("2) Get API Key for BackOffice URL")
    print("3) Generate Login Token for ft-nostress")
    print("4) Generate Login Token for ft-nostress-sandbox")
    print("5) Set/Change login credentials")
    print("6) Toggle copy to clipboard")

    option = input()

    if option == 'staff':
      print('Succesfully enabled 2FA staff login for BackOffice')
      setUserType(userType=STAFF_TYPE)
      continue
    elif option == "exit":
      break

    if re.search("[0-7]", option):
      option = int(option)
      print('')

      match option:
        case 1:
          chili = getConnector()
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          if clipboard: pc.copy(token)
          print(token)
        case 2:
          chili = getConnector()
          key = chili.getAPIKey()
          pc.copy(key)
          print(key)
        case 3:
          chili = ChiliConnector(backofficeURL='https://ft-nostress.chili-publish.online/ft-nostress/interface.aspx')
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          if clipboard: pc.copy(token)
          print(token)
        case 4:
          chili = ChiliConnector(backofficeURL='https://ft-nostress.chili-publish-sandbox.online/ft-nostress/interface.aspx')
          token = generateLoginTokenForURL(backofficeURL=chili.backofficeURL)
          if clipboard: pc.copy(token)
          print(token)
        case 5:
          print(generateOAuthTokenFromCredentials())
        case 6:
          clipboard = not clipboard

    else:
      print("That is not a valid option, please try again")

