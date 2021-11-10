using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectRotator : MonoBehaviour
{

    [SerializeField] Transform pivot;
    [SerializeField] Transform target;
    [SerializeField] float angle;

    private float angleInRads;

    // Update is called once per frame
    void Update()
    {
        angleInRads = angle * Mathf.Deg2Rad;
        Vector3 newPosition = rotateY(angleInRads, target.position, pivot.position);
        target.position.Set(newPosition.x, newPosition.y, newPosition.z);
    }

    // Rotate around Y axis
    Vector3 rotateY(float angle, Vector3 currentPosition, Vector3 pivotPosition)
    {
        float cosTheta = Mathf.Cos(angle);
        float sinTheta = Mathf.Sin(angle);
        Vector3 result = new Vector3(pivotPosition.x * cosTheta, currentPosition.y, pivotPosition.z * sinTheta);
        Debug.Log("New position should be: " + result);
        return result;
    }

}
