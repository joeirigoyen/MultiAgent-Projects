using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Exercise1 : MonoBehaviour
{
    // Exercise 1
    [SerializeField] MatrixOperator Operator;
    [SerializeField] float cRotation;
    [SerializeField] float scaleX;
    [SerializeField] float scaleY;
    [SerializeField] float scaleZ;
    [SerializeField] Transform pointA;
    [SerializeField] Transform pointB;
    [SerializeField] Transform pointC;
    [SerializeField] Transform pointQ;

    // Start is called before the first frame update
    void Start()
    {
        // Part 1
        // Rescale point A by 1.43 on each axis
        rescalePoint(pointQ, scaleX, scaleY, scaleZ);
        // Translate using B position
        translatePoint(pointQ, pointB);
        // Part 2
        // Rotate C by 45° 
        rotatePoint(pointC, pointQ);
    }   

    // Rescale a point
    void rescalePoint(Transform point, float scaleX, float scaleY, float scaleZ) 
    {
        float[,] scaleMatrix = Operator.scaleMatrix(scaleX, scaleY, scaleZ);
        float[,] result = Operator.multiplyMatrices(scaleMatrix, Operator.vectorToArray(point.localScale));
        Vector3 newScale = Operator.arrayToVec(result);
        point.localScale -= point.localScale;
        point.localScale += newScale;
    }

    // Translate a point
    void translatePoint(Transform point, Transform target)
    {
        float[,] transMatrix = Operator.translationMatrix(target.localPosition.x, target.localPosition.y, target.localPosition.z);
        float[,] result = Operator.multiplyMatrices(transMatrix, Operator.vectorToArray(point.localPosition));
        Vector3 newPos = Operator.arrayToVec(result);
        point.localPosition -= point.localPosition;
        point.localPosition += newPos;
    }

    // Rotate a point
    void rotatePoint(Transform point, Transform pivot) 
    {
        Vector3 tempPos = point.localPosition;
        // Translate to pivot
        float[,] transMat = Operator.translationMatrix(pivot.localPosition.x, pivot.localPosition.y, pivot.localPosition.z);
        float[,] transResult = Operator.multiplyMatrices(transMat, Operator.vectorToArray(point.localPosition));
        tempPos = Operator.arrayToVec(transResult);
        // Rotate
        float[,] rotMat = Operator.xRotationMatrix(cRotation);
        float[,] rotResult = Operator.multiplyMatrices(rotMat, Operator.vectorToArray(tempPos));
        tempPos = Operator.arrayToVec(rotResult);
        // Translate to original position
        float[,] transMat2 = Operator.translationMatrix(point.localPosition.x, point.localPosition.y, point.localPosition.z);
        float[,] transResult2 = Operator.multiplyMatrices(transMat2, Operator.vectorToArray(tempPos));
        tempPos = Operator.arrayToVec(transResult2);
        // Assign values
        point.localPosition -= point.localPosition;
        point.localPosition += tempPos;
    }
}