using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class toggleCamera : MonoBehaviour
{
    public Camera cam1;
    public Camera cam2;
    int x;

    public void SwitchCam(){
        x += 1;
        Debug.Log(x);
        if(x % 2 == 0){
            cam1.enabled = true;
            cam2.enabled = false;
        } else{
            cam1.enabled = false;
            cam2.enabled = true;
        }
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.Space)) {
            SwitchCam();
        }
    }

}
