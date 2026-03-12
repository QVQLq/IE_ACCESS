function l=Correlation_of_adjacent_pixels(image,choose,n)
%抽取n对相邻像素
%choose 选择1水平，2垂直，3对角
%n 抽样对数
image=double(image);
[M,N]=size(image);%M行N列
 
x_coor(1,:)=randi([1  N],1,n);%x序列x坐标
x_coor(2,:)=randi([1  M],1,n);%x序列y坐标
y_coor=ones(2,n);%y序列坐标
 
 
if choose==1
%水平
for i=1:n
    if x_coor(1,i)==N
        y_coor(1,i)=1;
    end
    if x_coor(1,i)<N
        y_coor(1,i)=x_coor(1,i)+1;
    end
    y_coor(2,i)=x_coor(2,i);
end
end
 
 
if choose==2
%垂直
for i=1:n
    if x_coor(2,i)==M
        y_coor(2,i)=1;
    end
    if x_coor(2,i)<M
        y_coor(2,i)=x_coor(2,i)+1;
    end
    y_coor(1,i)=x_coor(1,i);
end
end
 
 
if choose==3
%对角
for i=1:n
    if x_coor(1,i)==N
        y_coor(1,i)=1;
    end
    if x_coor(1,i)<N
        y_coor(1,i)=x_coor(1,i)+1;
    end
    
    if x_coor(2,i)==M
        y_coor(2,i)=1;
    end
    if x_coor(2,i)<M
        y_coor(2,i)=x_coor(2,i)+1;
    end
end
end
 
x=ones(1,n);
y=ones(1,n);
%获取像素值
for i=1:n
    x(i)=image(x_coor(2,i),x_coor(1,i));
    y(i)=image(y_coor(2,i),y_coor(1,i));
end
 
l=coefficient_of_association(x,y);