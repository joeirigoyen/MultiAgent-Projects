using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VectorDebugger : MonoBehaviour
{
    [SerializeField] int size;

    // Update is called once per frame
    void Update()
    {
        Debug.DrawLine(Vector3.zero, new Vector3(size, 0, 0), Color.red);
        Debug.DrawLine(Vector3.zero, new Vector3(0, size, 0), Color.green);
        Debug.DrawLine(Vector3.zero, new Vector3(0, 0, size), Color.blue);
    }
}
