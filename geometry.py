from fractions import Fraction as F

def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("coordinates must be integers or rational strings")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError("invalid rational coordinate") from None

def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def signed_area(ring):
    return sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(ring, ring[1:]+ring[:1])), F(0))/2

def simplify(ring):
    points = []
    for p in ring:
        if not points or p != points[-1]:
            points.append(p)
    if len(points)>1 and points[0]==points[-1]:
        points.pop()
    changed = True
    while changed and len(points)>2:
        changed = False
        for i, b in enumerate(points):
            a, c = points[i-1], points[(i+1)%len(points)]
            if cross(a,b,c)==0 and all(min(a[d],c[d])<=b[d]<=max(a[d],c[d]) for d in (0,1)):
                points.pop(i)
                changed = True
                break
    return points

def parse_ring(raw, positive):
    if not isinstance(raw, list):
        raise ValueError("ring must be an array")
    ring = []
    for p in raw:
        if not isinstance(p, list) or len(p)!=2:
            raise ValueError("point must contain two coordinates")
        ring.append((number(p[0]), number(p[1])))
    ring = simplify(ring)
    if len(ring)<3 or signed_area(ring)==0:
        raise ValueError("degenerate ring")
    if (signed_area(ring)>0)!=positive:
        ring.reverse()
    return ring

def canonical(ring, positive):
    ring = simplify(ring)
    if len(ring)<3 or signed_area(ring)==0:
        return []
    if (signed_area(ring)>0)!=positive:
        ring.reverse()
    # Numeric ordering, not lexicographic ordering of rational strings.
    ring = min(ring[i:]+ring[:i] for i in range(len(ring)))
    return [[str(x),str(y)] for x,y in ring]

def clip_ring(ring, box):
    """Exact Sutherland-Hodgman clipping of one boundary walk."""
    result = list(ring)
    x0,y0,x1,y1 = box
    for axis, edge, lower in ((0,x0,True),(0,x1,False),(1,y0,True),(1,y1,False)):
        if not result:
            break
        output = []
        def inside(p):
            return p[axis]>=edge if lower else p[axis]<=edge
        a = result[-1]
        for b in result:
            ai,bi = inside(a),inside(b)
            if ai != bi:
                t = (edge-a[axis])/(b[axis]-a[axis])
                output.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
            if bi:
                output.append(b)
            a = b
        result = simplify(output)
    return result
