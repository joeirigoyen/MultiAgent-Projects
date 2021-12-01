using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRotator : MonoBehaviour
{
    // Speed in which the camara will rotate around the city
    public float camera_speed;
    private int presses;
    private bool rotate;
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R)) {
            presses++;
        }
        if (presses % 2 == 0) {
            transform.Rotate(0, camera_speed * Time.deltaTime, 0);
        }
    }
}
