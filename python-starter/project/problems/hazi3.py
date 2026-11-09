import re
import sys

from project.problem import Problem
import argparse


def natural_key(name):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', name)]


def new_name(name):
    rest = re.sub(r'^[A-Za-z_]+', '', name)
    return "s" + (rest if rest else name)


class hazi3problem(Problem):
    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--mini', action='store_true', help='minimize the input DFA')

    def is_chosen_problem(self, args):
        return bool(args.mini)

    def run(self, args):
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except OSError as e:
            print(f"Hiba: a bemeneti fajl nem olvashato: {e}", file=sys.stderr)
            return

        if len(lines) < 4:
            print("Hiba: a bemeneti fajl legalabb 4 sort kell tartalmazzon.", file=sys.stderr)
            return

        states = lines[0].split()
        alphabet = lines[1].split()
        start_tokens = lines[2].split()
        finals = lines[3].split()

        if len(start_tokens) != 1:
            print("Hiba: pontosan egy kezdoallapot szukseges.", file=sys.stderr)
            return
        start = start_tokens[0]

        state_set = set(states)
        alpha_set = set(alphabet)

        if start not in state_set:
            print(f"Hiba: ismeretlen kezdoallapot: {start}", file=sys.stderr)
            return
        for q in finals:
            if q not in state_set:
                print(f"Hiba: ismeretlen vegallapot: {q}", file=sys.stderr)
                return
        delta = {}
        for i, line in enumerate(lines[4:], start=5):
            parts = line.split()
            if len(parts) != 3:
                print(f"Hiba: hibas atmenet a {i}. sorban: '{line}'", file=sys.stderr)
                return
            src, sym, dst = parts
            if src not in state_set:
                print(f"Hiba: ismeretlen allapot a {i}. sorban: {src}", file=sys.stderr)
                return
            if dst not in state_set:
                print(f"Hiba: ismeretlen allapot a {i}. sorban: {dst}", file=sys.stderr)
                return
            if sym not in alpha_set:
                print(f"Hiba: ismeretlen jel a {i}. sorban: {sym}", file=sys.stderr)
                return
            if (src, sym) in delta and delta[(src, sym)] != dst:
                print(f"Hiba: az automata nem determinisztikus a {i}. sorban: '{line}'",
                      file=sys.stderr)
                return
            delta[(src, sym)] = dst

        sorted_alphabet = sorted(alpha_set)
        final_set = set(finals)
        reachable = {start}
        stack = [start]
        while stack:
            q = stack.pop()
            for a in sorted_alphabet:
                t = delta.get((q, a))
                if t is not None and t not in reachable:
                    reachable.add(t)
                    stack.append(t)
        live = sorted(reachable, key=natural_key)
        cls = {q: (1 if q in final_set else 0) for q in live}
        count = len(set(cls.values()))
        while True:
            signatures = {}
            new_cls = {}
            for q in live:
                sig = (cls[q],) + tuple(
                    cls[delta[(q, a)]] if (q, a) in delta else -1
                    for a in sorted_alphabet
                )
                if sig not in signatures:
                    signatures[sig] = len(signatures)
                new_cls[q] = signatures[sig]
            cls = new_cls
            if len(signatures) == count:
                break
            count = len(signatures)
        members = {}
        for q in live:
            members.setdefault(cls[q], []).append(q)
        rep = {c: min(qs, key=natural_key) for c, qs in members.items()}
        name_of = {q: rep[cls[q]] for q in live}

        reps = sorted(set(rep.values()), key=natural_key)
        out_start = name_of[start]
        out_finals = sorted({name_of[q] for q in live if q in final_set}, key=natural_key)

        trans = set()
        for q in live:
            for a in sorted_alphabet:
                t = delta.get((q, a))
                if t is not None:
                    trans.add((name_of[q], a, name_of[t]))
        trans = sorted(trans, key=lambda t: (natural_key(t[0]), t[1], natural_key(t[2])))

        out = []
        out.append(" ".join(new_name(q) for q in reps))
        out.append(" ".join(sorted_alphabet))
        out.append(new_name(out_start))
        out.append(" ".join(new_name(q) for q in out_finals))
        for src, sym, dst in trans:
            out.append(f"{new_name(src)} {sym} {new_name(dst)}")
        #proba
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write("\n".join(out) + "\n")
        except OSError as e:
            print(f"Hiba: a kimeneti fajl nem irhato: {e}", file=sys.stderr)