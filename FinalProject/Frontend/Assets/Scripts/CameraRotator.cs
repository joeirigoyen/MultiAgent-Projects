using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRotator : MonoBehaviour
{
    // speed in wich the camara will rotate the city
    public float camera_speed;
    void Update()
    {
        transform.Rotate(0, camera_speed * Time.deltaTime, 0);
    }
}
