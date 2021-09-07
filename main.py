
import requests, json, os, getpass
#color
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
white = '\033[37m'
def duco_logo():
    print(yellow +'''                                        
      ,,,,,,,,,,,,,,,,,,,               
      ,,,,,,,,,,,,,,,,,,,,,,,,          
      ,,,,,,,,,,,,,,,,,,,,,,,,,,,       
      ,,,,,,,,,,,,,        ,,,,,,,,     
      ,,,,,,,,,,,,,,,,,      .,,,,,,    
                  ,,,,,,       ,,,,,,   
                    ,,,,,      ,,,,,,   
                    ,,,,,      .,,,,,   
                    ,,,,,      ,,,,,,   
      ,,,,,,,,,,,,,,,,,,      .,,,,,,   
      ,,,,,,,,,,,,,,,,       ,,,,,,,    
                           ,,,,,,,      
      ,,,,,,,,,,,,,,,,,,,,,,,,,,        
      ,,,,,,,,,,,,,,,,,,,,,,,.          
                                        
''')
def duco_text():
    print('''
██████╗ ██╗   ██╗ ██████╗ ██████╗      ██████╗██╗     ██╗
██╔══██╗██║   ██║██╔════╝██╔═══██╗    ██╔════╝██║     ██║
██║  ██║██║   ██║██║     ██║   ██║    ██║     ██║     ██║
██║  ██║██║   ██║██║     ██║   ██║    ██║     ██║     ██║
██████╔╝╚██████╔╝╚██████╗╚██████╔╝    ╚██████╗███████╗██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝      ╚═════╝╚══════╝╚═╝
                                                         ''')
def main():
    if os.name == 'nt':
        clear = 'cls'
    else:
        clear = 'clear'
    os.system(clear)
    duco_text()
    user = input('Username: ')
    passwd = getpass.getpass('Password: ')
    
    #auth 
    auth = 'https://server.duinocoin.com/auth/{}?password={}'.format(user, passwd)
    auth = requests.get(auth)
    auth = json.loads(auth.text)
    auth = auth['success']

    #color
    #os check os


    os.system(clear)
    if auth == True:
        verify = 'https://server.duinocoin.com/users/{}'.format(user)
        verify = requests.get(verify)
        verify = json.loads(verify.text)
        verify = verify['result']['balance']['verified']

        if verify == 'yes':
            verify = '\033[32m Yes \033[37m'
        elif verify == 'no':
            verify = '\033[31m No \033[37m'
        duco_logo()
        duco_text()
        print(red + 'https://github.com/Karibura-Cyber/DUCO-Wallet-CLI\n')
        print(yellow + 'Welcome, {} \033[37m [Verified {}]'.format(user, verify))
        print(green + '\nAuthentication successful!\n' + white)
        print('-'*54)
        print('''Command: \n
            /balance                #For check your Balance
            /tranfer                #For tranfer DUCO Coin
            /transactions or /ts    #For check your transaction
            /miners                 #For show all RIG
            /exit or /q             #For Exit\n''') 
        print('-'*54)
        
        while True:
            command = input('{}@duinocoin.com > '.format(user))
            if command == '/exit' or command == '/q':
                exit()
            elif command == '/help' or command == '/h':
                print('\n')
                print('-'*54)
                print('''Command: \n
            /balance                #For check your Balance
            /tranfer                #For tranfer DUCO Coin
            /transactions or /ts    #For check your transaction
            /miners                 #For show all RIG
            /exit or /q             #For Exit\n''')
                print('-'*54)            
                print('\n')
            elif command == '/miners':
                miners = requests.get('https://server.duinocoin.com/miners/{}'.format(user))
                miners = json.loads(miners.text)    
                miners = miners['result']  
                print('\n')
                print('-'*100)
                for i in range(len(miners)):
                    print(miners[i]["identifier"],'\t','|','\t',miners[i]["algorithm"],'\t','|','\t' , miners[i]["software"],'\t','|','\t' ,int(miners[i]["hashrate"]) / 1000,'KH/s')
                print('-'*100)
                print('\n')
            elif command == '/balance':
                balance = requests.get('https://server.duinocoin.com/users/{}'.format(user))
                balance = json.loads(balance.text)
                balance = balance['result']['balance']['balance']
                print(green + '\nYour Balance: {}\n'.format(balance) + white)
            elif command == '/tranfer':
                if verify == '\033[32m Yes \033[37m':
                    recipient = input('Recipient: ')
                    amount = input('Amount: ')
                    memo = input('Memo: ')
                    tranfer = 'https://server.duinocoin.com/transaction?username={}&password={}&recipient={}&amount={}&memo={}'.format(user, passwd, recipient, amount, memo)
                    tranfer = requests.get(tranfer)
                    tranfer = json.loads(tranfer.text)
                    #{"result":"OK,Successfully transferred funds,a6de9fa8adc07f75","success":true} ||>>s success API response
                    tranfer = tranfer['success']
                    if tranfer == True:
                        print(green + '\nTransfer Successful! please for 10 minute then check your Wallet\n' + white)
                    else:
                        print(red + '\nTransfer Failed! Please check Input data\n' + white)
                else:
                    print(red + '\nYou need to verify your account first!' + white)
                    print(green + 'https://server.duinocoin.com/verify.html\n' + white)
            elif command == '/transactions' or command == '/ts':
                transactions = requests.get('https://server.duinocoin.com/users/{}'.format(user))
                transactions = json.loads(transactions.text)
                transactions = transactions['result']['transactions']
                print('\nTransactions \n')
                print('{:>15}'.format('Sender'),'{:>25}'.format('Recipient'),'{:>23}'.format('Amount'),'{:>25}'.format('Date&Time'))
                for i in range(len(transactions)):
                    sender = transactions[i]['sender']
                    amount = transactions[i]['amount']
                    recipient = transactions[i]['recipient']
                    memo = transactions[i]['memo']
                    datetime = transactions[i]['datetime']

                    if transactions[i]['sender'] == '{}'.format(user):
                        c = red
                    else:
                        c = green                
                    print(c,'|','{:<20}'.format(sender),'|','|','{:<20}'.format(recipient),'|','|','{:<20}'.format(amount),'|','|','{:<20}'.format(datetime),'|', white)
                print('\n')
                

    else:
        print(red + '\nAuthentication failed!\n' + white)
        print(red + 'Please check your username and password.\n' + white)
        exit()


 
main()

    
