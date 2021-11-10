using System.Collections;
using System.Collections.Generic;
using static System.Math;
using UnityEngine;

public class VectorOperator : MonoBehaviour
{
    // Get cubes
    [SerializeField] Transform cubeA;
    [SerializeField] Transform cubeB;
    [SerializeField] Transform origin;

    private Vector3 originVec;
    private Vector3 cubeAPos;
    private Vector3 cubeBPos;
    private Vector3 vecA;
    private Vector3 vecB;
    private Vector3 cProduct;
    private float angle;

    // Update is called once per frame
    void Update()
    {
        originVec = origin.position;
        cubeAPos = cubeA.position;
        cubeBPos = cubeB.position;
        vecA = cubeAPos - originVec;
        vecB = cubeBPos - originVec;
        cProduct = crossProduct(vecA, vecB);
        angle = angleBetween(vecA, vecB);
        Debug.Log("Ángulo entre cubos: " + angle);
        /* Debug.Log("Cross product is: " + cProduct); */
        Debug.DrawLine(originVec, cProduct, Color.yellow);
        Debug.DrawLine(originVec, vecA, Color.red);
        Debug.DrawLine(originVec, vecB, Color.blue);
    }

    // Get magnitude of a vector
    float getMagnitude(Vector3 V) 
    {
        double sum = Pow(V.x, 2) + Pow(V.y, 2) + Pow(V.z, 2);
        return Mathf.Sqrt((float)sum);
    }

    // Normalize a vector
    Vector3 normalizeVector(Vector3 V)
    {
        float mag = getMagnitude(V);
        return new Vector3(V.x / mag, V.y / mag, V.z / mag);
    }

    // Get the dot product of two vectors
    float dotProduct(Vector3 A, Vector3 B)
    {
        return A.x * B.x + A.y * B.y + A.z * B.z;
    }

    // Get angle between two vectors
    float angleBetween(Vector3 A, Vector3 B)
    {
        Vector3 normA = normalizeVector(A);
        Vector3 normB = normalizeVector(B);
        return Mathf.Acos(dotProduct(normA, normB)) * Mathf.Rad2Deg;
    }

    Vector3 crossProduct(Vector3 A, Vector3 B) 
    {
        float x = A.y * B.z - B.y * A.z;
        float y = (A.x * B.z - B.y * A.z) * -1;
        float z = A.x * B.y - B.x * A.y;
        return new Vector3(x, y, z);
    }

}
