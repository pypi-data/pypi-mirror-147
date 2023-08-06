import pkg_resources  # part of setuptools
import typer
from ngn.config.config import *
from ngn.aws.data import *
from ngn.do.data import *
#from setup import version

'''
alpha expected behavior
costngn-cli (default company and account data)
costngn-cli config ->input account data
costngn-cli --show config -> show account/s data (without keys)
costngn-cli AWS ->aws default account data
costngn-cli DO  ->DO default account data
costngn-cli --help ->automatic

def main(): #it was for a test
    typer.echo("Hello from main")
    typer.run(hello)
'''

app = typer.Typer(help='* costngn-cli gives you access to cloud services data and costs')







def choose_acc(company):
    print("Reading configuration file") #config.toml
        
    config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Choose the first account found for this provider    
    have_acc=False
    for pro_nick in prof:
        #pp.pprint(prof[pro_nick]['provider'])
        if prof[pro_nick]['provider'].lower()==company:
            have_acc=True
            nick=pro_nick #acc=prof[nick] #pp.pprint(acc)                       
            print(company.upper(),'account found with nickname',nick)
            break
    if not have_acc:
        print(company.upper(),'account not found in profile')
        quit()
    return nick

def nick_ok(company,nick):
    print("Reading configuration file") #config.toml
    prof=toml.load(config_file)
    #Check if an account with that nickname exists and match the company    
    if nick in prof:
        print(f"Nickname {nick}",end=' ')
        if prof[nick]['provider']==company:
            print(f'is correct for an account on {company.upper()}')
            return
        else:
            print('does not match an account in',company.upper(),', it points to an account in', prof[nick]['provider'].upper())
            quit()
    else:
        print(f"There isn't any account with nickname {nick} in {config_file}")
        quit()

    
@app.callback(invoke_without_command=True)
def foo():
    version = pkg_resources.require("costngn-cli")[0].version
    typer.echo(f'Welcome to costngn-cli {version} (pre-alpha)')
    #typer.echo(f"{__app_name__} v{__version__}")
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','config.toml')
    global result_dir
    result_dir=os.path.join(Path.home(), 'costngn','results')
    #typer.echo(f"{lat}, {long}, {method}")

@app.command()
def config():
    """
    Input and store your account access information
    """
    #global config_file
    config_file=os.path.join(Path.home(), 'costngn','config.toml')
    typer.echo('Enter below your account access information:')
    typer.echo('It will be saved into config file')
    #typer.run(conf_main,config_file)
    conf_main(config_file)

@app.command()
def list_profiles():
    """
    Show your stored account/s access information
    """
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')
    typer.echo('Show config file contents:')
    #typer.run(conf_show(),config_file)
    conf_show(config_file)

@app.command()
def aws(nick:str,   
    cost: bool = typer.Option(False,
    '--cost', '-c',
    help="Show current real costs from Cost Explorer (it generates charges)"),
    ):

    """
    Gets AWS instances data - 'costngn-cli aws --help' for options
    """
    #global config_file
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')
    company='aws'
    #nick=choose_acc(company)
    typer.echo(f'Go to {company.upper()} data:')
    nick_ok(company, nick)
    #typer.run(aws_main)
    aws_main(company,nick,config_file,result_dir,cost)


@app.command()
def do(nick:str):

    """
    Gets Digital Ocean instances data \n 'costngn-cli aws --help' for options
    """
    #global config_file
    #config_file=os.path.join(Path.home(), 'costngn','config.toml') 
    company='do'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    typer.echo(f'Go to {company.upper()} data:')
    do_main(company, nick,config_file,result_dir)




@app.command()
def hello(name:str,nick:str): 

    """
    adding you name after 'hello' you'll be greeted
    """
    typer.echo(f"Hello {name} {nick} from costngn-cli !")


'''
def ngn():
    
    print('go to get')

    conf_get('Jack')

'''
if __name__ == "__main__":
    app()
    



