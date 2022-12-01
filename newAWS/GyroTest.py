from mpu6050 import mpu6050


# get the angle of the sensor
def GetGyro():
    mpu = mpu6050(0x68)
    # gets all three angle dimentions
    data = mpu.get_accel_data()
    data_string = data['y']
    return data_string


def main():
    angle = GetGyro()
    print("Test Data: " + str(angle))


if __name__ == "__main__":
    main()
