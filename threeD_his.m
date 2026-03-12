clc; clear; close all;


P=imread('e1.png');

K=[0.5,0.6,0.7,2000];

%% 测试加密时间

tic;
en_img=P;
toc;
 


% 设置标题和轴标签
% title('3D Bar Plot');
% xlabel('X');
% ylabel('Y');
% zlabel('Value');
% figure(4);imhist(img4(:));set(gca,'fontsize',18);set(gca,'YLim',[0 2400]);
% figure(5);imhist(img5(:));set(gca,'fontsize',18);set(gca,'YLim',[0 2400]);
% figure(6);imhist(img6(:));set(gca,'fontsize',18);set(gca,'YLim',[0 2400]);
%%
% 假设你的矩阵名为matrix，大小为512x512x3
matrix=en_img;
normalized_img=en_img;
% 创建X和Y的网格
[X, Y] = meshgrid(1:size(matrix, 2), 1:size(matrix, 1));

% % 创建一个新的图窗
% figure(1);
% 
% % 绘制红色通道
% 
% h=bar3(P);
% colormap jet;
% 
% colorbar;
% shading interp; % 使用插值填充颜色
% set(h, 'FaceColor', 'interp', 'EdgeColor', 'none');
% hold on;

figure(2);
h=bar3(en_img);
% colormap parula;
colormap summer;
colorbar;
shading interp; % 使用插值填充颜色
set(h, 'FaceColor', 'interp', 'EdgeColor', 'none');
hold on;

h=bar3(en_img);
% colormap parula;
colormap autumn;
colorbar;
shading interp; % 使用插值填充颜色
set(h, 'FaceColor', 'interp', 'EdgeColor', 'none');
hold on;

h=bar3(en_img);
% colormap parula;
colormap winter;
colorbar;
shading interp; % 使用插值填充颜色
set(h, 'FaceColor', 'interp', 'EdgeColor', 'none');
hold on;



saveas(gcf, 'k1.png');
% 读取图像并裁剪成正方形
im = imread('k1.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 150;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
%imwrite(im_cropped, 'h2.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'e1_his.png');  % 保存调整大小后的图像






% 
% 绘制绿色通道
% green_channel = matrix(:, :, 2);
% mesh(X, Y, green_channel);
% % colormap gray; % 设置色图为灰度


% 
% % 绘制蓝色通道
% blue_channel = matrix(:, :, 3);
% mesh(X, Y, blue_channel);
% % colormap gray; % 设置色图为灰度

% 设置图例
% legend('Red Channel', 'Green Channel', 'Blue Channel');

% 设置标题
% title('RGB Channels');

% 调整图窗尺寸
% set(gcf, 'Position', [100, 100, 800, 600]);
% 调整子图间距
% subplot_adjust = gcf;
% subplot_adjust.Children(1).Position = [0.05, 0.1, 0.25, 0.8];
% subplot_adjust.Children(2).Position = [0.375, 0.1, 0.25, 0.8];
% subplot_adjust.Children(3).Position = [0.7, 0.1, 0.25, 0.8];

% 保存图像
% saveas(gcf, 'rgb_channels_plot.png');