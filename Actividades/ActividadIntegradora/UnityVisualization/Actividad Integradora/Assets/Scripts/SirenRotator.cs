using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SirenRotator : MonoBehaviour
{
    [SerializeField] int rpm;

    // Update is called once per frame
    void Update()
    {
        transform.Rotate(0, 0, 6.0f * rpm * Time.deltaTime);
    }
}
