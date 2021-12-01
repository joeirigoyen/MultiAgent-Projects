using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightCycler : MonoBehaviour
{
    [SerializeField] Color goColor;
    [SerializeField] Color stopColor;
    [SerializeField] public bool state;

    // Update is called once per frame
    void Update()
    {
        if (state) {
            transform.GetComponent<Light>().color = goColor;
        } else {
            transform.GetComponent<Light>().color = stopColor;
        }
    }
}
