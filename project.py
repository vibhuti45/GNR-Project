
#def mainf takes input several parameters like max glcm size, direction, input file etc.

def mainf(m,wi,givenk,g,i1,i2,s1,s2,input_file_path,d1,d2):
#converting tiff file into array
    import tifffile as tiff
    print(input_file_path)
    imgo=tiff.imread(input_file_path)
    print(imgo.shape)
    import cv2
    from skimage.feature import graycomatrix
    import math
    import numpy as np
    from matplotlib import pyplot as plt
    from sklearn.metrics import silhouette_score

#      Progress bar

    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Progress Window")
    root.geometry("800x100")
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=450, mode="determinate")
    progress_bar.pack(pady=10)

    def update_progress(progress_label, progress):
        progress_label.config(text="Progress: {:.2f}%".format(progress))
        root.update()
    
    progress_label = tk.Label(root, text="Progress: 0.00%")
    progress_label.pack(padx=10, pady=10)
    
    max=m
    w=[wi]
    g=g
    init1=i1
    init2=i2
    size1=s1
    size2=s2
    img= imgo[init1:init1+size1, init2:init2+size2, :]

    def ishow(data1,data2): 
    #plotting graphs
        plt.rcParams["figure.figsize"] = [10.00, 5.00]
        plt.rcParams["figure.autolayout"] = True
        plt.subplot(1, 2, 1)
        plt.title("1.PCA1")
        plt.imshow(data1)
        plt.subplot(1, 2, 2)
        plt.title("2.output")
        plt.imshow(data2)
        plt.show()

    
    #def used for computing GLCM. Takes in input image, window size, ddirection
    def compute_glcm(img, window_size,g,d1,d2):
        glcm = np.zeros((g,g))
        for i in range(0,img.shape[0] - d1):
            for j in range(img.shape[1] - d2):
                try:
                    p = img[i, j]
                    q = img[i+d1, j+d2]
                    glcm[p,q] += 1
                    glcm[q,p] += 1
                except IndexError:
                    pass

            #computing features for each GLCM
        sum1 = 0
        energy = 0
        homo = 0
        asm = 0
        ent = 0
        idm=0

        for i in range(0, glcm.shape[0]):
            for j in range(0, glcm.shape[1]):
                sum1 = sum1 + ((i-j)*(i-j)*glcm[i,j])
                energy = energy + glcm[i,j]*glcm[i,j]
                homo = homo + (glcm[i,j]/(1+abs(i-j)))
                idm = idm + glcm[i, j]/(1+(i-j)*(i-j))
                ent = ent + glcm[i,j]*math.log(1/(0.01 + glcm[i,j]))
        
    


 

        return sum1, ent, homo, idm, asm
        
        
        
        
    #construction of patches of window size around a given pixel

    def compute_glcm_features(img, pca_idx, window_sizes,g,d1,d2):
        # Compute the GLCM features for PCA1
        img_pca = img
        features = []
        
        for w in window_sizes:
            s=img_pca.shape[0] - w
            window_half = w // 2
            for i in range(window_half, img_pca.shape[0] - window_half):
                for j in range(window_half, img_pca.shape[1] - window_half):
                    img_window = img_pca[i-window_half:i+window_half+1, j-window_half:j+window_half+1]
                    sum1, energy, homo, asm, ent = compute_glcm(img_window, w,g,d1,d2)
                    print(sum1)
                    feature=np.array([sum1, energy, homo, asm, ent])
                    print(i,j,feature)
                    update_progress(progress_label, (((i/(img_pca.shape[1] - window_half))*100)+(j/(img_pca.shape[1] - window_half))))
                    progress_bar["value"] = (i/(img_pca.shape[1] - window_half))*100
                    #bval=bval+ (300/(s*s))
                    features.append(feature)
        features = np.stack(features, axis=1)
        root.destroy()
        return features

    # normalizing the image from 2048 scale to arbitrary scale.
    def normalize_array(arr,g):
        min_val = np.min(arr)
        max_val = np.max(arr)
        

        arr_norm = (arr - min_val) / (max_val - min_val)
        
        arr_scaled = (arr_norm * (g-1)).astype(int)
        
        return arr_scaled

    def showimg(imgi,name):
        cv2.imwrite(name,imgi)

    print(img.shape)
    img = img.reshape((img.shape[0]*img.shape[1], img.shape[2]))


    # computing the PCA

    mean = np.mean(img, axis=0)
    img_centered = img - mean

    covariance_matrix = np.cov(img_centered.T)


    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]



    principal_components = np.dot(img_centered, sorted_eigenvectors)


    pca1 = principal_components[:, 0]
    pca1try=pca1.reshape((size1, size2))
    showimg(pca1try,'PCA1_without_normalizing.jpeg')
    
    pca1 = normalize_array(pca1.reshape((size1, size2)),g)
    showimg(pca1,'PCA1.jpeg')


    wg=wi
    matrix=compute_glcm_features(pca1, 0, [wg],g,d1,d2) #computiong feature matrix

 
    nmatrix = np.squeeze(matrix)




    # applying kmeans to cluster the data according to the features extracted
    from sklearn.cluster import KMeans
    import numpy as np

    X=nmatrix[0:4, :].T

    xn=X[:, 0:4]
 
   

    kmeans2 = KMeans(n_clusters=givenk, random_state=0)
    kmeans2.fit(X)
    
    
    cluster_labels2 = kmeans2.labels_

    # Reshape the cluster assignments back to a 2D array
    cluster_labels_2d2 = np.reshape(cluster_labels2, (pca1.shape[0]-wg+1,pca1.shape[1]-wg+1))

    # Define your own cluster labels based on the K-means cluster assignments
    my_cluster_labels2 = np.zeros_like(cluster_labels2)
    for i in range (0,givenk):
         my_cluster_labels2[cluster_labels2 == i] = (max/givenk)*i

    output2= np.reshape(my_cluster_labels2, (pca1.shape[0]-wg+1,pca1.shape[1]-wg+1))

    ishow(pca1,output2)
    



   

    

    
    

#mainf(1000,7,4,64,0,0,100,100,'/Users/sdl/Desktop/GNR_project/data.tif',1,1)