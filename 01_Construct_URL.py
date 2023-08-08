import calendar as c
import subprocess as s
import time as t


URL_PREFIX = 'https://www.bts.gov/sites/bts.dot.gov/files/transborder-raw'

years = range(2014,2024, 1)
months = range(1, 13)


"""

EXAMPLE_URL='https://www.bts.gov/sites/bts.dot.gov/files/transborder-raw/2023/Jan2023.zip'

print('Running bash script')
s.call(["bash", "./01_Extractdata_LoadToGCS.sh", EXAMPLE_URL, '2023'])
print ("Pausing for 15 Seconds")
t.sleep(15)

"""

for y in years:
    if y < 2018:
        URL=f'{URL_PREFIX}/{y}/{y}.zip'
        print(URL)
        print('Running bash script')
        s.call(["bash", "./01_ExtractData_LoadToGCS.sh", URL, str(y)])
        print ("Pausing for 15 Seconds")
        t.sleep(15)

    else:
        for m in months:
            m_abbr = c.month_abbr[m]
            m_long = c.month_name[m]

            if y == 2018:
                if m == 1: #Jan 2018
                    URL=f'{URL_PREFIX}/{y}/{m_abbr}.{y}.zip'
                elif m in (2,3): #Feb-Mar 2018
                    URL=f'{URL_PREFIX}/{y}/{m_abbr}{y}.zip'
                elif m in range(4,10): #April-Sep 2018
                    URL=f'{URL_PREFIX}/{y}/{m_long}{y}.zip'
                elif m in range(10,12): #Oct-Nov 2018
                    URL=f'{URL_PREFIX}/{y}/{m_long}{y}TransBorderRawData.zip'
                else: #Dec 2018
                    URL_SUFFIX='December2018TransBorderRawData-plus-yr-end.zip'
                    URL=f'{URL_PREFIX}/{y}/{URL_SUFFIX}.zip'
            elif y in (2019, 2020): #2019 & 2020
                URL=f'{URL_PREFIX}/{y}/{m_long}{y}TransBorderRawData.zip'
            elif y == 2021:
                if m < 7: #Jan-Jun 2021
                    URL=f'{URL_PREFIX}/{y}/{m_long}{y}TransBorderRawData.zip'
                elif m == 7: #July 2021
                    URL=f'{URL_PREFIX}/{y}/July-to-Dec-2021.zip'
                else:
                    break
            elif y == 2022:
                if m in range(1,3): #Jan-Feb 2022
                    URL=f'{URL_PREFIX}/{y}/{m_abbr}-{y}.zip'
                elif m == 3: #Mar 2022
                    URL=f'{URL_PREFIX}/{y}/{m_long}-{y}.zip'
                else: #Apr-Dec 2022
                    URL=f'{URL_PREFIX}/{y}/{m_long}{y}.zip'
            else: #2023
                if m in (1,2):
                    URL=f'{URL_PREFIX}/{y}/{m_abbr}{y}.zip'
                elif m in range(3,6):
                    URL=f'{URL_PREFIX}/{y}/{m_long}{y}.zip'
                else:
                    break

            print(URL)
            print('running bash script')
            s.call(["bash", "./01_ExtractData_LoadToGCS.sh", URL, str(y)])
            print ("Pausing for 15 Seconds")
            t.sleep(15)
