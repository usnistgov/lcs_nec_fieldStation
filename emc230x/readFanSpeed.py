import smbus2
import sys
import json
import os
import time


# Registers for reading PWM duty cycle
PWM_FAN1_REG = 0x30
PWM_FAN2_REG = 0x40

# Registers for reading fan speeds
TACH_FAN1_MSB = 0x3E
TACH_FAN1_LSB = 0x3F
TACH_FAN2_MSB = 0x4E
TACH_FAN2_LSB = 0x4F

# Fan pulses per revolution (from CFM-25CF datasheet)
PULSES_PER_REV = 2

def read_fan_duty_cycle(bus, i2c_addr, num_fans):
    """Read PWM duty cycle (0-100%) for 1 or 2 fans."""
    duty_cycle_fan1 = bus.read_byte_data(i2c_addr, PWM_FAN1_REG)
    duty_cycle_fan2 = bus.read_byte_data(i2c_addr, PWM_FAN2_REG) if num_fans == 2 else None

    return (duty_cycle_fan1 / 255) * 100, (duty_cycle_fan2 / 255) * 100 if duty_cycle_fan2 is not None else None

def read_fan_rpm(bus, i2c_addr, num_fans):
    """Read RPM values for 1 or 2 fans using the tachometer registers."""
    def get_rpm(msb_reg, lsb_reg):
        msb = bus.read_byte_data(i2c_addr, msb_reg)
        lsb = bus.read_byte_data(i2c_addr, lsb_reg)
        tach_count = (msb << 5) | (lsb >> 3)  # 13-bit value

        if tach_count == 0 or tach_count == 0x1FFF:  # Invalid reading (fan stalled)
            return None

        return (3932160 * PULSES_PER_REV) // tach_count  # Corrected RPM formula

    # Read Fan 1 speed
    rpm1 = get_rpm(TACH_FAN1_MSB, TACH_FAN1_LSB)

    # Read Fan 2 speed if controlling 2 fans
    rpm2 = get_rpm(TACH_FAN2_MSB, TACH_FAN2_LSB) if num_fans == 2 else None

    return rpm1, rpm2

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 read_fan_status.py <I2C_ADDRESS> <NUM_FANS> <MQTT_TOPIC>")
        print("Example: python3 read_fan_status.py 0x2F 2 st/raw/nist/... ")
        sys.exit(1)

    try:
        i2c_addr = int(sys.argv[1], 16)  # Convert hex string (e.g., "0x2F") to int
        num_fans = int(sys.argv[2])  # Number of fans (1 or 2)
        MQTT_TOPIC = str(sys.argv[3])

        if num_fans not in [1, 2]:
            raise ValueError("Number of fans must be 1 or 2.")

        # Initialize I2C bus (Raspberry Pi typically uses bus 1)
        bus = smbus2.SMBus(1)

        # Read fan duty cycles
        duty_cycle1, duty_cycle2 = read_fan_duty_cycle(bus, i2c_addr, num_fans)

        # Read fan speeds
                rpm1, rpm2 = read_fan_rpm(bus, i2c_addr, num_fans)

        # Construct JSON output
        fan_data = {
            "i2c_address": hex(i2c_addr),
            "fan_1_duty_cycle": round(duty_cycle1, 1),
            "fan_2_duty_cycle": round(duty_cycle2, 1) if duty_cycle2 is not None else "N/A",
            "fan_1_rpm": rpm1 if rpm1 is not None else "N/A",
            "fan_2_rpm": rpm2 if rpm2 is not None else "N/A",
            "epoch": int(time.time()),
            "topic": MQTT_TOPIC,
            "m_sensor_type":"emc2303",
            "stn_id":os.getenv("STN_NAME"),
            "stn_loc":os.getenv("STN_LOC"),
            "pkt_type":"emc2303"
        }

        # Print JSON output
        print(json.dumps(fan_data))

    except ValueError:
        print("Error: Invalid input. Please enter a valid I2C address (e.g., 0x2F) and number of fans (1 or 2).")

    finally:
        bus.close()
