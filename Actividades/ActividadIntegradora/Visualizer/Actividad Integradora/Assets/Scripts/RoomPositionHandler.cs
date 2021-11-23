using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoomPositionHandler : MonoBehaviour
{
    [SerializeField] GameObject LeftWall, RightWall, BackWall, FrontWall, Roof, Floor, Spotlight, Cam;

    // Update is called once per frame
    void Update()
    {
        LeftWall.transform.localPosition = new Vector3(Floor.transform.localPosition.x - 11, Floor.transform.localPosition.y + 5, Floor.transform.localPosition.z);
        RightWall.transform.localPosition = new Vector3(Floor.transform.localPosition.x + 11, Floor.transform.localPosition.y + 5, Floor.transform.localPosition.z);
        BackWall.transform.localPosition = new Vector3(Floor.transform.localPosition.x, Floor.transform.localPosition.y + 5, Floor.transform.localPosition.z + 12);
        FrontWall.transform.localPosition = new Vector3(Floor.transform.localPosition.x, Floor.transform.localPosition.y + 5, Floor.transform.localPosition.z + 12);
        Roof.transform.localPosition = new Vector3(Floor.transform.localPosition.x, Floor.transform.localPosition.y + 20, Floor.transform.localPosition.z - 4.5f);
        Spotlight.transform.localPosition = new Vector3(Floor.transform.localPosition.x, Floor.transform.localPosition.y + 21.52f, Floor.transform.localPosition.z);
        Cam.transform.localPosition = new Vector3(Floor.transform.localPosition.x + 6.6f, Floor.transform.localPosition.y + 13.44f, Floor.transform.localPosition.z - 12.06f);
    }
}
