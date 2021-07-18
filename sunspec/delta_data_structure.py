#
# Data structure for the data from the DELTA inverter
#
class DeltaDataStructure:
    data = {
        "Inverter": {
            "DSP_FW_Version": "V1.31",
            "Redundant_FW_Version": "V1.11",
            "Comm_FW_Version": "V1.27",
            "ARC_FW_Version": "V1.15",
            "Serial_Number": "08X20A04404WH",
            "Model_Name": "M70A_260"
        },
        "Status": {
            "State": "On Grid(2)",
            "Countdown": "0s",
            "Max_Power": 77000,
            "Clock": "2021/07/14 15:09:54",
            "Installation": "2021/07/12",
        },
        "Phase1_Output": {
            "Voltage": 223.5,
            "Current": 25.32,
            "Power": 5170,
            "Frequency": 50.00,
            "Max_Voltage": 230.4,
            "Max_Current": 79.53,
            "Max_Power": 17080,
            "Max_Frequency": 50.07,
        },
        "Phase2_Output": {
            "Voltage": 223.1,
            "Current": 25.38,
            "Power": 5240,
            "Frequency": 50.00,
            "Max_Voltage": 230.2,
            "Max_Current": 79.51,
            "Max_Power": 17100,
            "Max_Frequency": 50.07,
        },
        "Phase3_Output": {
            "Voltage": 224.5,
            "Current": 25.08,
            "Power": 5130,
            "Frequency": 50.00,
            "Max_Voltage": 231.3,
            "Max_Current": 79.56,
            "Max_Power": 17020,
            "Max_Frequency": 50.07,
        },
        "Input_1": {
            "Voltage": 673.2,
            "Current": 4.35,
            "Power": 2930,
            "Max_Voltage": 783.8,
            "Max_Current": 15.83,
            "Max_Power": 10220,
        },
        "Input_2": {
            "Voltage": 676.5,
            "Current": 4.58,
            "Power": 3100,
            "Max_Voltage": 783.3,
            "Max_Current": 16.16,
            "Max_Power": 10350,
        },
        "Input_3": {
            "Voltage": 662.5,
            "Current": 4.95,
            "Power": 3280,
            "Max_Voltage": 783.7,
            "Max_Current": 16.51,
            "Max_Power": 10620,
        },
        "Input_4": {
            "Voltage": 661.9,
            "Current": 5.15,
            "Power": 3410,
            "Max_Voltage": 782.7,
            "Max_Current": 16.10,
            "Max_Power": 10640,
        },
        "Input_5": {
            "Voltage": 670.0,
            "Current": 2.55,
            "Power": 1710,
            "Max_Voltage": 782.0,
            "Max_Current": 8.15,
            "Max_Power": 5270,
        },
        "Input_6": {
            "Voltage": 695.1,
            "Current": 2.31,
            "Power": 1610,
            "Max_Voltage": 782.0,
            "Max_Current": 8.07,
            "Max_Power": 5300,
        },
        "Temperature": {
            "Ambient": {
                "Now": 36.0,
                "Max": 53.1,
            },
            "Boost-1": {
                "Now": 53.0,
                "Max": 57.2,
            },
            "Boost-2": {
                "Now": 0.0,
                "Max": 0.0,
            },
            "Inverter": {
                "Now": 52.0,
                "Max": 60.1,
            }
        },
        "Energy": {
            "Today": {
                "Wh": 166.000,
                "Runtime": "9:37:1",
            },
            "Life": {
                "Wh": 394.500,
                "Lifetime": "32:4:4",
            }
        },
        "Bus_Voltage": {
            "PBus": 368.7,
            "NBus": 369.6,
        },
        "Errors": {
            "Time": "2021/07/14 11:32:51",
            "Code": "E02- AC Freq Low",
        }
    }

    def __init__(self):
        pass

    def get(self):
        return self.data
