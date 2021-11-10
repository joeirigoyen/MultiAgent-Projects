using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MatrixOperator : MonoBehaviour
{

    // Convert a position vector into a 4x1 array
    public float[,] vectorToArray(Vector3 v) {
        return new float[4,1] {{v.x}, {v.y}, {v.z}, {1}};
    }

    // Get a scale matrix given the amount to be applied to each component
    public float[,] scaleMatrix(float sx, float sy, float sz)
    {
        return new float[4,4] {{sx, 0, 0, 0}, {0, sy, 0, 0}, {0, 0, sz, 0}, {0, 0, 0, 1}};
    }

    // Get a translation matrix given the amount to be applied to each component
    public float[,] translationMatrix(float tx, float ty, float tz)
    {
        return new float[4,4] {{1, 0, 0, tx}, {0, 1, 0, ty}, {0, 0, 1, tz}, {0, 0, 0, 1}};
    }

    // Get a rotation matrix using the x axis
    public float[,] xRotationMatrix(float angle) {
        float radAngle = angle * Mathf.Deg2Rad;
        return new float[4,4] {{1, 0, 0, 0}, {0, Mathf.Cos(radAngle), -Mathf.Sin(radAngle), 0}, {0, Mathf.Sin(radAngle), Mathf.Cos(radAngle), 0}, {0, 0, 0, 1}};
    }

    // Rescale a 3D point given the amount to be applied to each component
    public float[,] rescalePoint3D(float[,] p, float sx, float sy, float sz) 
    {
        float[,] sm = scaleMatrix(sx, sy, sz);
        return multiplyMatrices(sm, p);
    }

    // Return the result of multiplying two matrices
    public float[,] multiplyMatrices(float[,] A, float[,] B) 
    {
        int rowsA = A.GetLength(0);
        int colsA = A.GetLength(1);
        int rowsB = B.GetLength(0);
        int colsB = B.GetLength(1);
        if (colsA == rowsB) {
            float[,] product = new float[rowsA, colsB];  
            // looping through matrix 1 rows  
            for (int i = 0; i < rowsA; i++) {  
                // for each matrix 1 row, loop through matrix 2 columns  
                for (int j = 0; j < colsB; j++) {  
                // loop through matrix 1 columns to calculate the dot product  
                    for (int k = 0; k < colsA; k++) {  
                        product[i, j] += A[i, k] * B[k, j];  
                    }  
                }  
            }
            return product;  
        } else {
            return new float[,] {};
        }
    }

    public string displayArr(float[,] arr) 
    {
        string arrString = "";
        for (int i = 0; i < arr.GetLength(0); i++) {
            for (int j = 0; j < arr.GetLength(1); j++) {
                arrString += string.Format("{0} ", arr[i, j]);
            }
        }
        return arrString;
    }
}
