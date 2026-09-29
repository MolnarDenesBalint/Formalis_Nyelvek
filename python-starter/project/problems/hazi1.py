from project.problem import Problem
import argparse

class hazi1problem(Problem):
    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--check', type=str, help='check the given words')
    def is_chosen_problem(self, args):
        return bool(args.check)

    def run(self, args):
        input_file = args.input
        output_file = args.output
        with open(input_file, 'r') as f:
            lines=[line.strip() for line in f if line.strip()]
        if len(lines) < 4:
            raise ValueError("Hiba a bemeneti allomanyban")
        allapotok=lines[0].split()
        betuk = lines[1].split()
        kezdopont= lines[2]
        vegpontok = lines[3].split()
        atmenetek={}
        for line in lines[4:]:
            utak = line.split()
            if len(utak) != 3:
                raise ValueError("Hiba a bemeneti allomanyban")
            ind, ert, cel = utak
            atmenetek[(ind, ert)]=cel
        szavak = args.check.split(',')
        eredmenyek=[]
        for szo in szavak:
            curr=kezdopont
            talal=True
            for betu in szo:
                key =(curr, betu)
                if key in atmenetek:
                    curr=atmenetek[key]
                else:
                    talal=False
                    break
            if talal==True and curr in vegpontok:
                eredmenyek.append("IGEN")
            else:
                eredmenyek.append("NEM")
        with open(output_file, 'w') as f:
            f.write("\n".join(eredmenyek)+"\n")


