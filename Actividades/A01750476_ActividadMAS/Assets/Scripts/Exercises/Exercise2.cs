using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Exercise2 : MonoBehaviour
{
    // Initialize variables
    [SerializeField] MatrixOperator Operator;
    [SerializeField] GameObject centerObject;
    [SerializeField] GameObject centroidObject;
    [SerializeField] float a;
    [SerializeField] float angle;
    [SerializeField] List<GameObject> vertObjects;

    private Vector3 center;
    private Vector3 centroidPos;
    private float h;
    // Start is called before the first frame update
    void Start()
    {
        // Get height
        h = Mathf.Sqrt(2 * a / 3);
        // Get center and centroid
        center = centerObject.transform.localPosition;
        centroidPos = new Vector3(center.x, h / 2, center.z);
        centroidObject.transform.localPosition = centroidPos;
        // Set original positions
        vertObjects[0].transform.localPosition = new Vector3(center.x + a / 2, center.y, center.z + a / 2);
        vertObjects[1].transform.localPosition = new Vector3(center.x - a / 2, center.y, center.z + a / 2);
        vertObjects[2].transform.localPosition = new Vector3(center.x + a / 2, center.y, center.z - a / 2);
        vertObjects[3].transform.localPosition = new Vector3(center.x - a / 2, center.y, center.z - a / 2);
        vertObjects[4].transform.localPosition = new Vector3(center.x, h, center.z);
        // Set new positions
        vertObjects[0].transform.localPosition = rotatePoint(vertObjects[0].transform.localPosition, centroidPos);
        vertObjects[1].transform.localPosition = rotatePoint(vertObjects[1].transform.localPosition, centroidPos);
        vertObjects[2].transform.localPosition = rotatePoint(vertObjects[2].transform.localPosition, centroidPos);
        vertObjects[3].transform.localPosition = rotatePoint(vertObjects[3].transform.localPosition, centroidPos);
        vertObjects[4].transform.localPosition = rotatePoint(vertObjects[4].transform.localPosition, centroidPos);
        centerObject.transform.localPosition = rotatePoint(centerObject.transform.localPosition, centroidPos);
        centroidObject.transform.localPosition = rotatePoint(centroidObject.transform.localPosition, centroidPos);
    }

    // Rotate a point
    Vector3 rotatePoint(Vector3 pointPos, Vector3 pivotPos) {
        // Translate to pivot
        float[,] translationMatrix1 = Operator.translationMatrix(pivotPos.x, pivotPos.y, pivotPos.z);
        float[,] temp = Operator.multiplyMatrices(translationMatrix1, Operator.vectorToArray(pointPos));
        // Rotate
        float[,] rotationMatrix = Operator.yRotationMatrix(angle);
        temp = Operator.multiplyMatrices(rotationMatrix, temp);
        // Retranslate from pivot
        float[,] translationMatrix2 = Operator.translationMatrix(pointPos.x, pointPos.y, pointPos.z);
        temp = Operator.multiplyMatrices(translationMatrix2, temp);

        return Operator.arrayToVec(temp);
    }

    // Update is called once per frame
    void Update()
    {

    }
},...........ñpl