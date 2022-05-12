from math import cos, radians, sin, log, atan
def n(N, lamb, t, a):
    tal = ((N*lamb)/(2*t)+cos(a)-1)**2 + (sin(a))**2
    nam = 2*(-(N*lamb)/(2*t)-cos(a)+1)
    return (tal/nam)

def alpha(dL, L0, dT):
    a = dL/(L0*dT)
    return a

def alpha_2(N, lamb, L0, dT):
    a = log(1+(N*lamb)/(L0*2))/dT
    return a

def b(lamb, m, ym, L):
    d = (m*lamb)/atan(ym/L)
    return d



#print(n(50, 532*(10**(-9)), t = 0.00285, radians(9.25)))
#print(alpha(15*532*10**(-9), 0.0808, 4.3))
#print(alpha_2(30, 532*(10**(-9)), 0.0808, 4.3))
#print(b(632.8*10**(-9), 8, 0.0249, 0.873)*10**3)
