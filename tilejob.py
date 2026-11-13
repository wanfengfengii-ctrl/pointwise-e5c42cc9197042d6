import json
import sys
from tiler import run

def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: python3 tilejob.py INPUT.json")
    try:
        with open(sys.argv[1],encoding="utf-8") as source:
            document = json.load(source)
        for row in run(document):
            print(json.dumps(row,ensure_ascii=False,separators=(",",":")))
    except (ValueError,KeyError,TypeError) as exc:
        print(json.dumps({"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)

if __name__=="__main__":
    main()
