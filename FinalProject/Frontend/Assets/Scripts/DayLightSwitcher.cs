using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DayLightSwitcher : MonoBehaviour
{
    [SerializeField] Color dayColor;
    [SerializeField] Color nightColor;
    [SerializeField] float updateTime;
    [SerializeField] Transform dayTransform;
    [SerializeField] Transform nightTransform;
    private Color currentColor;
    private int presses = 0;
    private float timer = 0;

    // Start
    void Start() {
        currentColor = nightColor;
    }

    // Update is called once per frame
    void Update()
    {
        transform.GetComponent<Light>().color = currentColor;
        if (Input.GetMouseButtonDown(0)) {
            Debug.Log("Key pressed.");
            timer = 0;
            presses++;
        }
        if (presses % 2 == 0) {
            if (timer < updateTime) {
                Color lerped = Color.Lerp(dayColor, nightColor, 1.0f - timer / updateTime);
                Quaternion lerpedRot = Quaternion.Lerp(dayTransform.localRotation, nightTransform.localRotation, 1.0f - timer / updateTime);
                currentColor = lerped;
                transform.localRotation = lerpedRot;
                timer += Time.deltaTime;
            }
        } else {
            if (timer < updateTime) {
                Color lerped = Color.Lerp(nightColor, dayColor, 1.0f - timer / updateTime);
                Quaternion lerpedRot = Quaternion.Lerp(nightTransform.localRotation, dayTransform.localRotation, 1.0f - timer / updateTime);
                currentColor = lerped;
                transform.localRotation = lerpedRot;
                timer += Time.deltaTime;
            }
        }
    }



}
