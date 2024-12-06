def ex2():
    """EX 2: Use feature selection/extraction method to perform dimensionality reduction Principal Component Analysis(PCA) :"""

    ## Principal Component Analysis (PCA)
    import numpy as np
    import matplotlib.pyplot as plt

    # 1. Creating Arrays
    x = np.array([4, 8, 13, 7])
    y = np.array([11, 4, 5, 14])
    # 2. Plotting the Original Data
    plt.scatter(x, y, color="blue", label="Original Data")
    plt.title("Original Data")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.legend()
    plt.show()
    # 3. Calculating the Mean
    xm = np.mean(x)
    ym = np.mean(y)
    print("Mean of x:", xm, "Mean of y:", ym)
    # 4. Calculating the Covariance Matrix
    covxy = np.cov(x, y)
    print("Covariance Matrix:\n", covxy)
    # 5. Eigenvalues and Eigenvectors
    w, v = np.linalg.eig(covxy)
    print("Eigenvalues:\n", w)
    print("Eigenvectors:\n", v)
    # 6. Transposing the Eigenvector Matrix
    vt = v.transpose()
    print("Transposed Eigenvector Matrix:\n", vt)
    # 7. Splitting the Eigenvector Matrix
    e1, e2 = np.hsplit(vt, 2)
    print("First Eigenvector (e1):\n", e1)
    print("Second Eigenvector (e2):\n", e2)
    # 8. Centering the Data
    x = x - xm
    y = y - ym
    # 9. Stacking the Centered Data
    data = np.stack((x.T, y.T), axis=0)
    print("Centered Data:\n", data)
    # 10. Projecting Data onto Eigenvectors
    p1 = e1 * data
    print("Projection onto e1:\n", p1)
    p2 = e2 * data
    print("Projection onto e2:\n", p2)
    # 11. Plotting the Projections
    plt.scatter(p1, p2, color="red", label="Projected Data")
    plt.title("Data Projected onto Principal Components")
    plt.xlabel("Projection on e1")
    plt.ylabel("Projection on e2")
    plt.legend()
    plt.show()

    # Singular value decomposition (SVD) :
    import numpy as np

    A = np.array([[3, 0], [4, 5]])
    U, Sigma, VT = np.linalg.svd(A)
    Sigma_matrix = np.diag(Sigma)
    print("Matrix A in SVD form:")
    print("U matrix:")
    print(U)
    print("\nSigma matrix:")
    print(Sigma_matrix)
    print("\nVT matrix:")
    print(VT)
    # Display the combination in order without multiplication
    print("\nA = [U][Sigma][V^T] form:")
    # Print each component in order
    print("[U] ")
    print(U)
    print("\n[Sigma] ")
    print(Sigma_matrix)
    print("\n[V^T] ")
    print(VT)

    # Linear discriminant analysis (LDA):
    import numpy as np
    import matplotlib.pyplot as plt
    # Define the data
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
    # Calculate between-class scatter matrix
    mean_diƯ = (mean1 - mean2).reshape(2, 1)
    Sb = mean_diƯ @ mean_diƯ.T
    print("\nSb (Between-class scatter matrix):\n", Sb)
    # Calculate eigenvectors and eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(Sw) @ Sb)
    print("\nEigenvalues:", eigenvalues)
    print("\nEigenvectors:\n", eigenvectors)
    # Select the eigenvector with the largest eigenvalue and normalize
    W = eigenvectors[:, np.argmax(eigenvalues)]
    W_normalized = W / W[0] # Normalize to make the first element 1, similar to the image
    print("\nNormalized projection vector W:", W_normalized) 
    # Project the data using normalized W
    Y1 = X1 @ W_normalized
    Y2 = X2 @ W_normalized
    print("\nProjected data for class 1:", Y1)
    print("Projected data for class 2:", Y2)
    # Plotting
    plt.figure(figsize=(12, 5))
    # Before LDA
    plt.subplot(121)
    plt.scatter(X1[:, 0], X1[:, 1], label='Class 1')
    plt.scatter(X2[:, 0], X2[:, 1], label='Class 2')
    plt.title('Before applying LDA')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    # After LDA
    plt.subplot(122)
    plt.scatter(Y1, np.zeros_like(Y1), label='Class 1')
    plt.scatter(Y2, np.zeros_like(Y2), label='Class 2')
    plt.title('After applying LDA')
    plt.xlabel('Projection axis')
    plt.yticks([])
    plt.legend()
    plt.tight_layout()
    plt.show() 