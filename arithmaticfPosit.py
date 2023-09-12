import numpy as np

class fposit_arithmetic:
    def __init__(self,length,regime_len,es):
        self.length = length
        self.es = es
        self.regime_len = regime_len
    
    def extract(self,operand):
        total_length = self.length
        es = self.es
        regime_len = self.regime_len
        frac_length = total_length - es - regime_len - 1
        if(frac_length<0):
            return (None)
        k_max = regime_len-1
        k_min = -1*regime_len
        e_max = 2**es - 1
        s=0
        e=0
        k=0
        f=1
        if(operand==0):
            return(s,k,e,f-1)
        elif(operand<0):
            s=1
        operand = abs(operand)
        exp = int(np.floor(np.log2(operand)))
        useed= 2**es
        k=int(np.floor(exp/useed))
        e=exp-k*useed
        if(k>k_max):
            k=k_max
        elif(k<k_min):
            k=k_min
        
        if(e>e_max):
            e=e_max
        f=float(operand)/(2**exp)
        f_new=f-1
        for i in range(1,frac_length+1):
            f_new-=2**(-i)
            if(f_new<0):
                f_new+=2**(-i)
        return (s,k,e,f-f_new)

    def multiply(self,operand1,operand2):
        total_length = self.length
        es = self.es
        regime_len = self.regime_len
        frac_length = total_length - es - regime_len - 1
        k_max = regime_len-1
        k_min = -1*regime_len
        e_max = 2**es - 1


        s1,k1,e1,f1=self.extract(operand1)
        s2,k2,e2,f2=self.extract(operand2)
        if((s1+k1+e1+f1==0) or (s2+k2+e2+f2==0)):
            return (0.0)
        # If sum of signs is >0 -> 
        s=s1+s2
        if(s!=1):
            s=0
        e1 = e1 + k1*(2**es)
        e2 = e2 + k2*(2**es)
        e = e1+e2
        f=f1*f2
        if(f>=2):
            f/=2
            e += 1

        useed= 2**es
        k=int(np.floor(e/useed))
        if(k>k_max):
            k=k_max
        elif(k<k_min):
            k=k_min
        e=e-k*useed
        if(e>e_max):
            e=e_max
        f_new=f-1
        for i in range(1,frac_length+1):
            f_new-=2**(-i)
            if(f_new<0):
                f_new+=2**(-i)
        # print(s,k,e,f-f_new)
        if(s==1):
            return -1*((f-f_new)*(2**((2**es)*k + e)))
        else:
            return ((f-f_new)*(2**((2**es)*k + e)))


    def add(self,operand1,operand2):
        total_length = self.length
        es = self.es
        regime_len = self.regime_len
        frac_length = total_length - es - regime_len - 1
        k_max = regime_len-1
        k_min = -1*regime_len
        e_max = 2**es - 1

        # operand 1 is larger amoung both
        if(abs(operand1)<abs(operand2)):
            help_=operand1
            operand1=operand2
            operand2=help_

        s1,k1,e1,f1=self.extract(operand1)
        s2,k2,e2,f2=self.extract(operand2)
        
        if((s1+k1+e1+f1==0) or (s2+k2+e2+f2==0)):
            return ((-1**s1)*f1*(2**((2**es)*k1 + e1)) + (-1**s2)*f2*(2**((2**es)*k2 + e2)))
        
        s=s1
        s_check=s1+s2
        if(s_check>1):
            s_check=0
        e1 = e1 + k1*(2**es)
        e2 = e2 + k2*(2**es)

        shift = e1-e2
        f2 = f2/(2**(shift))
        
        e=e1
        if(s_check==0):
            f=f1+f2
        else:
            f=f1-f2
        if(f==0):
            return (0.0)
        # print(f)
        while(f>=2):
            f/=2
            e+=1
        while(f<1):
            f*=2
            e-=1


        useed= 2**es
        k=int(np.floor(e/useed))
        if(k>k_max):
            k=k_max
        elif(k<k_min):
            k=k_min
        e=e-k*useed
        if(e>e_max):
            e=e_max
        f_new=f-1
        for i in range(1,frac_length+1):
            f_new-=2**(-i)
            if(f_new<0):
                f_new+=2**(-i)
        # print(s,k,e,f-f_new)
        if(s==1):
            return -1*((f-f_new)*(2**((2**es)*k + e)))
        else:
            return ((f-f_new)*(2**((2**es)*k + e)))

# posit = fposit_arithmetic(32,6,2)
# # print(posit.extract(-1.5))
# # print(posit.extract(0.0075))

# print(posit.add(-1024,0.0075))


