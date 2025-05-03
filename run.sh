RAW_LOCATION_DIR='raw_location' #存储要绘制路径的地点文件，一个文件代表要绘制的一条路线
JINGWEIDU_LOCATION_DIR='jingweidu_location' #存储带有经纬度的地点文件
HTML_FILE_NAME='test.html' #保存路径的html文件名
MAP_TYPE='街道图' #地图的类型，街道图，路网图，卫星图

python road_map.py --raw_location_dir $RAW_LOCATION_DIR \
                   --jingweidu_location_dir $JINGWEIDU_LOCATION_DIR \
                   --html_file_name $HTML_FILE_NAME \
                   --map_type $MAP_TYPE