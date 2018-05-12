# -*- coding: utf-8 -*-
"""
Created on Sat May 12 07:26:09 2018

@author: aperez
"""

cluster_list = [alg_cluster.Cluster(set(['1']), 0.11, 0.75, 1, 0), 
                alg_cluster.Cluster(set(['2']), 0.62, 0.86, 1, 0), 
                alg_cluster.Cluster(set(['3']), 0.65, 0.68, 1, 0), 
                alg_cluster.Cluster(set(['4']), 0.68, 0.48, 1, 0), 
                alg_cluster.Cluster(set(['5']), 0.7, 0.9, 1, 0), 
                alg_cluster.Cluster(set(['6']), 0.79, 0.18, 1, 0)]


# the code below is expected to return the value of the last line
cluster_list = [alg_cluster.Cluster(set(['01073']), 704.191210749, 411.014665198, 662047, 7.3e-05), alg_cluster.Cluster(set(['06059']), 113.997715586, 368.503452566, 2846289, 9.8e-05), alg_cluster.Cluster(set(['06037']), 105.369854549, 359.050126004, 9519338, 0.00011), alg_cluster.Cluster(set(['06029']), 103.787886113, 326.006585349, 661645, 9.7e-05), alg_cluster.Cluster(set(['06071']), 148.402461892, 350.061039619, 1709434, 7.7e-05), alg_cluster.Cluster(set(['06075']), 52.7404001225, 254.517429395, 776733, 8.4e-05), alg_cluster.Cluster(set(['08031']), 371.038986573, 266.847932979, 554636, 7.9e-05), alg_cluster.Cluster(set(['24510']), 872.946822486, 249.834427518, 651154, 7.4e-05), alg_cluster.Cluster(set(['34013']), 906.236730753, 206.977429459, 793633, 7.1e-05), alg_cluster.Cluster(set(['34039']), 905.587082153, 210.045085725, 522541, 7.3e-05), alg_cluster.Cluster(set(['34017']), 909.08042421, 207.462937763, 608975, 9.1e-05), alg_cluster.Cluster(set(['36061']), 911.072622034, 205.783086757, 1537195, 0.00015), alg_cluster.Cluster(set(['36005']), 912.315497328, 203.674106811, 1332650, 0.00011), alg_cluster.Cluster(set(['36047']), 911.595580089, 208.928374072, 2465326, 9.8e-05), alg_cluster.Cluster(set(['36059']), 917.384980291, 205.43647538, 1334544, 7.6e-05), alg_cluster.Cluster(set(['36081']), 913.462051588, 207.615750359, 2229379, 8.9e-05), alg_cluster.Cluster(set(['41051']), 103.293707198, 79.5194104381, 660486, 9.3e-05), alg_cluster.Cluster(set(['41067']), 92.2254623376, 76.2593957841, 445342, 7.3e-05), alg_cluster.Cluster(set(['51013']), 865.681962839, 261.222875114, 189453, 7.7e-05), alg_cluster.Cluster(set(['51840']), 845.843602685, 258.214178983, 23585, 7.1e-05), alg_cluster.Cluster(set(['51760']), 865.424050159, 293.735963553, 197790, 8.6e-05), alg_cluster.Cluster(set(['55079']), 664.855000617, 192.484141264, 940164, 7.4e-05), alg_cluster.Cluster(set(['54009']), 799.221537984, 240.153315109, 25447, 7.7e-05), alg_cluster.Cluster(set(['11001']), 867.470401202, 260.460974222, 572059, 7.7e-05)]
print hierarchical_clustering(cluster_list, 23)