function r= rxy_f( P )
%r是向量，用来保存水平、垂直、正对角和反对角方向上的相关系数
P=double(P);   [m,n]=size(P); r=zeros(1,4);
u1=zeros(1,m*(n-1)); u2=zeros(1,(m-1)*n); u3=zeros(1,(m-1)*(n-1)); u4=zeros(1,(m-1)*(n-1));
v1=zeros(1,m*(n-1)); v2=zeros(1,(m-1)*n); v3=zeros(1,(m-1)*(n-1)); v4=zeros(1,(m-1)*(n-1));
 k1=1;k2=1;k3=1;k4=1;
for i=1:m
    for j=1:n-1
    %u1和v1保存水平方向上的像素点对
    u1(k1)=P(i,j); v1(k1)=P(i,j+1);
    k1=k1+1;
    end
end
for i=1:m-1
    for j=1:n
    %u2和v2保存垂直方向上的像素点对
    u2(k2)=P(i,j); v2(k2)=P(i+1,j);
    k2=k2+1;
    end
end
for i=2:m
    for j=1:n-1
    %u3和v3保存正对角方向上的像素点对
    u3(k3)=P(i,j); v3(k3)=P(i-1,j+1);
    k3=k3+1;
    end
end
for i=1:m-1
    for j=1:n-1
    %u4和v4保存反对角方向上的像素点对
    u4(k4)=P(i,j); v4(k4)=P(i+1,j+1);
    k4=k4+1;
    end
end

%调用计算公式计算相关系数,其中a.*b是将a矩阵与b矩阵中相同位置的元素相乘，两个矩阵的大小必须相等
r(2)=mean((u1-mean(u1)).*(v1-mean(v1)))/(std(u1,1)*std(v1,1));
r(1)=mean((u2-mean(u2)).*(v2-mean(v2)))/(std(u2,1)*std(v2,1));
r(3)=mean((u3-mean(u3)).*(v3-mean(v3)))/(std(u3,1)*std(v3,1));
r(4)=mean((u4-mean(u4)).*(v4-mean(v4)))/(std(u4,1)*std(v4,1));

end

