import typer
from ngn.config.config import *
from ngn.aws.data00 import *

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

@app.command()
def config():
    """
    Input and store your account access information
    """
    typer.echo('Enter below your account access information:')
    typer.echo('It will be saved into current folder')
    typer.run(conf_post)

@app.command()
def show():
    """
    Show your stored account access information
    """
    typer.echo('Show config file contents:')
    typer.run(conf_get)



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




@app.command()
def aws(    
    cost: bool = typer.Option(False,
    '--cost', '-c',
    help="Show current real costs from Cost Explorer (it generates charges)"),
    ):
    """
    Gets AWS instances data - 'costngn-cli aws --help' for options
    """
    #print('nothing here by now')
    typer.echo(f'Go to AWS data:')
    #typer.run(aws_main)
    aws_main('some',cost)


'''
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
    



