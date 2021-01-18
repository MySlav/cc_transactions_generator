import datetime as dt
import xml.etree.cElementTree as ET
from random import choice,choices,random,randint
from string import digits

# random.seed(None) #None default  - determined by present time

def randomTime():
    # random number scaled on seconds of the day
    rtime = int(random()*86400)
    # Hours, mintues and seconds
    hours = int(rtime/3600)
    minutes = int((rtime - hours*3600)/60)
    seconds = rtime - hours*3600 - minutes*60
    # Result in needed format
    time_string = '%02d%02d%02d' % (hours, minutes, seconds)
    return time_string





def generate_card():
    """
    Prefill some values based on the card type
    """
    card_types = ["americanexpress","visa13", "visa16","mastercard","discover"]
    t=choice(card_types)
    def prefill(t):
        # typical number of digits in credit card
        def_length = 16
        
        """
        Prefill with initial numbers and return it including the total number of digits
        remaining to fill
        """
        if t == card_types[0]:
            # american express starts with 3 and is 15 digits long
            # override the def lengths
            return [3, randint(4,7)], 13
            
        elif t == card_types[1] or t == card_types[2]:
            # visa starts with 4
            if t.endswith("16"):
                return [4], def_length - 1
            else:
                return [4], 12
            
        elif t == card_types[3]:
            # master card start with 5 and is 16 digits long
            return [5, randint(1,5)], def_length - 2
            
        elif t == card_types[4]:
            # discover card starts with 6011 and is 16 digits long
            return [6, 0, 1, 1], def_length - 4
            
        else:
            # this section probably not even needed here
            return [], def_length
    
    def finalize(nums):
        """
        Make the current generated list pass the Luhn check by checking and adding
        the last digit appropriately bia calculating the check sum
        """
        check_sum = 0
        
        #is_even = True if (len(nums) + 1 % 2) == 0 else False
        
        """
        Reason for this check offset is to figure out whther the final list is going
        to be even or odd which will affect calculating the check_sum.
        This is mainly also to avoid reversing the list back and forth which is specified
        on the Luhn algorithm.
        """
        check_offset = (len(nums) + 1) % 2
        
        for i, n in enumerate(nums):
            if (i + check_offset) % 2 == 0:
                n_ = n*2
                check_sum += n_ -9 if n_ > 9 else n_
            else:
                check_sum += n
        return nums + [10 - (check_sum % 10) ]
    
# main part of func generate_card
    initial, rem = prefill(t)
    so_far = initial + [randint(1,9) for x in range(rem - 1)]
    return ("".join(map(str,finalize(so_far))))





# main body
root = ET.Element("root")

print('Number of transactions per day:')
x = int(input())

print('Total number of days in the past:')
y = int(input())

for j in range(0,y+1):
    for i in range(x):
        # Date and time in needed format
        date_x=(dt.date.today()-dt.timedelta(j)).strftime('%d%m%Y')
        time_x=randomTime()

        # Random 16 digit CC string
        CC_x = generate_card()

        # Amount - realistic figure?,  max 6 digit one without decimal part
        whole=("")
        for z in range(0,randint(1,6)):
            if z==0:
                temp=str(randint(1,6))
            else:
                temp=str(randint(0,6))
            whole=whole+temp

        dec=randint(0,99)
        if dec<10:
            dec_s=str("0"+str(dec))
        else:
            dec_s=str(dec)

        amount_x=whole+"."+ dec_s

        log = ET.SubElement(root, "LOG")
        ET.SubElement(log, "DATE").text = date_x
        ET.SubElement(log, "TIME").text = time_x
        ET.SubElement(log, "CC").text = CC_x
        ET.SubElement(log, "AMOUNT").text = amount_x


tree = ET.ElementTree(root)
tree.write("history.xml")