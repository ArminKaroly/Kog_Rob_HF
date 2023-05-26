#!/bin/bash

for i in {0..100}
do
   roslaunch aruco_description generate_aruco.launch aruco_dictionary:="DICT_4X4_100" aruco_ids:=$i
done