from VideoBot import VideoBot
from os.path import exists
import os
import sys

fileConfig="Config";

if exists(fileConfig):
    fConfig = open(fileConfig, "r");
    config = fConfig.readlines();
    fConfig.close();
    token=config[0].replace("\n","");
    urlBase=config[1].replace("\n","");
elif len(sys.argv)>1:
    token=sys.argv[1];
    urlBase=sys.argv[2];
    fConfig = open(fileConfig, 'w');
    fConfig.writelines([token,urlBase]);
    fConfig.close();

print("Iniciando Bot V3.0");
VideoBot(token, urlBase).Start().run_forever();