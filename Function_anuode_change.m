function [NPCR,UACI] = Function_anuode_change(P,a,b)
P1=P;
[M,N]=size(P);

L=M*N;
P=reshape(P,1,L);
P=double(P);

N0 =1000;
xn=zeros(1,L);
x3 = -0.8;
r3=3.2;
for i = 1:N0 + L
    x3 = cos(r3 / asin(x3));
    if i > N0
        xn(i - N0) = mod(floor(x3* 10^15), 256);
    end
end

yn=xn+1;
zn=xn*(-1);

K1=xn;
K2=yn;
K3=zn;


% xn=zeros(1,L);
% yn=zeros(1,L);
% zn=zeros(1,L);
% wn=zeros(1,L);
% 
% %%超LONRENZ系统               
% K=[1.1 2.2 3.3 4.4 2000];
% x0=K(1);y0=K(2);z0=K(3);w0=K(4);
% N0=K(5);
% h=0.002;a=10;b=8/3;c=28;r=-1;
% 
% for i=1:N0+L
% 
%      K11=a*(y0-x0)+w0;      K12=a*(y0-(x0+K11*h/2))+w0;
%      K13=a*(y0-(x0+K12*h/2))+w0; K14=a*(y0-(x0+K13*h))+w0;
%      x1=x0+(K11+K12+K13+K14)*h/6;
% 
%      K21=c*x1-y0-x1*z0;      K22=c*x1-(y0+K21*h/2)-x1*z0;
%      K23=c*x1-(y0+K22*h/2)-x1*z0; K24=c*x1-(y0+K23*h/2)-x1*z0;
%      y1=y0+(K21+K22+K23+K24)*h/6;
% 
%      K31=x1*y1-b*z0;      K32=x1*y1-b*(z0+K31*h/2);
%      K33=x1*y1-b*(z0+K32*h/2); K34=x1*y1-b*(z0+K33*h/2);
%      z1=z0+(K31+K32+K33+K34)*h/6;
% 
%      K41=-y1*z1+r*w0;      K42=-y1*z1+r*(w0+K41*h/2);
%      K43=-y1*z1+r*(w0+K42*h/2); K44=-y1*z1+r*(w0+K43*h/2);
%      w1=w0+(K41+K42+K43+K44)*h/6;
% 
%      x0=x1;y0=y1;z0=z1;w0=w1;
%      if i>N0
%          xn(i-N0)=x1;
%          yn(i-N0)=y1;
%          zn(i-N0)=z1;
%          wn(i-N0)=w1;
%      end
% end
%K1=mod(floor(xn*10^6),256);
%K2=mod(floor(yn*10^6),256);
% K3=mod(floor(zn*10^6),256);



%a=15;b=85;
%5000000000000




%%第二轮从左到右
C=zeros(1,L);
S=zeros(1,L); 
T=zeros(1,L);

C(1)=mod(1*P(1)+a*K1(1)+K2(1),256);
T(1)=mod(b*P(1)+(a*b+1)*K1(1)+K3(1),256);
S(2)=mod(T(1)+P(2),256);

for i=2:L-1
    C(i)=mod(1*S(i)+a*K1(i)+K2(i),256);
    T(i)=mod(b*S(i)+(a*b+1)*K1(i)+K3(i),256);
    S(i+1)=mod(T(i)+P(i+1),256);

end
C(L)=mod(1*S(L)+a*K1(L)+K2(L),256);




%%第二轮从右到左
C1=zeros(1,L);
C1(L)=mod(1*C(L)+a*K1(1)+K2(1),256);
T(L)=mod(b*C(L)+(a*b+1)*K1(1)+K3(1),256);
S(L-1)=mod(T(L)+C(L-1),256);

for i=L-1:-1:2
    C1(i)=mod(1*S(i)+a*K1(L-i+1)+K2(L-i+1),256);
    T(i)=mod(b*S(i)+(a*b+1)*K1(L-i+1)+K3(L-i+1),256);
    S(i-1)=mod(T(i)+C(i-1),256);

end
C1(1)=mod(1*S(1)+a*K1(L)+K2(L),256);


C1=uint8(reshape(C1,M,N));
C1=uint8(C1);



[NPCR,UACI] = function_NPCRUACI(C1, P1) ;




end