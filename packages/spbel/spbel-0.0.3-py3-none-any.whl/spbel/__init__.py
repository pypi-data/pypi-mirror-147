import sys
import time
import argparse
import _thread as th
from .proxy import run_proxy
from .rapel import run_rapel
from .reply import run_reply

def run_emitter(args):
    print("Running SPBEL Emitter: Proxy port = {}, Rapel port= {}, Data Path = {}".format(
        args.proxyport, args.emitterport, args.datapath
    ))
    try:    
        proxy_th = th.start_new_thread(run_proxy, (args.proxyport,args.datapath))
        rapel_th = th.start_new_thread(run_rapel, (args.emitterport,args.datapath))
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exit")

def run_collector(args):
    run_reply(args.source, args.archivepath, args.collectorpath)

def run_default(args):
    print("Run: spbel -h for help")

def cmd_run():
    cmd_parse = argparse.ArgumentParser(prog="spbel")
    cmd_parse.set_defaults(func=run_default)
    subparse = cmd_parse.add_subparsers()

    emiter = subparse.add_parser("emitter")
    emiter.add_argument("-p", 
            type=int, default=9097,dest="proxyport", 
            help='Proxy port for used in sentry proxy')
    emiter.add_argument("-e", 
            type=int, default=7000, dest="emitterport",
            help='Emitter port for nginx proxy source')
    emiter.add_argument("-d", 
            type=str, default="/tmp/spbel", dest="datapath",
            help='Data path where app should store json data')
    emiter.set_defaults(func=run_emitter)

    collector = subparse.add_parser("collector")
    collector.set_defaults(func=run_collector)
    collector.add_argument("source",type=str,
            help='Emitter Source URL')
    collector.add_argument("-a", 
            type=str, default="/tmp/spbel.tar", dest="archivepath",
            help='Data path where app should store temporary emitter response')
    collector.add_argument("-c", 
            type=str, default="/tmp/spbel_collector", dest="collectorpath",
            help='Where should app store temporary exteracted data')

    args = cmd_parse.parse_args()

    args.func(args)
