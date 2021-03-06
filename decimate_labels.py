"""
Match the labels (body parts) of each original mesh to its equivalent in decimated mesh
Use 1-NN to match each face of the mesh
By inverting dirLabels and dirLabelsDecimated, it should be possible to do the inverse
mapping

Just indicate the parameters and target directories.

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np
import utils

# Set directories
root = os.getcwd()
dirMesh            = root + '/../MeshsegBenchmark-1.0/data/off/'
dirMeshDecimated   = root + '/../MeshsegBenchmark-1.0/data/off_decimated/' # Should contain the sames number and filename as above
dirLabels          = root + '/../MeshsegBenchmark-1.0/data/seg/Bench/'
dirLabelsDecimated = root + '/../MeshsegBenchmark-1.0/data/seg/Bench_decimated/'


def main():

    # Global check
    assert(os.path.exists(dirMesh))
    assert(os.path.exists(dirMeshDecimated))
    assert(os.path.exists(dirLabels))
    assert(os.path.exists(dirLabelsDecimated))
    
    # For each mesh
    filesList = utils.sortFiles(os.listdir(dirMesh))
    for filename in filesList:
        if filename.endswith('.off'): # Candidate
            print('Try matching ', filename)
            idMesh = filename.split('.')[0]
            
            # Loading the original and reduced meshes and compute the center of each face
            vertices,          faces          = utils.extractMesh(dirMesh          + filename)
            verticesDecimated, facesDecimated = utils.extractMesh(dirMeshDecimated + filename)
            
            pointCloud          = utils.meshToPointCloud(vertices,          faces)
            pointCloudDecimated = utils.meshToPointCloud(verticesDecimated, facesDecimated)
            
            # Extract the label list
            labelList = utils.loadLabelList(dirLabels + idMesh + '.seg')
            labelListDecimated = []
            
            # Use K-NN on each face of the decimated mesh
            for pointDecimated in pointCloudDecimated:
                # Search the closest point index in the original point cloud
                minIndex = 0
                minDist = -1 # Initialize
                for i, point in enumerate(pointCloud):
                    distance = np.linalg.norm(pointDecimated - point)
                    if distance < minDist or minDist == -1:
                        minDist = distance
                        minIndex = i
                
                labelListDecimated.append(labelList[minIndex])
                if len(labelListDecimated) % 100 == 0:
                    print(len(labelListDecimated) / len(pointCloudDecimated) * 100, '%')
                
            # Save the values of the labels of the closest match indexes
            saveName = dirLabelsDecimated + idMesh + '.seg'
            print('Saving ', saveName)
            utils.saveLabelList(labelListDecimated, saveName)
    

if __name__ == "__main__":
    main()
    