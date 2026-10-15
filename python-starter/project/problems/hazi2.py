import sys

from project.problem import Problem
import argparse

class hazi2problem(Problem):
    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--det', action='store_true', help='determinalize the input')
    def is_chosen_problem(self, args):
        return bool(args.det)

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
            print("Hiba: pontosan egy kezdoallapot szikseges.", file=sys.stderr)
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
            delta.setdefault((src, sym), set()).add(dst)

        sorted_alphabet = sorted(alpha_set)
        final_set = set(finals)

        start_subset = frozenset([start])
        index = {start_subset: 0}
        order = [start_subset]
        trans = []  # (src, sym, dst)

        i = 0
        while i < len(order):
            current = order[i]
            for sym in sorted_alphabet:
                target = set()
                for q in current:
                    target |= delta.get((q, sym), set())
                if not target:
                    continue
                target = frozenset(target)
                if target not in index:
                    index[target] = len(order)
                    order.append(target)
                trans.append((i, sym, index[target]))
            i += 1

        new_finals = [k for k, subset in enumerate(order) if subset & final_set]
        trans.sort(key=lambda t: (t[0], t[1], t[2]))
        out = []
        out.append(" ".join(f"s{k}" for k in range(len(order))))
        out.append(" ".join(sorted_alphabet))
        out.append("s0")
        out.append(" ".join(f"s{k}" for k in new_finals))
        for src, sym, dst in trans:
            out.append(f"s{src} {sym} s{dst}")
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("\n".join(out) + "\n")



