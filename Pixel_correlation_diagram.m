function s=Pixel_correlation_diagram(choose,img)
%choose 1.水平相关 2.垂直相关 3.对角相关
[M,N]=size(img);%M行N列
x=ones(1,M*N);
y=ones(1,M*N);
num=1;
if choose==1
    for i=1:M
        for j=1:N
            x(num)=img(i,j);
            if j==N
                y(num)=img(i,1);
            end
            if j<N
                y(num)=img(i,j+1);
            end
            num=num+1;
        end
    end
end

if choose==2
    for i=1:M
        for j=1:N
            x(num)=img(i,j);
            if i==M
                y(num)=img(1,j);
            end
            if i<M
                y(num)=img(i+1,j);
            end
            num=num+1;
        end
    end
end

if choose==3
    for i=1:M
        for j=1:N
            x(num)=img(i,j);
            if i<M && j<N
                y(num)=img(i+1,j+1);
            end
            if i<M && j==N
                y(num)=img(i+1,1);
            end
            if i==M && j<N
                y(num)=img(1,j+1);
            end
            if i==M && j==N
                y(num)=img(1,1);
            end
            num=num+1;
        end
    end
end

s=ones(2,M*N);
s(1,:)=x;
s(2,:)=y;