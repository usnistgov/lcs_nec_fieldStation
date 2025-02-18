import smbus2
import sys
import time
import json

# Registers for Fan 1 and Fan 2
PWM_FAN1_REG = 0x30      # PWM control register for Fan 1
PWM_FAN2_REG = 0x40      # PWM control register for Fan 2
TACH_FAN1_MSB = 0x3E     # Fan 1 Tachometer MSB
TACH_FAN1_LSB = 0x3F     # Fan 1 Tachometer LSB
TACH_FAN2_MSB = 0x4E     # Fan 2 Tachometer MSB
TACH_FAN2_LSB = 0x4F     # Fan 2 Tachometer LSB

# Fan pulses per revolution (from CFM-25CF datasheet)
PULSES_PER_REV = 2  

def set_fan_speed(bus, i2c_addr, percentage, num_fans):
    """Set PWM duty cycle for 1 or 2 fans using percentage (0-100%)."""
    percentage = max(0, min(100, percentage))  # Clamp value to valid range
    duty_cycle = int((percentage / 100) * 255)  # Convert to 0-255 scale

    # Set Fan 1 speed
    bus.write_byte_data(i2c_addr, PWM_FAN1_REG, duty_cycle)

    # Set Fan 2 speed if controlling 2 fans
    if num_fans == 2:
        bus.write_byte_data(i2c_addr, PWM_FAN2_REG, duty_cycle)

    return duty_cycle  # Return the duty cycle value for JSON output

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
        print("Usage: python3 set_fan_speed.py <I2C_ADDRESS> <PERCENTAGE> <NUM_FANS>")
        print("Example: python3 set_fan_speed.py 0x2F 75 2")
        sys.exit(1)

    try:
        i2c_addr = int(sys.argv[1], 16)  # Convert hex string (e.g., "0x2F") to int
        percentage = float(sys.argv[2])  # Allow decimal inputs (e.g., 50.5)
        num_fans = int(sys.argv[3])  # Number of fans (1 or 2)

        if num_fans not in [1, 2]:
            raise ValueError("Number of fans must be 1 or 2.")

        # Initialize I2C bus (Raspberry Pi typically uses bus 1)
        bus = smbus2.SMBus(1)

        # Set fan speed
        duty_cycle = set_fan_speed(bus, i2c_addr, percentage, num_fans)

        # Wait 3 seconds to allow fan speed to stabilize
        time.sleep(10)

        # Read fan speeds
        rpm1, rpm2 = read_fan_rpm(bus, i2c_addr, num_fans)

        # Construct JSON output
        fan_data = {
            "i2c_address": hex(i2c_addr),
            "duty_cycle_percentage": percentage,
            "fan_1_rpm": rpm1 if rpm1 is not None else "N/A",
            "fan_2_rpm": rpm2 if rpm2 is not None else "N/A"
        }

        # Print JSON output
        print(json.dumps(fan_data, indent=4))

    except ValueError:
        print("Error: Invalid input. Please enter a valid I2C address (e.g., 0x2F), percentage (0-100), and number of fans (1 or 2).")

    finally:
        bus.close()
