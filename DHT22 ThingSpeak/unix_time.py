class unix():
    month_table = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, time_zone):
        self.time_zone_offset = (time_zone * 3600)

    def leap_year_check(self, year):
        if((year % 4) == 0):

            if((year % 100) == 0):

                if((year % 400) == 0):
                    return True
                else:
                    return False

            else:
                return True

        else:
            return False



    def unix_to_date_time(self, counts):
        tmp = 0
        temp = 0
        day_count = 0
        
        year = 0
        month = 0
        date = 0
        hour = 0
        minute = 0
        second = 0

        counts = (counts + self.time_zone_offset)

        temp = (counts // 86400)

        if(day_count != temp):
            day_count = temp
            tmp = 1970

            while(temp >= 365):
                if(self.leap_year_check(tmp) == True):
                    
                    if(temp >= 366):
                        temp -= 366
                    else:
                        break

                else:
                    temp -= 365

                tmp += 1

            year = tmp

            tmp = 0
            while(temp >= 28):
                if((tmp == 1) and (self.leap_year_check(year) == True)):
                    
                    if(temp >= 29):
                        temp -= 29

                    else:
                        break

                else:
                    if(temp >= unix.month_table[tmp]):
                        temp -= unix.month_table[tmp]

                    else:
                        break

                tmp += 1

        month = (tmp + 1)
        date = (temp + 1)

        temp = (counts % 86400)

        hour = (temp // 3600)
        minute = ((temp % 3600) // 60)
        second = ((temp % 3600) % 60)

        return year, month, date, hour, minute, second
    
    
    def date_time_to_unix(self, year, month, date, hour, minute, second):
        i = 0
        counts = 0
        
        if(year >= 2099):
            year = 2099
        
        if(year <= 1970):
            year = 1970
            
        for i in range (1970, year):
            if(self.leap_year_check(i) == True):
                counts += 31622400
            else:
                counts += 31536000
                
        month -= 1
        
        for i in range (0, month):
            counts += ((unix.month_table[i]) * 86400)
        
        if(self.leap_year_check(year) == True):
            counts += 86400
            
        counts += ((date - 1) * 86400)
        counts += (hour * 3600)
        counts += (minute * 60)
        counts += second
        
        return counts