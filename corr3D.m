% 读取RGB彩色照片
%随机选取图像A中相邻的N个像素点，分别计算在水平，垂直，正对角和反对角方向上的相关系数
clear all
close all
img11_RGB = imread('img-00025-00001.jpg'); 
img22_RGB = imread('img-00029-00001.jpg'); 
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));

% 定义测试像素数量
N=20000;

% 计算图像像素相关性
[r1_1_R,u1_1_R,v1_1_R,u2_1_R,v2_1_R,u3_1_R,v3_1_R,u4_1_R,v4_1_R]=ImCoef(IMG1(:,:,1),N);
[r1_2_R,u1_2_R,v1_2_R,u2_2_R,v2_2_R,u3_2_R,v3_2_R,u4_2_R,v4_2_R]=ImCoef(IMG1(:,:,2),N);
[r1_3_R,u1_3_R,v1_3_R,u2_3_R,v2_3_R,u3_3_R,v3_3_R,u4_3_R,v4_3_R]=ImCoef(IMG1(:,:,3),N);
[r1_4_R,u1_4_R,v1_4_R,u2_4_R,v2_4_R,u3_4_R,v3_4_R,u4_4_R,v4_4_R]=ImCoef(IMG1(:,:,4),N);
[r1_5_R,u1_5_R,v1_5_R,u2_5_R,v2_5_R,u3_5_R,v3_5_R,u4_5_R,v4_5_R]=ImCoef(IMG1(:,:,5),N);
[r1_6_R,u1_6_R,v1_6_R,u2_6_R,v2_6_R,u3_6_R,v3_6_R,u4_6_R,v4_6_R]=ImCoef(IMG1(:,:,6),N);

% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u1_1_R)), u1_1_R, v1_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u1_2_R)), u1_2_R, v1_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u1_3_R)), u1_3_R, v1_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u1_4_R)), u1_4_R, v1_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u1_5_R)), u1_5_R, v1_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u1_6_R)), u1_6_R, v1_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in horizontal direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_horizontal_e.png');

% 图像相邻像素相关性函数
function [r,u1,v1,u2,v2,u3,v3,u4,v4]=ImCoef(A,N)
A=double(A);[m,n]=size(A);r=zeros(1,4);
x1=mod(floor(rand(1,N)*10^10),m-1)+1;
x2=mod(floor(rand(1,N)*10^10),m)+1;
x3=mod(floor(rand(1,N)*10^10),m-1)+2;
y1=mod(floor(rand(1,N)*10^10),n-1)+1;
y2=mod(floor(rand(1,N)*10^10),n)+1;
u1=zeros(1,N);u2=zeros(1,N);u3=zeros(1,N);u4=zeros(1,N);
v1=zeros(1,N);v2=zeros(1,N);v3=zeros(1,N);v4=zeros(1,N);
for i=1:N
    u1(i)=A(x1(i),y2(i));v1(i)=A(x1(i)+1,y2(i));
    u2(i)=A(x2(i),y1(i));v2(i)=A(x2(i),y1(i)+1);
    u3(i)=A(x1(i),y1(i));v3(i)=A(x1(i)+1,y1(i)+1);
    u4(i)=A(x3(i),y1(i));v4(i)=A(x3(i)-1,y1(i)+1);
end
r(1)=mean((u1-mean(u1)).*(v1-mean(v1)))/(std(u1,1)*std(v1,1));
r(2)=mean((u2-mean(u2)).*(v2-mean(v2)))/(std(u2,1)*std(v2,1));
r(3)=mean((u3-mean(u3)).*(v3-mean(v3)))/(std(u3,1)*std(v3,1));
r(4)=mean((u4-mean(u4)).*(v4-mean(v4)))/(std(u4,1)*std(v4,1));
end


% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u2_1_R)), u2_1_R, v2_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u2_2_R)), u2_2_R, v2_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u2_3_R)), u2_3_R, v2_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u2_4_R)), u2_4_R, v2_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u2_5_R)), u2_5_R, v2_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u2_6_R)), u2_6_R, v2_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in vertical direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_vertical_e.png');




% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u3_1_R)), u3_1_R, v3_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u3_2_R)), u3_2_R, v3_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u3_3_R)), u3_3_R, v3_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u3_4_R)), u3_4_R, v3_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u3_5_R)), u3_5_R, v3_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u3_6_R)), u3_6_R, v3_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in diagonal direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_diagonal_e.png');



[r1_1_R,u1_1_R,v1_1_R,u2_1_R,v2_1_R,u3_1_R,v3_1_R,u4_1_R,v4_1_R]=ImCoef(img11_RGB(:,:,1),N);
[r1_2_R,u1_2_R,v1_2_R,u2_2_R,v2_2_R,u3_2_R,v3_2_R,u4_2_R,v4_2_R]=ImCoef(img11_RGB(:,:,2),N);
[r1_3_R,u1_3_R,v1_3_R,u2_3_R,v2_3_R,u3_3_R,v3_3_R,u4_3_R,v4_3_R]=ImCoef(img11_RGB(:,:,3),N);
[r1_4_R,u1_4_R,v1_4_R,u2_4_R,v2_4_R,u3_4_R,v3_4_R,u4_4_R,v4_4_R]=ImCoef(img22_RGB(:,:,1),N);
[r1_5_R,u1_5_R,v1_5_R,u2_5_R,v2_5_R,u3_5_R,v3_5_R,u4_5_R,v4_5_R]=ImCoef(img22_RGB(:,:,2),N);
[r1_6_R,u1_6_R,v1_6_R,u2_6_R,v2_6_R,u3_6_R,v3_6_R,u4_6_R,v4_6_R]=ImCoef(img22_RGB(:,:,3),N);






% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u1_1_R)), u1_1_R, v1_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u1_2_R)), u1_2_R, v1_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u1_3_R)), u1_3_R, v1_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u1_4_R)), u1_4_R, v1_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u1_5_R)), u1_5_R, v1_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u1_6_R)), u1_6_R, v1_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in horizontal direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_horizontal_o.png');

% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u2_1_R)), u2_1_R, v2_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u2_2_R)), u2_2_R, v2_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u2_3_R)), u2_3_R, v2_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u2_4_R)), u2_4_R, v2_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u2_5_R)), u2_5_R, v2_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u2_6_R)), u2_6_R, v2_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in vertical direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_vertical_o.png');




% 绘制图像
figure;

% 绘制像素相关性图
% 绘制第一个面
h1 = plot3(ones(size(u3_1_R)), u3_1_R, v3_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(2*ones(size(u3_2_R)), u3_2_R, v3_2_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(3*ones(size(u3_3_R)), u3_3_R, v3_3_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第四个面
h4 = plot3(4*ones(size(u3_4_R)), u3_4_R, v3_4_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第五个面
h5 = plot3(5*ones(size(u3_5_R)), u3_5_R, v3_5_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第六个面
h6 = plot3(6*ones(size(u3_6_R)), u3_6_R, v3_6_R, 'r.', 'linewidth', 3, 'markersize', 3);

% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
set(h4, 'Color', [0.3, 0.6, 0.1]);
set(h5, 'Color', [0.5, 0.1, 0.8]);
set(h6, 'Color', [0.5, 0.5, 0.5]);

% 设置坐标轴标签等
xlabel('Image');
ylabel('Pixel value');
zlabel('Adjacent pixel value');
title('Pixel correlation in diagonal direction');
ax = gca;
ax.XTick = [1, 2, 3, 4, 5, 6];
ax.XTickLabel = {'IMG1', 'IMG2', 'IMG3', 'IMG4', 'IMG5', 'IMG6'}; % 设置新的刻度标签

% 保存图像为PNG格式
saveas(gcf, 'scatter_plot_diagonal_o.png');

