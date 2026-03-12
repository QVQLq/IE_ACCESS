function [b] = zhongzhilvbo(x)

n=3;    %模板大小
[height, width]=size(x);   %获取图像的尺寸（n小于图片的宽高）
x1=double(x);  %数据类型转换
x2=x1;  %转换后的数据赋给x2
for i=1:height-n+1  
    for j=1:width-n+1  
        c=x1(i:i+(n-1),j:j+(n-1)); %在x1中从头取模板大小的块赋给c  
        e=c(1,:);      %e中存放是c矩阵的第一行  
        for u=2:n  %将c中的其他行元素取出来接在e后使e为一个行矩阵 
            e=[e,c(u,:)];          
        end  
        med=median(e);      %取一行的中值  
        x2(i+(n-1)/2,j+(n-1)/2)=med;   %将模板各元素的中值赋给模板中心位置的元素  
    end  
end    
d=uint8(x2);  %未被赋值的元素取原值 
x0=rgb2gray(x);  %灰度处理，灰度处理后的图像是二维矩阵
b=medfilt2(x0,[n,n]);  %matlab中自带值滤波函数




end

