import random

class InnType:
    def __init__(self, inn_type=''):
        self.inn_type = inn_type
       
    def inn_withdrawal(self):
            while(True):
                value_selection = ''
                inn=''
                if self.inn_type == 'YUR':
                    for i in range(9): 
                        value_selection += str(random.randint(0, 9))

                    fitted_value_conversion = list(map(int, value_selection))
                    calculation = (2 * fitted_value_conversion[0]) + (4 * fitted_value_conversion[1]) + (10 * fitted_value_conversion[2]) + (3 * fitted_value_conversion[3]) + (5 * fitted_value_conversion[4]) + (9 * fitted_value_conversion[5]) + (4 * fitted_value_conversion[6]) + (6 * fitted_value_conversion[7]) + (8 * fitted_value_conversion[8])
                    selection_of_a_suitable = calculation % 11 %10

                    if (selection_of_a_suitable == 0 or 1):
                        fitted_value_conversion.insert(9, selection_of_a_suitable)  
                        for s in range(10):
                                inn += str(fitted_value_conversion[s])
                        return inn

                    
                        
               

                elif self.inn_type == "FIZ":
                    for i in range(10): 
                        value_selection += str(random.randint(0, 9))

                    fitted_value_conversion = list(map(int, value_selection))
                    calculation = (7 * fitted_value_conversion[0]) + (2 * fitted_value_conversion[1]) + (4 * fitted_value_conversion[2]) + (10 * fitted_value_conversion[3]) +  (3 * fitted_value_conversion[4]) + (5 * fitted_value_conversion[5]) + (9 * fitted_value_conversion[6]) + (4 * fitted_value_conversion[7])+ (6 * fitted_value_conversion[8])+ (8 * fitted_value_conversion[9])
                    selection_of_a_suitable = calculation % 11 %10
                    fitted_value_conversion.insert(10, selection_of_a_suitable)

                    calculation2 = (3 * fitted_value_conversion[0]) + (7 * fitted_value_conversion[1]) + (2 * fitted_value_conversion[2]) + (4 * fitted_value_conversion[3]) + (10 * fitted_value_conversion[4]) + (3 * fitted_value_conversion[5]) + (5 * fitted_value_conversion[6]) + (9 * fitted_value_conversion[7]) + (4 * fitted_value_conversion[8])+ (6 * fitted_value_conversion[9])+ (8 * fitted_value_conversion[10])
                    selection_of_a_suitable2 = calculation2 % 11 %10
                    fitted_value_conversion.insert(11, selection_of_a_suitable2)

                    for s in range(12):
                        inn += str(fitted_value_conversion[s])
                    return inn    

                else:
                    return 'Неверно выбран тип!\nВыберите тип: FIZ или YUR'       
               

    
                    