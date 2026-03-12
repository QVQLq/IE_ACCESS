clear
L1 = 6;
xn = zeros(1, L1);
yn = zeros(1, L1);
x1 = 0.8;
y1 = 0.8;

m=512;

N0=2000;
x1 =-0.8;
r1=0.9;
for i = 1:N0 + L1
    x1 = 25*cos(exp(x1)^2 + y1);
    y1= 25*cos(y1*(1-x1^x1));
    disp(x1)
    if i > N0
        xn(i - N0) = x1;
        q(i - N0) = mod(floor(real(x1)*10^15), m*m)+1;
    end
end








% x1 =-0.8;
% r1=0.9;
% for i = 1:N0 + L1
%     x1 = cos(r1 / asin(x1));
%     if i > N0
%         xn(i - N0) = x1;
%         q(i - N0) = mod(floor(x1*10^15), m*m)+1;
%     end
% end
% 