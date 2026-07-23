from pathlib import Path 
import json
import random
import string 
class Bank :
    database = "database.json"
    data =[]
    try :
       if Path(database).exists():
          with open (database,'r') as fs:
            data= json.loads(fs.read())
    except Exception as error :
       print(f"An error occured as {error} try again ")
    @classmethod
    def __update(cls):
       with open (cls.database,'w') as fs :
          fs.write(json.dumps(cls.data))
    @staticmethod
    def __Generate_accountno():
       chr = random.choices(string.ascii_uppercase,k=4)
       digits=random.choices(string.digits,k=8)
       acc=chr+digits
       final="".join(acc)
       return final 

    def create_account (self):
        
        info = { 
            "name" : input("Enter  your name :- "),
            "age" : int(input("Enter the age ")),
            "mail" :input("enter the  your mail :- "),
            "balance" :  0 ,
            "account no. " : Bank.__Generate_accountno(),
            "number" : int(input("enter  your number "))
            
                        
        }
        try:
            while True :
           
                
                pin = int(input("Enter your 4 digit pin "))
                if len (str (pin)) != 4:
                 print("your pin must be 4 digit try again ")
                else:
                   info['pin']=pin
                   break
        except Exception as valueError :
            print("you can only have numbers try again ")

        if info ['age']<18:
           print("you are  a minor ")
           return
        else : 
           Bank.data.append(info)
           Bank.__update()
    def deposite_money(self):
       acc_no=input("tell your account number :- ")
       pin= int(input ("tell your pin :- "))
       user=[i for i in Bank.data if i['pin']==pin and i ['account no. '] == acc_no]
       if user :
         money=int(input("Enter the depositing money :- "))
         if money > 100000 or money <= 0:
               print("you cannot deposit more than 100000 rs or less than 0 rs ")
         else:
            user[0]['balance'] += money 
            print("Money added successfully Thanks visit again 😒 ")
            Bank.__update()
       else : 
          print ("Invalid account no. or pin")


           
    def withdraw_money(self):
         acc_no=input("tell your account number :- ")
         pin= int(input ("tell your pin :- "))
         user=[i for i in Bank.data if i['pin']==pin and i ['account no. '] == acc_no  ]
         if user :
            money=int(input("Enter the  withdrwal money :- "))
            if  user[0]['balance'] < money :
                  
               print(" Insufficient balance    ")
            else:
               user[0]['balance'] -= money 
               print("Money debited successfuly 😒 ")
               Bank.__update()
         else : 
            print ("Invalid account no. or pin")
    def check_details (self):
            acc_no=input("tell your account number :- ")
            pin= int(input ("tell your pin :- "))
            user=[i for i in Bank.data if i['pin']==pin and i ['account no. '] == acc_no  ]
            if user :
               print("your details  are : \n ")
               for i in user [0]:
                  if i !="pin":
                     print(f"{i} : {user[0][i]}")
            else :
               print("Invalid account no. or pin ")
    def update_details(self):
      acc_no=input("tell your account number :- ")
      pin= int(input ("tell your pin :- "))
      user=[i for i in Bank.data if i['pin']==pin and i ['account no. '] == acc_no  ]
      if user == False :
         print("invalid number or pin ")
      else:
         newdata = {
            "name":input("Enter to skip or type your new name "),
            "mail":input("Enter to skip or type your new mail "),
            "number":input("Enter to skip or type your new number "),
            "pin":input("Enter to skip or type your new pin  ")
            
         }
         if newdata['name']=="":
            newdata['name']=user[0]['name']
         if newdata['mail']=="":
            newdata['mail']=user[0]['mail']
         if newdata['number']=="":
            newdata['number']=str(user[0]['number'])
         if newdata['pin']=="":
            newdata['pin']=str(user[0]['pin'])
         newdata['pin']=int(newdata['pin'])
         newdata['number']=int(newdata['number'])

      for i in user[0]:
         if i in newdata:
            user[0][i]=newdata[i]
      Bank.__update()
    def delete_user(self):
      acc_no=input("tell your account number :- ")
      pin= int(input ("tell your pin :- "))
      user=[i for i in Bank.data if i['pin']==pin and i ['accountno.'] ==acc_no  ]
      if user == False :
         print("invalid acc no.  or pin number ")
      else:

         print("are you sure press y/n")
         check =input("press (Y) or (N)")
         if check == 'y' or check=='Y':
            index=Bank.data.index(user)
            Bank.data.pop(index)
            Bank.__update()
         else:
            print("OK")



       
       



       
                  

           


Bank=Bank()
print(" Press 1 for create an Account ")
print("Press 2 for depositing  money ")
print("Press 3 for withdral  money ")
print("Press 4 for checking balance  ")
print("Press 5 for updating some details ")
print("Press 6 for deactivate  your Account ")
print("Press 0  to exit  ")



check = int (input(" tell your response :- "))

if check==1:
   Bank.create_account()
if check == 2:
   Bank.deposite_money()
if check == 3: 
   Bank.withdraw_money() 
if check == 4 :
   Bank.check_details ()
if check==5 :
   Bank.update_details()
if check ==6 :
   Bank.delete_user()




   






















#  list compreshon