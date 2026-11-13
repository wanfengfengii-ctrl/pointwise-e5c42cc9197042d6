import copy
import json
import sys
from fractions import Fraction as F
from tiler import run
from samples import NORMAL, INCIDENT

def ring(points, positive=True):
    values=[(F(x),F(y)) for x,y in points]
    twice=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(values,values[1:]+values[:1]))
    if (twice>0)!=positive:
        values.reverse()
    values=min(values[i:]+values[:i] for i in range(len(values)))
    return [[str(x),str(y)] for x,y in values]

def fragment(points, holes=()):
    return {"outer":ring(points),"holes":sorted(ring(h,False) for h in holes)}

def normalized(parts):
    return sorted(parts,key=lambda p:json.dumps(p,sort_keys=True))

def rows(doc):
    return {(r["id"],*r["tile"]):r for r in run(doc)}

def normal():
    frozen = copy.deepcopy(NORMAL)
    actual = rows(NORMAL)
    assert NORMAL==frozen
    assert set(actual)=={("solid",0,0),("courtyard",0,0),("rational",-1,0),("rational",0,0)}
    assert actual[("solid",0,0)]["fragments"]==[fragment([(1,1),(9,1),(9,9),(1,9)])]
    assert actual[("solid",0,0)]["area"]=="64"
    assert actual[("courtyard",0,0)]["fragments"]==[fragment(
        [(1,1),(9,1),(9,9),(1,9)], [[(3,3),(3,7),(7,7),(7,3)]])]
    assert actual[("courtyard",0,0)]["area"]=="48"
    assert sum(F(r["area"]) for r in actual.values() if r["id"]=="rational")==F(9,2)
    # Translating by one grid width must preserve exact vertices and tile identity.
    moved = copy.deepcopy(NORMAL)
    for feature in moved["features"]:
        for boundary in [feature["outer"]]+feature["holes"]:
            for p in boundary:
                p[0]=str(F(p[0])+10)
    shifted = rows(moved)
    for (fid,x,y),old in actual.items():
        new=shifted[(fid,x+1,y)]
        assert old["area"]==new["area"]
        recovered=copy.deepcopy(new["fragments"])
        for part in recovered:
            for boundary in [part["outer"]]+part["holes"]:
                for p in boundary:
                    p[0]=str(F(p[0])-10)
        assert normalized(recovered)==normalized(old["fragments"])
    try:
        list(run({"size":0,"features":NORMAL["features"]}))
    except ValueError:
        pass
    else:
        raise AssertionError("zero tile size accepted")
    print("NORMAL_REGRESSION_OK")

def incident():
    actual=rows(INCIDENT)
    expected={
        ("fork",0,0):[fragment([(1,1),(3,1),(3,10),(1,10)]),
                        fragment([(7,1),(9,1),(9,10),(7,10)])],
        ("fork",0,1):[fragment([(1,10),(3,10),(3,12),(7,12),(7,10),(9,10),(9,14),(1,14)])],
        ("pinch",0,0):[fragment([(1,1),(5,10),(1,10)]),fragment([(5,10),(9,1),(9,10)])],
        ("pinch",0,1):[fragment([(1,10),(5,10),(9,10),(9,14),(1,14)])],
        ("opened-courtyard",0,0):[fragment([(1,1),(9,1),(9,10),(6,10),(6,3),(4,3),(4,10),(1,10)])],
        ("opened-courtyard",0,1):[fragment([(1,10),(4,10),(4,12),(6,12),(6,10),(9,10),(9,14),(1,14)])]
    }
    issues=[]
    if set(actual)!=set(expected):
        issues.append({"keys":list(map(str,set(actual)^set(expected)))})
    for key,want in expected.items():
        got=actual.get(key,{})
        if normalized(got.get("fragments",[]))!=normalized(want):
            issues.append({"key":list(key),"expected":want,"actual":got.get("fragments")})
    # These deliberately pass on the broken implementation: area is not topology.
    assert actual[("fork",0,0)]["area"]=="36"
    assert actual[("pinch",0,0)]["area"]=="36"
    assert actual[("opened-courtyard",0,0)]["area"]=="58"
    if issues:
        print("TILE_TOPOLOGY_MISMATCH "+json.dumps(issues,sort_keys=True))
        raise SystemExit(1)
    print("TOPOLOGY_REGRESSION_OK")

def demo():
    for label,doc in (("normal",NORMAL),("incident",INCIDENT)):
        print(json.dumps({"case":label,"rows":list(run(doc))},ensure_ascii=False))

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else "verify"
    if mode=="normal":
        normal()
    elif mode=="incident":
        incident()
    elif mode=="verify":
        normal()
        incident()
    elif mode=="demo":
        demo()
    else:
        raise SystemExit("normal | incident | verify | demo")

if __name__=="__main__":
    main()
