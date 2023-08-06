import platform,os,sys
from pathlib import Path

def main() :

    try:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
    except:
        print("\n❌️ Erreur d'execution ❌️")
        print("   Cause : Arguments requis pour l'exécution du script.\n")
        sys.exit(1)

    if platform.system() == 'Windows':
        os.system(str(Path(__file__).resolve().parent)+"\dist\main.exe %s %s" % (client_id,client_secret))
    else :
        os.system(str(Path(__file__).resolve().parent)+"/dist/main %s %s" % (client_id,client_secret))
