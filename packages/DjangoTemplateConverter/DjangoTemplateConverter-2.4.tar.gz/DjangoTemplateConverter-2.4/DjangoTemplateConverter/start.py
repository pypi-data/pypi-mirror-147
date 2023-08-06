import argparse
import os
import importlib.util
from bs4 import BeautifulSoup
from pathlib import Path


# DjangoTemplateConverter

requiredAll = ['css', 'png', 'jpg', 'json','ico']
requiredOnly = ['css']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--su', help='arg1 help')
    parser.add_argument('--rl', help='arg2 help')
    parser.add_argument('--md', help='arg3 help')
    args = parser.parse_args()
    print("remove_length {}, static_url {}, mode {}".format(args.rl, args.su, args.md))
    removeLength = int(args.rl) if args.rl else 7
    staticUrl = args.su if args.su else 'static'
    mode = "all" if args.md else 'only'
    requiredEx = requiredAll if (mode =='all') else requiredOnly
    loadStatic = "{% load static %}"
    cwd = os.getcwd()
    lol = Path(cwd).resolve()
    BASE_DIR = [lol / 'templates']
    for temPath in BASE_DIR:
        files = os.listdir(temPath)
    # shutil.copy(settings.BASE_DIR / "writenow/build/index.html", settings.BASE_DIR / "template/index.html")
        for f in files:
            split_up = os.path.splitext(f)
            if(split_up[-1] == '.html' and len(split_up) > 1):
                file_path = temPath / f
                with open(file_path, 'r+') as file:
                    data = file.read()
                    if(loadStatic in data):
                        staticExist = True
                    else:
                        staticExist = False
                    soup = BeautifulSoup(data, "html.parser")
                    for link in soup.find_all('link', href=True):
                        splitt = link['href'].split('.')
                        # if(len(splitt)>1 and splitt[-1]=='css' and link.parent.name=='head'):
                        if(len(splitt) > 1 and splitt[-1] in requiredEx):
                            newHref = "{% "+staticUrl+" '" + \
                                link['href'][removeLength:] + "' %}"
                            link['href'] = newHref

                    for script in soup.find_all('script', src=True):
                        splitt = script['src'].split('.')
                        # if(len(splitt)>1 and splitt[-1]=='js' and script.parent.name=='body'):
                        if(len(splitt) > 1 and splitt[-1] == 'js'):
                            newSrc = "{% "+staticUrl+" '" + \
                                script['src'][removeLength:] + "' %}"
                            script['src'] = newSrc

                    file.truncate(0)
                    file.seek(0)
                    if(staticExist == False):
                        file.write(loadStatic+'\n')
                    file.write(str(soup))
                    file.close()
