function P = Decrypt_Function_anuode(C1)
%%用的是论文的方程
[M,N]=size(C1);
L=M*N;
C1=reshape(C1,1,L);
C1=double(C1);

% N0 =1000;
% xn=zeros(1,L);
% x3 = -0.8;
% r3=3.2;
% for i = 1:N0 + L
%     x3 = cos(r3 / asin(x3));
%     if i > N0
%         xn(i - N0) = mod(floor(x3* 10^15), 256);
%     end
% end
% 
% yn=xn+1;
% zn=xn*(-1);
% 
% K1=xn;
% K2=yn;
% K3=zn;

% 
N0 =1000;
xn=zeros(1,L);yn=zeros(1,L);
x3 = -0.8;
y3 = -0.8;
a=25;b=20;
for i = 1:N0 + L/2
    x3 = a*cos(exp(1*x3^2)+y3);  
    y3 = b*cos(y3*(1-x3^2));
    if i > N0
        xn(i - N0) = mod(floor(x3* 10^15), 256);
        yn(i - N0) = mod(floor(x3* 10^10), 256);
    end
end

xn=horzcat(xn,yn);
yn=xn+1;
zn=xn*(-1);

K1=xn;
K2=yn;
K3=zn;






a=15;b=85;

%5000000000000



 %a=9999999;b=-9999999;
 %a=-10000000;b=10000000;


% xn=zeros(1,L);
% yn=zeros(1,L);
% zn=zeros(1,L);
% wn=zeros(1,L);
%%超LONRENZ系统               
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
%K3=mod(floor(zn*10^6),256);





%%  大综方法
% C(L)=mod(C1(L)-H(1,2)*K1(1)-K2(1),256);
% T(L)=mod(H(2,1)*C(L)+H(2,2)*K1(1)+K3(1),256);
% 
%  for k=L-1:-1:1
%  S(k)=mod(C1(k)-H(1,2)*K1(L+1-k)-K2(L+1-k),256);
%  C(k)=mod(S(k)-T(k+1),256);
%  T(k)=mod(H(2,1)*S(k)+H(2,2)*K1(L+1-k)+K3(L+1-k),256);
% 
%  end
% 
% 
% P(1)=mod(C(1)-H(1,2)*K1(1)-K2(1),256);
% T(1)=mod(H(2,1)*P(1)+H(2,2)*K1(1)+K3(1),256);
% 
% 
% 
% for k=2:L
% S(k)=mod(C(k)-H(1,2)*K1(k)-K2(k),256);
% 
% T(k)=mod(H(2,1)*S(k)+H(2,2)*K1(k)+K3(k),256);
% 
% P(k)=mod(S(k)-T(k-1),256);
% 
% end




%小方法（针对阿诺德映射）
% C1知道求C
 T(L)=mod(K1(1)+(b)*(C1(L)-K2(1))+(1)*(K3(1)),256);
 C(L)=mod((a*b+1)*(C1(L)-K2(1))+(-a)*(T(L)-K3(1)),256);


for n=L-1:-1:1

 T(n)=mod(K1(L+1-n)+(b)*(C1(n)-K2(L+1-n))+(1)*(K3(L+1-n)),256);
 S(n)=mod((a*b+1)*(C1(n)-K2(L+1-n))+(-a)*(T(n)-K3(L+1-n)),256);
 C(n)=mod(S(n)-T(n+1),256);

end


P=zeros(1,L);

% C知道求P
 T(1)=mod(K1(1)+(b)*(C(1)-K2(1))+(1)*(K3(1)),256);
 P(1)=mod((a*b+1)*(C(1)-K2(1))+(-a)*(T(1)-K3(1)),256);

for n=2:L

 T(n)=mod(K1(n)+(b)*(C(n)-K2(n))+(1)*(K3(n)),256);
 S(n)=mod((a*b+1)*(C(n)-K2(n))+(-a)*(T(n)-K3(n)),256);
 P(n)=mod(S(n)-T(n-1),256);



P=uint8(reshape(P,M,N));

end

