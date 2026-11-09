import re
import sys

from project.problem import Problem
import argparse


LINE_RE = re.compile(r'(([0-9-]+ [0-9:.]+) +([0-9]+) +([0-9]+) ([IDVEFAW]) (.+?):(?: (.+))?)')

PREFIX = r'\s*[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ '

DATE_1015_RE = re.compile(r'\s*10-15 ')
TIME_101851_RE = re.compile(r'\s*10-15 10:18:51\.')
SEC_51_RE = re.compile(r'\s*[0-9-]+ [0-9]{2}:[0-9]{2}:51\.')
LOWMEM_RE = re.compile(PREFIX + r'[IDVEFAW] [^:]*lowmemorykiller[^:]*:')
PID221_RE = re.compile(r'\s*[0-9-]+ 10:18:51\.[0-9]+ +221 ')
ERROR_RE = re.compile(PREFIX + r'E ')
PKGMAN_WARN_RE = re.compile(PREFIX + r'W PackageManager\s*:')
EXO_DEBUG_RE = re.compile(PREFIX + r'D [^:]*ExoPlayer[^:]*:')
JAVA_POS_RE = re.compile(PREFIX + r'[EW] .*\.java:')
THREAD_MSG_RE = re.compile(PREFIX + r'[IDVEFAW] [^:]*: .*Thread')

JAVA_FILE_RE = re.compile(r'([A-Za-z0-9_$]+\.java):[0-9]+')

MAIN_THREAD_ERR_RE = re.compile(PREFIX.replace(r'[0-9]+ +[0-9]+ ', r'([0-9]+) +\1 ') + r'E ')


class hazi4problem(Problem):
    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--rgx', type=int, default=None,
                            help='regex task number (1-5)')

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        if args.rgx not in (1, 2, 3, 4, 5):
            print(f"Hiba: ismeretlen feladatszam: {args.rgx}", file=sys.stderr)
            return

        try:
            with open(args.input, 'r', encoding='utf-8', errors='replace') as f:
                lines = [line.rstrip('\r\n') for line in f]
        except OSError as e:
            print(f"Hiba: a bemeneti fajl nem olvashato: {e}", file=sys.stderr)
            return

        if args.rgx == 1:
            out = self.task1(lines)
        elif args.rgx == 2:
            out = self.task2(lines)
        elif args.rgx == 3:
            out = self.task3(lines)
        elif args.rgx == 4:
            out = self.task4(lines)
        else:
            out = self.task5(lines)

        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write("".join(s + "\n" for s in out))
        except OSError as e:
            print(f"Hiba: a kimeneti fajl nem irhato: {e}", file=sys.stderr)

    def task1(self, lines):
        patterns = [
            DATE_1015_RE, TIME_101851_RE, SEC_51_RE, LOWMEM_RE, PID221_RE,
            ERROR_RE, PKGMAN_WARN_RE, EXO_DEBUG_RE, JAVA_POS_RE, THREAD_MSG_RE,
        ]
        counts = [0] * len(patterns)
        for line in lines:
            for k, rx in enumerate(patterns):
                if rx.match(line):
                    counts[k] += 1
        return [str(c) for c in counts]

    def task2(self, lines):
        result = []
        in_error = False
        for line in lines:
            if LINE_RE.match(line):
                in_error = bool(ERROR_RE.match(line))
                if in_error:
                    result.extend(JAVA_FILE_RE.findall(line))
            elif in_error:
                result.extend(JAVA_FILE_RE.findall(line))
        return result

    def task3(self, lines):
        seen = set()
        order = []
        for line in lines:
            m = LINE_RE.match(line)
            if m:
                pid = m.group(3)
                if pid not in seen:
                    seen.add(pid)
                    order.append(pid)
        return order

    def task4(self, lines):
        counts = {}
        for line in lines:
            m = LINE_RE.match(line)
            if m and ERROR_RE.match(line):
                pid = m.group(3)
                counts[pid] = counts.get(pid, 0) + 1
        if not counts:
            return []
        best_pid = None
        best = 0
        for pid, c in counts.items():
            if c > best:
                best = c
                best_pid = pid
        return [f"PID={best_pid} ({best} errors)"]
    def task5(self, lines):
        return [str(sum(1 for line in lines if MAIN_THREAD_ERR_RE.match(line)))]