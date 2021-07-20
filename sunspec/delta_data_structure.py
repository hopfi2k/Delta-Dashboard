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
            "Phase1_Output_Voltage": 223.5,
            "Phase1_Output_Current": 25.32,
            "Phase1_Output_Power": 5170,
            "Phase1_Output_Frequency": 50.00,
            "Phase1_Output_Max_Voltage": 230.4,
            "Phase1_Output_Max_Current": 79.53,
            "Phase1_Output_Max_Power": 17080,
            "Phase1_Output_Max_Frequency": 50.07,
        },
        "Phase2_Output": {
            "Phase2_Output_Voltage": 223.1,
            "Phase2_Output_Current": 25.38,
            "Phase2_Output_Power": 5240,
            "Phase2_Output_Frequency": 50.00,
            "Phase2_Output_Max_Voltage": 230.2,
            "Phase2_Output_Max_Current": 79.51,
            "Phase2_Output_Max_Power": 17100,
            "Phase2_Output_Max_Frequency": 50.07,
        },
        "Phase3_Output": {
            "Phase3_Output_Voltage": 224.5,
            "Phase3_Output_Current": 25.08,
            "Phase3_Output_Power": 5130,
            "Phase3_Output_Frequency": 50.00,
            "Phase3_Output_Max_Voltage": 231.3,
            "Phase3_Output_Max_Current": 79.56,
            "Phase3_Output_Max_Power": 17020,
            "Phase3_Output_Max_Frequency": 50.07,
        },
        "String_1": {
            "String_1_Voltage": 673.2,
            "String_1_Current": 4.35,
            "String_1_Power": 2930,
            "String_1_Max_Voltage": 783.8,
            "String_1_Max_Current": 15.83,
            "String_1_Max_Power": 10220,
        },
        "String_2": {
            "String_2_Voltage": 676.5,
            "String_2_Current": 4.58,
            "String_2_Power": 3100,
            "String_2_Max_Voltage": 783.3,
            "String_2_Max_Current": 16.16,
            "String_2_Max_Power": 10350,
        },
        "String_3": {
            "String_3_Voltage": 662.5,
            "String_3_Current": 4.95,
            "String_3_Power": 3280,
            "String_3_Max_Voltage": 783.7,
            "String_3_Max_Current": 16.51,
            "String_3_Max_Power": 10620,
        },
        "String_4": {
            "String_4_Voltage": 661.9,
            "String_4_Current": 5.15,
            "String_4_Power": 3410,
            "String_4_Max_Voltage": 782.7,
            "String_4_Max_Current": 16.10,
            "String_4_Max_Power": 10640,
        },
        "String_5": {
            "String_5_Voltage": 670.0,
            "String_5_Current": 2.55,
            "String_5_Power": 1710,
            "String_5_Max_Voltage": 782.0,
            "String_5_Max_Current": 8.15,
            "String_5_Max_Power": 5270,
        },
        "String_6": {
            "String_6_Voltage": 695.1,
            "String_6_Current": 2.31,
            "String_6_Power": 1610,
            "String_6_Max_Voltage": 782.0,
            "String_6_Max_Current": 8.07,
            "String_6_Max_Power": 5300,
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
