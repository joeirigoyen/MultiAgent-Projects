using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destroyer : MonoBehaviour
{

    // Update is called once per frame
    void Update()
    {
        Destroy(this, 6.0f);
    }
}
