import typer
import os
from os.path import exists
from pathlib import Path
import copy
import pprint as pp
from ngn.config.base_dict import *
import toml

def conf_aws(config_file):
    print('Amazon Web Services API account configuration') 
    prof=toml.load(config_file)
    #pp.pprint(prof) #print(profile)
    nick= input('Enter nickname for a new account:') 
    # check if account nickname already exists, else create and append
    if nick in prof:print('That account nickname already exists')
    else:
        print(f'A new account config record named {nick} will be added to the profile')
        acc= copy.deepcopy(account)
        acc['provider']= 'aws'
        acc['ACCESS_KEY']= input('Enter or paste access key:')
        acc['SECRET_KEY']= input('Enter or paste secret key:')        
        acc['AUTH_REGION']= 'us-east-2'    
        #pp.pprint(acc)
        #fi1=os.environ['USERPROFILE']+'\costngn-cli\pru01.toml'        
        print('Save profile to:',config_file)
        prof[nick]=acc
        with open(config_file, "w") as f:
                toml.dump(prof, f)

def conf_do(config_file):
    print('Digital Ocean account configuration')
    prof=toml.load(config_file)
    #pp.pprint(prof) #print(profile)
    nick= input('Enter nickname for a new account:') 
    # check if account nickname already exists, else create and append
    if nick in prof:print('That account nickname already exists')
    else:
        print(f'A new account config record named {nick} will be added to the profile')
        acc= copy.deepcopy(account)
        acc['provider']= 'do'
        #acc['ACCESS_KEY']= input('Enter or paste access key:')
        acc['SECRET_KEY']= input('Enter or paste secret key:')        
        acc['AUTH_REGION']= 'us-east-2' #don't know yet   
        #pp.pprint(acc)      
        print('Save profile to:',config_file)
        prof[nick]=acc
        with open(config_file, "w") as f:
                toml.dump(prof, f)


def conf_main(some_a:str):
    #print('passing for conf_post',some_a)
    #Create .costngn folder if does not exist on home directory
    #costngn_path= str(Path.home())+'\.costngn' #not platform independent
    costngn_path=os.path.join(Path.home(), '.costngn')
    if os.path.exists(costngn_path): print('Folder already exists')
    else: 
        print('Making new folder',costngn_path)
        os.makedirs(costngn_path)

    #Check ir config file exista on .costngn folder, else create
    #config_file=costngn_path+'\config.toml' #not platform independent
    config_file=os.path.join(costngn_path,'config.toml')
    if exists(config_file): print('Config file already exists')
    else: #
        print('Creating config file',config_file)
        prof=copy.deepcopy(profile)
        fi1= config_file        
        with open(fi1, "w") as f:
            toml.dump(prof, f)
    #Ask which provider is the new account for
    provider=input('Enter company ID (AWS/DO/...):')
        
    if provider.lower() not in providers:
        print(provider,'is not valid')
        print('valid inputs are:',providers)
    else:
        print('Going to', provider.upper(),'account configuration')
    if provider.lower()=='aws':conf_aws(config_file)
    elif provider.lower()=='do':conf_do(config_file)

    #Call

  
 


def conf_show(nick): #(don't need company)
    #print(nick)   
    #open config file (in CLI\config folder)
    acc={}
    acc=toml.load("config.toml")
    #pp.pprint(acc)
    print(f"Account Nickname: {acc['nick']}")
    print(f"Service Provider: {acc['provider']}")
    print(f"Data Output Format: {acc['out_format']}")
    print(f"Access Key: XXX HIDDEN XXX")
    print(f"Secret Key: XXX HIDDEN XXX")
    print('')
    
    #if account (nickname) exists
        #extract profile to a dictio     
        #print(profile)
    #else
        #error message'not found' like
    #print something and exit

'''
# call function
if __name__ == "__main__":
    conf_post()
    #conf_get('MJ01')

'''