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
    private Vector3 originalCPosition;
    private float[,] scaleMatrix;
    private float[,] transMatrixA;
    private float[,] transMatrixC;
    private float[,] rotationMatrixC;
    private float[,] scaleMatResult;
    private float[,] transMatResultA;
    private float[,] transMatResultC;
    private float[,] rotationMatrixResultC;

    // Start is called before the first frame update
    void Start()
    {
        // Rescale point A
        scaleMatrix = Operator.scaleMatrix(scaleX, scaleY, scaleZ);
        scaleMatResult = Operator.multiplyMatrices(scaleMatrix, Operator.vectorToArray(pointA.localScale));
        // Translate point A
        transMatrixA = Operator.translationMatrix(pointB.localPosition.x, pointB.localPosition.y, pointB.localPosition.z);
        transMatResultA = Operator.multiplyMatrices(transMatrixA, Operator.vectorToArray(pointA.localPosition));
        // Get original position of point C
        originalCPosition = pointC.localPosition;
    }

    // Update is called once per frame
    void Update()
    {
        // Rescale point A
        rescalePoint(pointA, scaleMatResult);
        Debug.Log("Point A scale: " + pointA.localScale);
        // Translate point A
        translatePoint(pointA, transMatResultA);
        Debug.Log("Point A position: " + pointA.localPosition);
        // Rotate point C
        rotationMatrixC = Operator.xRotationMatrix(cRotation);
        rotationMatrixResultC = Operator.multiplyMatrices(rotationMatrixC, Operator.vectorToArray(pointA.localPosition));
        rotatePoint(pointC, rotationMatrixResultC);
    }

    // Rescale a point
    void rescalePoint(Transform point, float[,] scaleVec) 
    {
        point.localScale -= point.localScale;
        point.localScale += new Vector3(scaleVec[0,0], scaleVec[1,0], scaleVec[2,0]);
    }

    // Translate a point
    void translatePoint(Transform point, float[,] transVec)
    {
        point.localPosition -= point.localPosition;
        point.localPosition += new Vector3(transVec[0,0], transVec[1,0], transVec[2,0]);
    }

    // Rotate a point
    void rotatePoint(Transform point, float[,] rotateVec) 
    {
        point.localPosition -= point.localPosition;
        point.localPosition += new Vector3(rotateVec[0,0], rotateVec[1,0], rotateVec[2,0]) + originalCPosition;
    }
}