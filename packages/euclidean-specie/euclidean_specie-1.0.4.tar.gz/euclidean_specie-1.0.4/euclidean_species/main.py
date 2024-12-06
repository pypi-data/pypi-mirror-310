def hello():
    """EX 2: Use feature selection/extraction method to perform
    dimensionality reduction
    Principal Component Analysis(PCA) :"""

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
