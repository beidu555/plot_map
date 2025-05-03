import os

# 本函数的根本作用，是将folium所生成的html文件中的相关js/css引用链接，替换为本地的js/css路径。所使用的路径为相对路径，所以在打开html文件的时候，需要将html文件与src文件夹放置在同一个路径下
def replaceJsRef(fileFullName):
    replaceContents = [['''<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>''',
                        '''<script src="./src/jQuery/jquery-2.0.0.js"></script>'''],
                       ['''<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>''',
                        '''<script src="./src/jQuery/jquery-2.0.0.js"></script>'''],
                       ['''<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>''',
                        '''<script src="./src/leaflet/leaflet.js"></script>'''],
                       ['''<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>''',
                        '''<script src="./src/bootstrap-5.2.2/js/bootstrap.min.js"></script>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>''',
                        '''<script src="./src/Leaflet.awesome-markers-2.0/dist/leaflet.awesome-markers.js"></script>'''],
                       ['''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/leaflet/leaflet.css"/>'''],
                       ['''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/bootstrap-5.2.2/css/bootstrap.min.css"/>'''],
                       ['''<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/bootstrap-5.2.2/css/bootstrap-theme.min.css"/>'''],
                       ['''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/font-awesome-4.7.0/css/font-awesome.min.css"/>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/Leaflet.awesome-markers-2.0/dist/leaflet.awesome-markers.css"/>'''],
                       ['''<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/leaflet.awesome.rotate/leaflet.awesome.rotate.css"/>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>''',
                        '''<script src="./src/leaflet.markercluster/dist/leaflet.markercluster.js"></script>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/leaflet.markercluster/dist/MarkerCluster.css"/>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="./src/leaflet.markercluster/dist/MarkerCluster.Default.css"/>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.3.0/leaflet-dvf.markers.min.js"></script>''',
                        '''<script src="./src/leaflet-dvf/leaflet-dvf.markers.min.js"></script>'''],
                        ['''<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css"/>''',
                         '''<link rel="stylesheet" href="./src/bootstrap-5.2.2/css/bootstrap-glyphicons.css"/>''']
                       ]

    with open(fileFullName, "r", encoding="utf-8") as f1, open("%s.bak" % fileFullName, "w", encoding="utf-8") as f2:
        for line in f1:
            for itm in replaceContents:
                if itm[0] in line:
                    line = line.replace(itm[0], itm[1])
                    replaceContents.remove(itm)
            f2.write(line)
    os.remove(fileFullName)
    os.rename("%s.bak" % fileFullName, fileFullName)
