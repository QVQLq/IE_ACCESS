function C1 = Function_anuode_differ(P,a,b)
digits(50); % 设置默认精度为50位小数
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




%%第二轮从左到右
C=zeros(1,L);
S=zeros(1,L); 
T=zeros(1,L);

C(1)=mod(1*P(1)+a*K1(1)+K2(1),256);


T(1)=mod(b*P(1)+(a*b+1)*K1(1)+K3(1),256);
S(2)=mod(T(1)+P(2),256);
% fprintf('P%d: %d,C%d: %d, T%d: %d, S%d: %d\n', 1,P(1),1, C(1), 1, T(1), 1+1, S(1+1));
for i=2:L-1
    C(i)=mod(1*S(i)+a*K1(i)+K2(i),256);
    T(i)=mod(b*S(i)+(a*b+1)*K1(i)+K3(i),256);
    S(i+1)=mod(T(i)+P(i+1),256);
% fprintf('P%d: %d,C%d: %d, T%d: %d, S%d: %d\n',i,P(i), i, C(i), i, T(i), i+1, S(i+1));


end
%disp(mod(b*S(3)+(a*b+1)*K1(3)+K3(3),256))


% disp(mod(T(5)+P(6),256))
% disp(mod(b*((b*(T(3)+P(4))+(a*b+1)*K1(4)+K3(4))+P(5))+(a*b+1)*K1(5)+K3(5),256))
% 
% 
% disp(mod(b*(T(3)+P(4))+(a*b+1)*K1(4)+K3(4),256))
% 
% 
% 
% 
% disp(mod(b^2*T(3)+b^2*P(4)+(a*b+1)*b*K1(4)+b*K3(4)+b*P(5)+(a*b+1)*K1(5)+K3(5),256))
% 
% 
% disp(b^2*T(3)+b^2*P(4)+(a*b+1)*b*K1(4)+b*K3(4)+b*P(5)+(a*b+1)*K1(5)+K3(5))

 % c=1;  %2-4
 % disp(b^2*T(c)+b^2*P(c+1)+(a*b+1)*b*K1(c+1)+b*K3(c+1)+b*P(c+2)+(a*b+1)*K1(c+2)+K3(c+2))
 % disp( mod(b^2*T(c)+b^2*P(c+1)+(a*b+1)*b*K1(c+1)+b*K3(c+1)+b*P(c+2)+(a*b+1)*K1(c+2)+K3(c+2),256))


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








end