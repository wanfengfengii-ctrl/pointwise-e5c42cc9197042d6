# Coordinates describe retained survey polygons, not raster cells.
NORMAL = {"size":10,"features":[
    {"id":"solid","outer":[[1,1],[9,1],[9,9],[1,9]],"holes":[]},
    {"id":"courtyard","outer":[[1,1],[9,1],[9,9],[1,9]],
     "holes":[[[3,3],[3,7],[7,7],[7,3]]]},
    {"id":"rational","outer":[["-3/2","1/2"],["3/2","1/2"],[0,"7/2"]],"holes":[]}
]}
INCIDENT = {"size":10,"features":[
    {"id":"fork","outer":[[1,1],[3,1],[3,12],[7,12],[7,1],[9,1],[9,14],[1,14]],"holes":[]},
    {"id":"pinch","outer":[[1,1],[5,10],[9,1],[9,14],[1,14]],"holes":[]},
    {"id":"opened-courtyard","outer":[[1,1],[9,1],[9,14],[1,14]],
     "holes":[[[4,3],[4,12],[6,12],[6,3]]]}
]}
