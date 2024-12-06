def hello():
    """EXP2







PCA











import numpy as np



import matplotlib.pyplot as plt



X = np.array([[17,7,16,19],



       [12,5,9,21]])



X_transposed = X.T



print("Step 2: Transposed Data:")



print(X_transposed)



X_mean = np.mean(X_transposed, axis=0)



X_centered = X_transposed - X_mean



print("\nStep 3: Centered Data (Subtract Mean):")



print(X_centered)



cov_matrix = np.cov(X_centered, rowvar=False)



print("\nStep 4: Covariance Matrix:")



print(cov_matrix)



eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)



print("\nStep 5: Eigenvalues:")



print(eigenvalues)



print("\nStep 5: Eigenvectors:")



print(eigenvectors)



sorted_indices = np.argsort(eigenvalues)[::-1]



sorted_eigenvalues = eigenvalues[sorted_indices]



sorted_eigenvectors = eigenvectors[:, sorted_indices]



print("\nStep 6: Sorted Eigenvalues:")



print(sorted_eigenvalues)



print("\nStep 6: Sorted Eigenvectors:")



print(sorted_eigenvectors)



X_pca_manual = np.dot(X_centered, sorted_eigenvectors)



print("\nStep 7: Projected Data (Manual PCA):")



print(X_pca_manual)



plt.figure(figsize=(8, 6))



plt.scatter(X_transposed[:, 0], X_transposed[:, 1], color='blue', label='Original Data')



plt.scatter(X_centered[:, 0], X_centered[:, 1], color='red', label='Centered Data')



plt.axhline(0, color='black', linewidth=0.8, linestyle='--')



plt.axvline(0, color='black', linewidth=0.8, linestyle='--')



plt.xlabel('Feature 1')



plt.ylabel('Feature 2')



plt.title('PCA Transformation with X and Y Axes')



plt.legend()



plt.grid(True)



plt.show()















































SVD











import numpy as np



A=np.array([[3,0],[4,5]])



U,sigma,VT=np.linalg.svd(A)



sigma_matrix = np.diag(sigma)



print("Matrix A in SVD form: ")



print("U Matrix: ")



print(U)



print("\n Sigma Matrix: ")



print(sigma_matrix)



print("\nVT Matrix: ")



print(VT)



print("\n A=[U][sigma_matric][VT] form:")



print("\n[U]")



print(U)



print("\n[sigma]")



print(sigma_matrix)



print("\n[VT]")



print(VT)



































LDA







import numpy as np



import matplotlib.pyplot as plt



X1 = np.array([[4, 2], [2, 4], [2, 3], [3, 6], [4, 4]])



X2 = np.array([[9, 10], [6, 8], [9, 5], [8, 7], [10, 8]])



mean1 = np.mean(X1, axis=0)



mean2 = np.mean(X2, axis=0)



print("Mean vector for class 1:", mean1)



print("Mean vector for class 2:", mean2)



S1 = np.cov(X1.T)



S2 = np.cov(X2.T)



Sw = S1 + S2



print("\nS1 (Covariance matrix for class 1):\n", S1)



print("\nS2 (Covariance matrix for class 2):\n", S2)



print("\nSw (Within-class scatter matrix):\n", Sw)



mean_diff = (mean1 - mean2).reshape(2, 1)



Sb = mean_diff @ mean_diff.T



print("\nSb (Between-class scatter matrix):\n", Sb)



eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(Sw) @ Sb)



print("\nEigenvalues:", eigenvalues)



print("\nEigenvectors:\n", eigenvectors)



W = eigenvectors[:, np.argmax(eigenvalues)]



W_normalized = W / W[0]



print("\nNormalized projection vector W:", W_normalized)



Y1 = X1 @ W_normalized



Y2 = X2 @ W_normalized



print("\nProjected data for class 1:", Y1)



print("Projected data for class 2:", Y2)



plt.figure(figsize=(12, 5))



plt.subplot(121)



plt.scatter(X1[:, 0], X1[:, 1], label='Class 1')



plt.scatter(X2[:, 0], X2[:, 1], label='Class 2')



plt.title('Before applying LDA')



plt.xlabel('x1')



plt.ylabel('x2')



plt.legend()



plt.subplot(122)



plt.scatter(Y1, np.zeros_like(Y1), label='Class 1')



plt.scatter(Y2, np.zeros_like(Y2), label='Class 2')



plt.title('After applying LDA')



plt.xlabel('Projection axis')



plt.yticks([])



plt.legend()



plt.tight_layout()



plt.show()





















































EXP3







KNN















from math import sqrt



from collections import Counter



import pandas as pd







# Dataset in the order given



data = [



  [5.3, 3.7, 'Setosa'],



  [5.1, 3.8, 'Setosa'],



  [7.2, 3.0, 'Virginica'],



  [5.4, 3.4, 'Setosa'],



  [5.1, 3.3, 'Setosa'],"""