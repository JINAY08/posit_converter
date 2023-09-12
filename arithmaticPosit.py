import numpy as np

class posit_arithmatic:
	def __init__(self,length,es):
		self.length = length
		self.es = es
	def extract(self,operand):
		total_length = self.length
		es = self.es
		k_max = total_length - 1 - 1
		k_min = -1*(total_length - 1)
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
		if(k>k_max):
		    k=k_max
		elif(k<k_min):
		    k=k_min

		if(k>=0):
			if(k==k_max):
				regime_len = k + 1
			else:
				regime_len = k + 2 
		else:
			if(k==k_min):
				regime_len = abs(k)
			else:
				regime_len = abs(k) + 1

		bits_remaining = total_length - 1 - regime_len
		if(bits_remaining>=es):
			es_length = es
		else:
			es_length = bits_remaining

		e=exp-k*useed
		e_remaining_max = 2**(es_length) - 1
		if(e>e_remaining_max):
			e=e_remaining_max

		frac_length = total_length - 1 - regime_len - es_length 

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
		useed = 2**es
		[s1,k1,e1,f1]=self.extract(operand1)
		[s2,k2,e2,f2]=self.extract(operand2)
		
		# Checking for 0
		if((abs(s1)+abs(k1)+abs(e1)+abs(f1)==0) or ( abs(s2)+abs(k2)+abs(e2)+abs(f2)==0)):
			return (0.0)
		#sign
		s=s1+s2
		if(s!=1):
		    s=0

		k_max = total_length - 1 - 1
		k_min = -1*(total_length - 1)


		e1 = e1 + k1*(useed)
		e2 = e2 + k2*(useed)

		e=e1+e2
		f=f1*f2

		if(f>=2):
		    f/=2
		    e += 1

		k=int(np.floor(e/useed))

		if(k>k_max):
		    k=k_max
		elif(k<k_min):
		    k=k_min


		if(k>=0):
			if(k==k_max):
				regime_len = k + 1
			else:
				regime_len = k + 2 
		else:
			if(k==k_min):
				regime_len = abs(k)
			else:
				regime_len = abs(k) + 1

		bits_remaining = total_length - 1 - regime_len
		if(bits_remaining>=es):
			es_length = es
		else:
			es_length = bits_remaining


		e=e-k*useed
		e_remaining_max = 2**(es_length) - 1
		if(e>e_remaining_max):
			e=e_remaining_max


		frac_length = total_length - 1 - regime_len - es_length 

		
		f_new=f-1
		for i in range(1,frac_length+1):
		    f_new-=2**(-i)
		    if(f_new<0):
		        f_new+=2**(-i)

		if(s==1):
		    return -1*((f-f_new)*(2**((2**es)*k + e)))
		else:
		    return ((f-f_new)*(2**((2**es)*k + e)))


	def add(self,operand1,operand2):
		total_length = self.length
		es = self.es
		useed= 2**es
		k_max = total_length - 1 - 1
		k_min = -1*(total_length - 1)

		# operand 1 is larger amoung both
		if(abs(operand1)<abs(operand2)):
		    help_=operand1
		    operand1=operand2
		    operand2=help_

		s1,k1,e1,f1=self.extract(operand1)
		s2,k2,e2,f2=self.extract(operand2)

		if((s1+k1+e1+f1==0) or (s2+k2+e2+f2==0)):
		    return float((-1**s1)*f1*(2**((2**es)*k1 + e1)) + (-1**s2)*f2*(2**((2**es)*k2 + e2)))

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

		k=int(np.floor(e/useed))
		if(k>k_max):
		    k=k_max
		elif(k<k_min):
		    k=k_min

		if(k>=0):
			if(k==k_max):
				regime_len = k + 1
			else:
				regime_len = k + 2 
		else:
			if(k==k_min):
				regime_len = abs(k)
			else:
				regime_len = abs(k) + 1

		bits_remaining = total_length - 1 - regime_len
		if(bits_remaining>=es):
			es_length = es
		else:
			es_length = bits_remaining


		e=e-k*useed
		e_remaining_max = 2**(es_length) - 1
		if(e>e_remaining_max):
			e=e_remaining_max
		frac_length = total_length - 1 - regime_len - es_length 
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
		



# length = 8
# es = 2
# posit = posit_arithmatic(length,es)
# b = -0.00
# a = -0.0
# print(posit.extract(b))
# print(posit.extract(a))
# print(posit.add(a,b))
# # print(posit.multiply(a,b))
# print(a+b)
# print(a*b)