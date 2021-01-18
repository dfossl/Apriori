import AprioriPruningOptimized as APO
import argparse


parser = argparse.ArgumentParser(description='Perform Apriori On Dataset.')

parser.add_argument('-f',
                    dest="filename",
                    type=str,
                    nargs=1,
                    help='File directory of data file.',
                    required=True)

parser.add_argument('-minsup',
                    "-m",
                    type=int,
                    dest="minsup",
                    nargs=1,
                    help="Minimum support percent. Must be integer [1-100]",
                    required=True,
                    metavar="[1-100]",
                    choices=range(1,101))

parser.add_argument('-o',
                    dest="outputfile",
                    type=str,
                    nargs=1,
                    help='output file directory.',
                    required=True)

args = parser.parse_args()

apriori = APO.AprioriPruningOptimized()

apriori.apriori(filename=args.filename[0], minimumsup=args.minsup[0])
apriori.results_to_file(filename=args.outputfile[0])
apriori.printterminal()

