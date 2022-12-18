import predictor #user library
import pandas as pd
import numpy as np
import time


startMain = time.time()
#____________// MAIN ARCHITECTURE //____________#
print('-='*50)
print('\n\t\t<< METAR Data Analysis - Prediction Model >>\n\n')

start_1 = time.time()
reg_model = predictor.GradientBooster()
end_1 = time.time()
print(f'\n>> Loaded Gradient Booster Algorythm in {round((end_1-start_1),3)} seconds.\n')


#----------------------#
# User input variables
print('\n>> Please, fill the requested data with the current METAR variables:')

## 1. Numeric Variables
print('\n~ NUMERIC VARIABLES ~\n')
tmpf = input('* Air Temperature in Farenheint -> ')
dwpf = input('* Dew Point Temperature in Fahrenheit -> ')
relh = input('* Relative Humidity in % -> ')
drct = input('* Wind Direction in degrees from true north -> ')
sknt = input('* Wind Speed in knots -> ')
alti = input('* Pressure altimeter in inches/Hg -> ')
vsby = input('* Visibility in miles -> ')
skyl1 = input('* Sky Level 1 Coverage -> ')
feel = input('* Apparent Temperature (Wind Chill or Heat Index) in Fahrenheit -> ')
entries = (tmpf,dwpf,relh,drct,sknt,alti,vsby,skyl1,feel)
try:
    float_converted = []
    for e in entries:
        e = float(e)
        float_converted.append(e)    
    tmpf,dwpf,relh,drct,sknt,alti,vsby,skyl1,feel = float_converted
    print(f'Current numeric entries:{float_converted}')
except:
    print('One or more entries are invalid! Cannot authenticate as a model input...')


## 2. Categorical Variables
print('\n~ CATEGORICAL VARIABLES ~')

### (i) Sky Coverage Variable
print('\n* Sky Level 1 Coverage Code\n1-BKN\n2-FEW\n3-NSC\n4-OVC\n5-SCT\n6-VV')
Sky_Coverage = input('Insert SKL1 Code -> ')
if(Sky_Coverage == '1'):
    print('Selected SKL1: BKN')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 1,0,0,0,0,0
elif(Sky_Coverage == '2'):
    print('Selected SKL1: FEW')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 0,1,0,0,0,0
elif(Sky_Coverage == '3'):
    print('Selected SKL1: NSC')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 0,0,1,0,0,0
elif(Sky_Coverage == '4'):
    print('Selected SKL1: OVC')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 0,0,0,1,0,0
elif(Sky_Coverage == '5'):
    print('Selected SKL1: SCT')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 0,0,0,0,1,0
elif(Sky_Coverage == '6'):
    print('Selected SKL1: VV')
    skyc1_BKN, skyc1_FEW, skyc1_NSC, skyc1_OVC, skyc1_SCT, skyc1_VV = 0,0,0,0,0,1
else:
    print('Invalid Entry! Cannot authenticate as a model input...')

### (ii) Month Variable
print('\n* Current Month Code\n1-JAN\n2-FEB\n3-MAR\n4-APR\n5-MAY\n6-JUN\n7-JUL\n8-AUG\n9-SEP\n10-OCT\n11-NOV\n12-DEC')
Month = input('Insert Month Code -> ')
if(Month == '1'):
    print('Selected month: JAN')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 1,0,0,0,0,0,0,0,0,0,0,0
elif(Month == '2'):
    print('Selected month: FEB')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,1,0,0,0,0,0,0,0,0,0,0
elif(Month == '3'):
    print('Selected month: MAR')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,1,0,0,0,0,0,0,0,0,0
elif(Month == '4'):
    print('Selected month: APR')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,1,0,0,0,0,0,0,0,0
elif(Month == '5'):
    print('Selected month: MAY')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,1,0,0,0,0,0,0,0
elif(Month == '6'):
    print('Selected month: JUN')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,1,0,0,0,0,0,0
elif(Month == '7'):
    print('Selected month: JUL')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,1,0,0,0,0,0
elif(Month == '8'):
    print('Selected month: AUG')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,0,1,0,0,0,0
elif(Month == '9'):
    print('Selected month: SEP')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,0,0,1,0,0,0
elif(Month == '10'):
    print('Selected month: OCT')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,0,0,0,1,0,0
elif(Month == '11'):
    print('Selected month: NOV')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,0,0,0,0,1,0
elif(Month == '12'):
    print('Selected month: DEC')
    month_Jan, month_Feb, month_Mar, month_Apr, month_May, month_Jun,\
    month_Jul, month_Aug, month_Sep, month_Oct, month_Nov, month_Dec = 0,0,0,0,0,0,0,0,0,0,0,1
else:
    print('Invalid Entry! Cannot authenticate as a model input...')

### (iii) Day of Week Variable
print('\n* Current Day of Week Code\n1-SUN\n2-MON\n3-TUE\n4-WED\n5-THU\n6-FRI\n7-SAT')
Day_of_Week = input('Insert Day of Week Code -> ')
if(Day_of_Week == '1'):
    print('Selected day of week: SUN')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 1,0,0,0,0,0,0
elif(Day_of_Week == '2'):
    print('Selected day of week: MON')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,1,0,0,0,0,0
elif(Day_of_Week == '3'):
    print('Selected day of week: TUE')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,0,1,0,0,0,0
elif(Day_of_Week == '4'):
    print('Selected day of week: WED')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,0,0,1,0,0,0
elif(Day_of_Week == '5'):
    print('Selected day of week: THU')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,0,0,0,1,0,0
elif(Day_of_Week == '6'):
    print('Selected day of week: FRI')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,0,0,0,0,1,0
elif(Day_of_Week == '7'):
    print('Selected day of week: SAT')
    dayofweek_flag_Sun, dayofweek_flag_Mon, dayofweek_flag_Tues, dayofweek_flag_Wed,\
    dayofweek_flag_Thurs, dayofweek_flag_Fri, dayofweek_flag_Sat = 0,0,0,0,0,0,1
else:
    print('Invalid Entry! Cannot authenticate as a model input...')

### (iv) Season Variable
print('\n* Current Season Code\n1-SUMMER\n2-AUTUMN\n3-WINTER\n4-SPRING')
Season = input('Insert Season Code -> ')
if(Season == '1'):
    print('Selected season: 1')
    season_flag_summer, season_flag_autumn, season_flag_winter, season_flag_spring = 1,0,0,0
elif(Season == '2'):
    print('Selected season: 2')
    season_flag_summer, season_flag_autumn, season_flag_winter, season_flag_spring = 0,1,0,0
elif(Season == '3'):
    print('Selected season: 3')
    season_flag_summer, season_flag_autumn, season_flag_winter, season_flag_spring = 0,0,1,0
elif(Season == '4'):
    print('Selected season: 4')
    season_flag_summer, season_flag_autumn, season_flag_winter, season_flag_spring = 0,0,0,1
else:
    print('Invalid Entry! Cannot authenticate as a model input...')

### (v) Flight Rule Code Variable
print('\n* Current Flight Rule Code\n1-VFR\n2-MVFR\n3-IFR\n4-LIFR')
FR_CODE = input('Insert Flight Rule Code -> ')
if(FR_CODE == '1'):
    print('Selected Flight Rule Code: VFR')
    fr_code_VFR, fr_code_MVFR, fr_code_IFR, fr_code_LIFR = 1,0,0,0
if(FR_CODE == '2'):
    print('Selected Flight Rule Code: MVFR')
    fr_code_VFR, fr_code_MVFR, fr_code_IFR, fr_code_LIFR = 0,1,0,0
if(FR_CODE == '3'):
    print('Selected Flight Rule Code: IFR')
    fr_code_VFR, fr_code_MVFR, fr_code_IFR, fr_code_LIFR = 0,0,1,0
if(FR_CODE == '4'):
    print('Selected Flight Rule Code: LIFR')
    fr_code_VFR, fr_code_MVFR, fr_code_IFR, fr_code_LIFR = 0,0,0,1


#----------------------#
# Prediction Model Input:
arr = np.array([
                [tmpf,dwpf,relh,drct,sknt,alti,vsby,skyl1,feel,skyc1_BKN,skyc1_FEW,
                 skyc1_NSC,skyc1_OVC,skyc1_SCT,skyc1_VV ,month_Apr,month_Aug,month_Dec,
                 month_Feb,month_Jan,month_Jul,month_Jun,month_Mar,month_May,month_Nov,
                 month_Oct,month_Sep,dayofweek_flag_Fri,dayofweek_flag_Mon,dayofweek_flag_Sat,
                 dayofweek_flag_Sun,dayofweek_flag_Thurs,dayofweek_flag_Tues,dayofweek_flag_Wed,
                 season_flag_autumn,season_flag_spring,season_flag_summer,season_flag_winter,
                 fr_code_IFR,fr_code_LIFR,fr_code_MVFR,fr_code_VFR]
                ])

time.sleep(1)
print('\n>> Starting Prediction...')
y_pred = reg_model.predict(arr)
time.sleep(1)

print(f"Results: tmpf={round(y_pred.item(0),3)} | relh={round(y_pred.item(1),3)} | sknt={round(y_pred.item(2),3)} | alti={round(y_pred.item(3),3)} | vsby={round(y_pred.item(4),3)} | skyl1={round(y_pred.item(5),3)}")


#____________// END //____________#
endMain = time.time()
print(f'\n>> Time elapsed is {round((endMain-startMain),3)} seconds.\n   End of execution.\n')