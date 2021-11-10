using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriangleMaker : MonoBehaviour
{
    // Define geometry
    Vector3[] vertices;
    int[] topology;
    // Start is called before the first frame update
    void Start()
    {
        Mesh mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;
        vertices = new Vector3[3] {new Vector3(0, 0, 0), new Vector3(2, 5, 6), new Vector3(5, 0, 0)};
        topology = new int[3];

        topology[0] = 0;
        topology[1] = 1;
        topology[2] = 2;

        mesh.vertices = vertices;
        mesh.triangles = topology;

        mesh.RecalculateNormals();
    }


    // Update is called once per frame
    void Update()
    {
        
    }
}