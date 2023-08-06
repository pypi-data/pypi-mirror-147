import typer
from ngn.config.config import *
from ngn.aws.data import *
from ngn.do.data import *

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
    config_file=os.path.join(Path.home(), '.costngn','config.toml')    
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


@app.command()
def config():
    """
    Input and store your account access information
    """
    typer.echo('Enter below your account access information:')
    typer.echo('It will be saved into config file')
    typer.run(conf_main)

@app.command()
def show():
    """
    Show your stored account/s access information
    """
    typer.echo('Show config file contents:')
    typer.run(conf_show)



@app.command()
def aws(    
    cost: bool = typer.Option(False,
    '--cost', '-c',
    help="Show current real costs from Cost Explorer (it generates charges)"),
    ):

    """
    Gets AWS instances data - 'costngn-cli aws --help' for options
    """
    company='aws'
    nick=choose_acc(company)
    typer.echo(f'Go to {company.upper()} data:')

    #typer.run(aws_main)
    aws_main(nick,cost)


@app.command()
def do(    
    cost: bool = typer.Option(False,
    '--cost', '-c',
    help="Show current real costs"),
    ):
    """
    Gets Digital Ocean instances data \n 'costngn-cli aws --help' for options
    """
    company='do'
    nick=choose_acc(company)
    typer.echo(f'Go to {company.upper()} data:')
    do_main(nick,cost)

    








'''

@app.command()
def hello(name:str,
    cost: bool = typer.Option(
        False, "--greet","-g",
        help="Show current real costs from Cost Explorer (0.01 USDt/query)",),
):
    """
    adding you name after 'hello' you'll be greeted
    """
    typer.echo(f"Hello {name} from costngn-cli!")
    if cost: print('Cost Explorer Enabled')


def main(what:str= typer.Argument(..., help="Action to take config|AWS")):
    print('passing for main in ct1')
    typer.echo(f"passing for main in ct1")
    #typer.run(distributor)
    typer.run(conf_post())
'''

'''
def ngn():
    
    print('go to get')

    conf_get('Jack')

'''
if __name__ == "__main__":
    app()
    



