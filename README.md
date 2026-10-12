# Self-Balancing Dancing Segway

**Kennard Mah**

Access to video and pictures:

https://drive.google.com/drive/folders/1i2_h7K0nHX6o55lKXWxxARlcaVrOX2x7?usp=sharing

## Brief summary of files and content

| File | Description |
| --- | --- |
| **[Challenge1.py](challenges/Challenge1.py)** | Utilise built-in microphone to develop a beat detection code<ul><li>Combine beat detection with loudness</li><li>Light up LEDs synchronised with music</li></ul> |
| **[Challenge2.py](challenges/Challenge2.py)** | Control speed and direction of motors using IMU<ul><li>Control speed and direction with potentiometer</li><li>Combine with ability to derive pitch and roll angles from IMU measurements</li><li>Display each motor on OLED display</li></ul> |
| **[Challenge3.py](challenges/Challenge3.py)** | Implement PID controller for speed of motors<ul><li>Demonstrate PID control algorithm is functioning</li><li>Apply pressure to increase friction (video)</li></ul> |
| **[Challenge4.py](challenges/Challenge4.py)** | Dancing Segway (w/o balancing)<ul><li>Attach stabilisers to Segway</li><li>Develop dancing code with combination of beat detection from Challenge1.py</li></ul> |
| [Challenge4Moves.py](challenges/Challenge4Moves.py) | Dance choreography file |
| **[Challenge5.py](challenges/Challenge5.py)** | Self-balancing the Segway<ul><li>Implement a PID algorithm using the pitch angle as the set-point variable and control the motors to maintain the pitch angle to be zero (post-calibration)</li></ul> |
| [Challenge5PID.py](challenges/Challenge5PID.py) | PID controller for challenge 5 |
| [Challenge5Motor.py](challenges/Challenge5Motor.py) | Motor function for challenge 5 |
| [Challenges.pdf](challenges/Challenges.pdf) | <ul><li>Brief for each challenges and criteria</li></ul> |

## Standard modules

We use the following standard modules:

- `boot.py`
- `drive.py`
- `font.py`
- `main.py`
- `mic.py`
- `motor.py`
- `mpu6050.py`
- `oled_938.py`
- `pybench.py`
- `user.py`
