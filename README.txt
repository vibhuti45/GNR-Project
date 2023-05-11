
GNR602 Course Project

Topic: 	For a multispectral remote sensed image apply PCA for dimensionality reduction then for PC1 apply GLCM to extract features by varying window size 9*9, 11*11, 13*13, 15*15, 17*17 and 19*19. Classify the image using the features thus collected.

Description:

Multispectral images are high dimensional images generally satellite images. Our input dataset “data.tif” is an image of 8 dimension. Dealing with such high dimensions make the work hard and time taking and also space consuming. Therefore we try to reduce the dimension of image without losing much information. We apply Principal Component Analysis to reduce the dimension to 1. This is done using finding the projections of datapoints on to several eigenvectors. Finally we chose that dimension as PC1 which has the highest eigenvalue associated with it. Thus we get the PC1 as our output with just one 1 band.

Executable file:
The EXE file is located at dist folder. This file will only run on windows.

Def Main basically is the body of the interface. It takes in different parameters like Max GLCM size, Initial Coordinates of patch, direction and no of clusters etc and the output is PC1, PC1 with normalization and the final segmented image.

Maxi : Maxi/k is distance between two adjacent centroid where k is the no of cluster.
Window size: Size of patch for GLCM construction
GLCM size
Initial1, Initial2 : Initial (top-left corner) coordinate of patch (input image)
Size1, size2: Size of Input image
Clusters: No of cluster
D1, d2: Direction vector


Now comes the process of forming GLCM matrix for each pixel of the image. For this we map every pixel with an arbitrary chosen window size with arbitrary direction and offset. Thus we obtain the matrices with the process explained in Slides. We have coded the GLCM making process under a separate function.

Def Compute GLCM computes the GLCM matrix. Def GLCM features computes the Features of each pixel.

The third step that is actually how to calculate the features i.e. IDM, ASM, Contrast. This step goes in parallel with the computation of Matrix to reduce redundancy and space. The formula for all these features associated with each pixel is already given in the slides. We store all these data in an 2D array.

Now finally we apply the K-means Algorithm to cluster the pixels with similar features.

Def K-Means CLuster: This function segments the input image into clusters of similar features.

Thank You

References:

1) GNR602 slides
2)towardsdatascience

