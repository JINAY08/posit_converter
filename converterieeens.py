import numpy as np

class ieeens():
    def __init__(self,length,exp):
        self.length = length
        self.exp = exp 
    
    def extract(self,operand):
        total_length = self.length
        exp_length = self.exp

        frac_length = total_length - exp_length - 1

        if(frac_length<0):
            return (None)
        
        e_max = 2**(exp_length-1) - 1
        e_min = -1*(2**(exp_length-1))
        s=0
        e=0
        f=1
        if(operand==0):
            return(s,e,f-1)
        elif(operand<0):
            s=1
        operand = abs(operand)
        exp = int(np.floor(np.log2(operand)))

        if(exp>e_max):
            e=e_max
        elif(exp<e_min):
            e=e_min
        else:
            e=exp

        f=float(operand)/(2**exp)
        f_new=f-1
        for i in range(1,frac_length+1):
            f_new-=2**(-i)
            if(f_new<0):
                f_new+=2**(-i)
        # Rounding error begin
        rounding=2**(-1*(frac_length+1))
        # print(rounding)
        if(f_new>=rounding):
            f = f-f_new+2**(-1*(frac_length))
            if(f>=2):
                f=f/2
                e+=1
        else:
            f = f - f_new
        # Rounding error end
        return (s,e,f)

    def neg(self,string):
        out = ""
        # print(len(string))
        for i in range(len(string)):
            if(string[i]=="1"):
                out+="0"
            else:
                out+="1"
        # print(out)
        return out
    def float2ieeens(self,dec):
        total_length = self.length
        exp_length = self.exp

        frac_length = total_length - exp_length - 1

        sign,e,frac = self.extract(dec)

        if(sign==0 and e==0 and frac == 0):
            return ("0"*total_length) # if the input is 0
        out=''
        bias = 2**(exp_length-1)-1
        e=e+bias
        if(e<0):
            e_bin = bin(e)[3:]
        else:
            e_bin = bin(e)[2:]
        # print(e_bin)
        if(len(e_bin)<exp_length):
            e_bin = "0"*(exp_length-len(e_bin)) + e_bin
        # print(e_bin)
        out+=e_bin

        frac -= 1
        frac_bin = ""
        for i in range(frac_length):
            # print(frac)
            frac*=2
            if(frac>=1):
                frac_bin +="1"
                frac -=1
            else:
                frac_bin +="0" 
        out+=frac_bin
        # print(out)
        # do it at last
        if(sign==0):
            out ='0' + out
        else:
            out ='1' + out
        return (out)
    
    def ieeens2float(self,ieeens_dec):
        total_length = self.length
        exp_length = self.exp

        frac_length = total_length - exp_length - 1

        if(ieeens_dec=="0"*total_length):
            return (0.0)
        
        exp_bits = ieeens_dec[1:exp_length+1]
        e = int(exp_bits,2)
        bias = 2**(exp_length-1)-1
        exp = e - bias
        

        frac_bits = ieeens_dec[1+exp_length:]
        # print(frac_bits)
        frac = 1
        for i in range(len(frac_bits)):
            if(frac_bits[i]=="1"):
                frac += 2**(-(i+1)) 
        out = frac*2**(exp) 
        if(ieeens_dec[0]=="0"):
            return (out)
        else:
            return (-1*out)


#ieeens = ieeens(8,4)
#a=255
#print(ieeens.extract(a))
#print(ieeens.float2ieeens(a))
#print(ieeens.ieeens2float(ieeens.float2ieeens(a)))
