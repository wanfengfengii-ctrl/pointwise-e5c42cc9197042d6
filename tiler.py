import math
from fractions import Fraction as F
from geometry import number, parse_ring, signed_area, canonical, clip_ring

def tile(feature, size):
    """Yield tile rows in (iy, ix) order; the source feature is not mutated."""
    size = number(size)
    if size<=0:
        raise ValueError("size must be positive")
    if not isinstance(feature, dict) or not isinstance(feature.get("id"), str) or not feature["id"]:
        raise ValueError("feature id must be a nonempty string")
    if "outer" not in feature:
        raise ValueError("outer is required")
    outer = parse_ring(feature["outer"], True)
    raw_holes = feature.get("holes", [])
    if not isinstance(raw_holes, list):
        raise ValueError("holes must be an array")
    holes = [parse_ring(h,False) for h in raw_holes]
    xs,ys = zip(*outer)
    left,right = math.floor(min(xs)/size), math.ceil(max(xs)/size)-1
    bottom,top = math.floor(min(ys)/size), math.ceil(max(ys)/size)-1
    for iy in range(bottom,top+1):
        for ix in range(left,right+1):
            box = (ix*size,iy*size,(ix+1)*size,(iy+1)*size)
            shell = clip_ring(outer,box)
            if len(shell)<3 or not signed_area(shell):
                continue
            cut_holes = []
            for hole in holes:
                cut = clip_ring(hole,box)
                if len(cut)>=3 and signed_area(cut):
                    cut_holes.append(cut)
            total = abs(signed_area(shell))-sum((abs(signed_area(h)) for h in cut_holes),F(0))
            if total<=0:
                continue
            fragment = {"outer":canonical(shell,True),
                        "holes":sorted((canonical(h,False) for h in cut_holes))}
            yield {"id":feature["id"],"tile":[ix,iy],
                   "fragments":[fragment],"area":str(total)}

def run(document):
    if not isinstance(document,dict) or not isinstance(document.get("features"),list) or "size" not in document:
        raise ValueError("expected size and features")
    size=number(document["size"])
    if size<=0:
        raise ValueError("size must be positive")
    for feature in document["features"]:
        yield from tile(feature,size.numerator if size.denominator==1 else str(size))
