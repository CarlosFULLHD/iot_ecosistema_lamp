from machine import ADC , Pin
import time

class Sensor:
    def __init__(self, pin_lm35, pin_setpoint):
        self.adc_lm35 = pin_lm35  # Pin ADC para LM35
        self.adc_setpoint = pin_setpoint
        self.adclm35 = ADC(self.adc_lm35)
        self.adc_temp_int = ADC(4)  # Pin ADC para sensor de temperatura interna
        self.adcsetpoint = ADC(self.adc_setpoint) 
        

    def ReadTemperature(self):
        adc_value = self.adclm35.read_u16()
        volt = (3.3 / 65535) * adc_value
        temp = volt/(10.0 / 1000)
        degC = round(temp, 1)
        return degC

    def TempInt(self):
        factor_16 = 3.3 / (65535)
        voltaje = self.adc_temp_int.read_u16() * factor_16
        temperatura = 27 - (voltaje - 0.706) / 0.001721
        Inttemp = round(temperatura, 1)
        return Inttemp
    
   # def map_setpoint(value, in_min, in_max, out_min, out_max):
    #    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def Setpoint(self):
        #x = map_setpoint(self.adc_setpoint.read_u16(), 0, 50, 0, 65535)
        x = (self.adcsetpoint.read_u16() - 0) * (65535 - 0) / (50 - 0) + 0
        return x
        

class File:
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.file.write("Nreg"+"\t"+"dia/mes/año"+ "\t"+ "hora/min/seg" + "\t"+"LM35" + "\t" + "TempInt" +"\t" +"SetPoint"+"\t" +"RGB" +"\t" +"Nmed"+"\t" +"NmedOnOff"+"\n")

    def WriteData(self,k,t,lm35_temp, int_temp, setpoint, rgb, nmed, nmedonoff):
        time = str(t)
        lm35_temp = str(round(lm35_temp, 2))
        int_temp = str(round(int_temp,2))
        setpoint = str(round(setpoint,2)) 
        self.file.write(str(k)+"\t"+time + "\t" + lm35_temp +"\t"+ int_temp +"\t" + setpoint + "\t" + str(rgb) + "\t" + str(nmed) + "\t" + str(nmedonoff))
        self.file.write("\n")
        self.file.flush()
        
    def GetDateTime(self):
        datetime = time.localtime()
        year = str(datetime[0])
        month = str(datetime[1])
        if (len(month) == 1):
            month = "0" + month
        day = str(datetime[2])
        if (len(day) == 1):
            day = "0" + day
        hour = str(datetime[3])
        if (len(hour) == 1):
            hour = "0" + hour
        minute = str(datetime[4])
        if (len(minute) == 1):
            minute = "0" + minute
        second = str(datetime[5])
        if (len(second) == 1):
            second = "0" + second
        d = year + "." + month + "." + day
        t = hour + ":" + minute + ":" + second
        timestamp = d + "\t" + t
        return timestamp

