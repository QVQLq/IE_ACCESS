close all
clear

img11_RGB = imread('RGB_Lena.bmp'); 
img22_RGB = imread('RGB_baboon.bmp');


 % img11_RGB = imread('RGB256_Couple.tiff'); 
 % img22_RGB = imread('RGB256_Female.tiff');

% img11_RGB(:,:,1)=imread('GERY_Airplane.tiff'); 
% img11_RGB(:,:,2)=imread('GREY_Aerial.tiff'); 
% img11_RGB(:,:,3)=imread('GREY_APC.tiff'); 
% img22_RGB(:,:,1)=imread('GREY_Truck.tiff'); 
% img22_RGB(:,:,2)=imread('GREY_tank.tiff'); 
% img22_RGB(:,:,3)=imread('GREY_Couple.tiff'); 
% img22_RGB(:,:,3)=imread('GREY_Baboon.bmp'); 
% img22_RGB(:,:,3)=imread('GREY_pepperplain.bmp'); 

% P1 = imread('GREY256_Aerial.tiff'); 
% P2= imread('GREY256_Airplane.tiff');
% P3= imread('GREY256_ChemicalPlant.tiff');
% P4= imread('GREY256_Cloack.tiff');
% P5= imread('GREY256_Moon surface.tiff');
% P6= imread('GREY256_ResolutionChart.tiff');
% 
%  img11_RGB = cat(3,P1,P2,P3); 
%  img22_RGB = cat(3,P4,P5,P6);

%option
%1=测试NPCR,UACI
%2=高斯噪声
%3=椒盐噪声
%4=裁剪攻击
%5=水平垂直对角相关  
%6=信息熵
%7=直方图分析
%8=相邻像素相关性图

option=3;


switch option

case 1


%生成6*512*512的置乱加扩散的IMG1
IMG1=Shengchengtupian_Jiami(img11_RGB,img22_RGB);
n=1;
NPCR_sum=0;
UACI_sum=0;

for k=1:n

img33_RGB = change_one_pixel(img11_RGB);IMG2=Shengchengtupian_Jiami(img33_RGB,img22_RGB);

%连成512*（512*6）的Horz_1和Horz_2
Horz_1=horzcat(IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3),IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6));
Horz_2=horzcat(IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3),IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6));


%检测其NPCR,UACI
[NPCR,UACI] = function_NPCRUACI(Horz_1, Horz_2) ;
NPCR_sum=NPCR+NPCR_sum;
UACI_sum=UACI+UACI_sum;
end
NPCR_ave=double(NPCR_sum/n);
UACI_ave=double(UACI_sum/n);
 disp(NPCR_ave)
 disp(UACI_ave)








 case 2

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);

img3_RGB = img11_RGB; 
img4_RGB = img22_RGB;
[IMG2] = Shengchengtupian_Jiami(img3_RGB,img4_RGB);

%高斯噪声
kk=IMG2(:,:,1);
IMG2(:,:,1) =  (imnoise(IMG2(:,:,1), 'gaussian',  0,0.01));
IMG2(:,:,2) =  (imnoise(IMG2(:,:,2), 'gaussian',  0,0.01));
IMG2(:,:,3)=  (imnoise(IMG2(:,:,3), 'gaussian',  0,0.01));
IMG2(:,:,4) =  (imnoise(IMG2(:,:,4), 'gaussian', 0, 0.01));
IMG2(:,:,5) =  (imnoise(IMG2(:,:,5), 'gaussian',  0,0.01));
IMG2(:,:,6) = (imnoise(IMG2(:,:,6), 'gaussian',  0,0.01));



jiamihou_3=uint8(cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3)));
jiamihou_4=uint8(cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6)));
[img33_RGB_b,img44_RGB_b] = Shengchengtupian_Jiemi(IMG2);



figure
subplot(3, 4, 1)
imshow(img11_RGB )
%title('第一张加密前的图像')

subplot(3, 4, 2)
imshow(img22_RGB )
%title('第二张加密前的图像')


subplot(3, 4, 3)
imshow(img3_RGB )
%title('第一张加密前的图像')

subplot(3, 4, 4)
imshow(img4_RGB )
%title('第二张加密前的图像')



subplot(3, 4, 5)
imshow(jiamihou_1)
%title('第一张加密后的图像')

subplot(3, 4, 6)
imshow(jiamihou_2)
%title('第二张加密后的图像')

subplot(3, 4, 7)
imshow(jiamihou_3)
%title('第一张高斯噪声攻击后的加密后的图像')

subplot(3, 4, 8)
imshow(jiamihou_4)
%title('第二张高斯噪声攻击后的加密后的图像')

subplot(3, 4, 9)
imshow(uint8(img11_RGB_b))
%title('第一张解密后的图像')

subplot(3, 4, 10)
imshow(uint8(img22_RGB_b))
%title('第二张解密后的图像')


subplot(3, 4, 11)
imshow(uint8(img33_RGB_b))
%title('第一张高斯噪声攻击后的解密后的图像')

subplot(3, 4, 12)
imshow(uint8(img44_RGB_b))
%title('第二张高斯噪声攻击后的解密后的图像')




 case 3
%椒盐噪声
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);


img3_RGB = img11_RGB; 
img4_RGB = img22_RGB;
[IMG2] = Shengchengtupian_Jiami(img3_RGB,img4_RGB);



% IMG2(:,:,1) =  (imnoise(IMG2(:,:,1), 'salt & pepper', 0.1));
% IMG2(:,:,2) =  (imnoise(IMG2(:,:,2), 'salt & pepper', 0.1));
% IMG2(:,:,3)=  (imnoise(IMG2(:,:,3), 'salt & pepper', 0.1));
% IMG2(:,:,4) =  (imnoise(IMG2(:,:,4), 'salt & pepper', 0.1));
% IMG2(:,:,5) =  (imnoise(IMG2(:,:,5), 'salt & pepper', 0.1));
% IMG2(:,:,6) = (imnoise(IMG2(:,:,6), 'salt & pepper', 0.1));

jiamihou_3=uint8(cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3)));
jiamihou_4=uint8(cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6)));
[img33_RGB_b,img44_RGB_b] = Shengchengtupian_Jiemi(IMG2);



figure
subplot(3, 4, 1)
imshow(img11_RGB )
%title('第一张加密前的图像')

subplot(3, 4, 2)
imshow(img22_RGB )
%title('第二张加密前的图像')


subplot(3, 4, 3)
imshow(img3_RGB )
%title('第一张加密前的图像')

subplot(3, 4, 4)
imshow(img4_RGB )
%title('第二张加密前的图像')



subplot(3, 4, 5)
imshow(jiamihou_1)
%title('第一张加密后的图像')

subplot(3, 4, 6)
imshow(jiamihou_2)
%title('第二张加密后的图像')

subplot(3, 4, 7)
imshow(jiamihou_3)
%title('第一张椒盐噪声攻击后的加密后的图像')

subplot(3, 4, 8)
imshow(jiamihou_4)
%title('第二张椒盐噪声攻击后的加密后的图像')

subplot(3, 4, 9)
imshow(uint8(img11_RGB_b))
%title('第一张解密后的图像')

subplot(3, 4, 10)
imshow(uint8(img22_RGB_b))
%title('第二张解密后的图像')


subplot(3, 4, 11)
imshow(uint8(img33_RGB_b))
%title('第一张椒盐噪声攻击后的解密后的图像')

subplot(3, 4, 12)
imshow(uint8(img44_RGB_b))
%title('第二张椒盐噪声攻击后的解密后的图像')

imwrite(jiamihou_3,'1.png')
imwrite(jiamihou_4,'2.png')
imwrite(img33_RGB_b,'3.png')
imwrite(img44_RGB_b,'4.png')





case 4

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);


img3_RGB = img11_RGB; 
img4_RGB = img22_RGB;
[IMG2] = Shengchengtupian_Jiami(img3_RGB,img4_RGB);


n_cj=128;
nk=150;
%裁剪攻击
I_r_1 =IMG2(:,:,1);
%I_r_1(1+n_cj:n_cj*3,1+n_cj:n_cj*3)=0;
I_r_1(150:512-150,150:512-150)=0;
I_g_1 =IMG2(:,:,2);
I_g_1(150:512-150,150:512-150)=0;
I_b_1 =IMG2(:,:,3);
I_b_1(150:512-150,150:512-150)=0;


I_r_2 =IMG2(:,:,4);
I_r_2(150:512-150,150:512-150)=0;
I_g_2 =IMG2(:,:,5);
I_g_2(150:512-150,150:512-150)=0;
I_b_2 =IMG2(:,:,6);
I_b_2(150:512-150,150:512-150)=0;



img1111=cat(3,I_r_1,I_g_1,I_b_1);
img2222=cat(3,I_r_2,I_g_2,I_b_2);

imwrite(img1111,'test1.png')
imwrite(img2222,'test2.png')


%三色通道合并
IMG2(:,:,1) = I_r_1;
IMG2(:,:,2) = I_g_1;
IMG2(:,:,3) = I_b_1;
IMG2(:,:,4) = I_r_2;
IMG2(:,:,5) = I_g_2;
IMG2(:,:,6) = I_b_2;


jiamihou_3=uint8(cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3)));
jiamihou_4=uint8(cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6)));
[img33_RGB_b,img44_RGB_b] = Shengchengtupian_Jiemi(IMG2);

imwrite(img33_RGB_b,'test3.png')
imwrite(img44_RGB_b,'test4.png')



figure
subplot(3, 4, 1)
imshow(img11_RGB )


subplot(3, 4, 2)
imshow(img22_RGB )



subplot(3, 4, 3)
imshow(img3_RGB )


subplot(3, 4, 4)
imshow(img4_RGB )




subplot(3, 4, 5)
imshow(jiamihou_1)


subplot(3, 4, 6)
imshow(jiamihou_2)


subplot(3, 4, 7)
imshow(jiamihou_3)


subplot(3, 4, 8)
imshow(jiamihou_4)


subplot(3, 4, 9)
imshow(uint8(img11_RGB_b))


subplot(3, 4, 10)
imshow(uint8(img22_RGB_b))



subplot(3, 4, 11)
imshow(uint8(img33_RGB_b))


subplot(3, 4, 12)
imshow(uint8(img44_RGB_b))



case 5
   %水平垂直对角相关     

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);


figure

subplot(4, 3, 1);
[x1, y1] = PixelCorrelationDiagram(jiamihou_1(:,:,1));
title('第一张加密前的图像R通道的水平垂直对角相关 ')
plot(x1, y1, '.');


subplot(4, 3, 2);
[x2, y2] = PixelCorrelationDiagram(jiamihou_1(:,:,2));
title('第一张加密前的图像G通道的水平垂直对角相关 ')
plot(x2, y2, '.');

subplot(4, 3, 3);
[x3, y3] = PixelCorrelationDiagram(jiamihou_1(:,:,3));
title('第一张加密前的图像B通道的水平垂直对角相关 ')
plot(x3, y3, '.');

subplot(4, 3, 4);
[x4, y4] = PixelCorrelationDiagram(jiamihou_2(:,:,1));
title('第一张加密前的图像R通道的水平垂直对角相关 ')
plot(x4, y4, '.');

subplot(4, 3, 5);
[x5, y5] = PixelCorrelationDiagram(jiamihou_2(:,:,2));
title('第一张加密前的图像G通道的水平垂直对角相关 ')
plot(x5, y5, '.');

subplot(4, 3, 6);
[x6, y6] = PixelCorrelationDiagram(jiamihou_2(:,:,3));
title('第一张加密前的图像B通道的水平垂直对角相关 ')
plot(x6, y6, '.');

subplot(4, 3, 1);
[x7, y7] = PixelCorrelationDiagram(img11_RGB_b(:,:,1));
title('第一张加密后的图像R通道的水平垂直对角相关 ')
plot(x7, y7, '.');

subplot(4, 3, 2);
[x8, y8] = PixelCorrelationDiagram(img11_RGB_b(:,:,2));
title('第一张加密后的图像G通道的水平垂直对角相关 ')
plot(x8, y8, '.');

subplot(4, 3, 3);
[x9, y9] = PixelCorrelationDiagram(img11_RGB_b(:,:,3));
title('第一张加密后的图像B通道的水平垂直对角相关 ')
plot(x9, y9, '.');

subplot(4, 3, 4);
[x10, y10] = PixelCorrelationDiagram(img22_RGB_b(:,:,1));
title('第一张加密后的图像R通道的水平垂直对角相关 ')
plot(x10, y10, '.');

subplot(4, 3, 5);
[x11, y11] = PixelCorrelationDiagram(img22_RGB_b(:,:,2));
title('第一张加密后的图像G通道的水平垂直对角相关 ')
plot(x11, y11, '.');

subplot(4, 3, 6);
[x12, y12] = PixelCorrelationDiagram(img22_RGB_b(:,:,3));
title('第一张加密后的图像B通道的水平垂直对角相关 ')
plot(x12, y12, '.');


case 6

entropy_1 = entropy(img11_RGB(:,:,1));
entropy_2 = entropy(img11_RGB(:,:,2));
entropy_3 = entropy(img11_RGB(:,:,3));
entropy_4 = entropy(img22_RGB(:,:,1));
entropy_5 = entropy(img22_RGB(:,:,2));
entropy_6 = entropy(img22_RGB(:,:,3));
entropy_7=(entropy_1+entropy_2+entropy_3+entropy_4+entropy_5+entropy_6)/6;

fprintf('加密前图像1的R通道的信息熵1: %f\n', entropy_1);
fprintf('加密前图像1的G通道的信息熵2: %f\n', entropy_2);
fprintf('加密前图像1的B通道的信息熵3: %f\n', entropy_3);
fprintf('加密前图像2的R通道的信息熵2: %f\n', entropy_4);
fprintf('加密前图像2的G通道的信息熵1: %f\n', entropy_5);
fprintf('加密前图像2的B通道的信息熵2: %f\n', entropy_6);
fprintf('加密前两张图像的平均信息熵2: %f\n', entropy_7);


[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);

   
entropy_1 = entropy(IMG1(:,:,1));
entropy_2 = entropy(IMG1(:,:,2));
entropy_3 = entropy(IMG1(:,:,3));
entropy_4 = entropy(IMG1(:,:,4));
entropy_5 = entropy(IMG1(:,:,5));
entropy_6 = entropy(IMG1(:,:,6));
entropy_7=(entropy_1+entropy_2+entropy_3+entropy_4+entropy_5+entropy_6)/6;

fprintf('加密后图像1的R通道的信息熵1: %f\n', entropy_1);
fprintf('加密后图像1的G通道的信息熵2: %f\n', entropy_2);
fprintf('加密后图像1的B通道的信息熵3: %f\n', entropy_3);
fprintf('加密后图像2的R通道的信息熵2: %f\n', entropy_4);
fprintf('加密后图像2的G通道的信息熵1: %f\n', entropy_5);
fprintf('加密后图像2的B通道的信息熵2: %f\n', entropy_6);
fprintf('加密后两张图像的平均信息熵2: %f\n', entropy_7);


case 7  
  %直方图分析

% [IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
% jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
% jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
% [img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);
% 
% 
% % 计算image1的直方图
% [h1_r_1, x1_r_1] = imhist(img11_RGB_b(:,:,1));
% [h1_g_1, x1_g_1] = imhist(img11_RGB_b(:,:,2));
% [h1_b_1, x1_b_1] = imhist(img11_RGB_b(:,:,3));
% 
% % 计算image2的直方图
% [h2_r_1, x2_r_1] = imhist(img11_RGB_b(:,:,1));
% [h2_g_1, x2_g_1] = imhist(img11_RGB_b(:,:,2));
% [h2_b_1, x2_b_1] = imhist(img11_RGB_b(:,:,3));
% 
% 
% 
% 
% 
% % 计算image1的直方图
% [h1_r, x1_r] = imhist(jiamihou_1(:,:,1));
% [h1_g, x1_g] = imhist(jiamihou_1(:,:,2));
% [h1_b, x1_b] = imhist(jiamihou_1(:,:,3));
% 
% % 计算image2的直方图
% [h2_r, x2_r] = imhist(jiamihou_2(:,:,1));
% [h2_g, x2_g] = imhist(jiamihou_2(:,:,2));
% [h2_b, x2_b] = imhist(jiamihou_2(:,:,3));
% 
% 
% 
% 
% 
% % 在一个图形窗口中展示直方图
% figure;
% 
% 
% 
% subplot(2,6,1);
% bar(x1_r_1, h1_r_1, 'r');
% title('原图Image 1 - Red Channel');
% 
% subplot(2,6,2);
% bar(x1_g_1, h1_g_1, 'g');
% title('原图Image 1 - Green Channel');
% 
% subplot(2,6,3);
% bar(x1_b_1, h1_b_1, 'b');
% title('原图Image 1 - Blue Channel');
% 
% subplot(2,6,4);
% bar(x2_r_1, h2_r_1, 'r');
% title('原图Image 2 - Red Channel');
% 
% subplot(2,6,5);
% bar(x2_g_1, h2_g_1, 'g');
% title('原图Image 2 - Green Channel');
% 
% subplot(2,6,6);
% bar(x2_b_1, h2_b_1, 'b');
% title('原图Image 2 - Blue Channel');
% 
% 
% 
% subplot(2,6,7);
% bar(x1_r, h1_r, 'r');
% title('加密后Image 1 - Red Channel');
% 
% subplot(2,6,8);
% bar(x1_g, h1_g, 'g');
% title('加密后Image 1 - Green Channel');
% 
% subplot(2,6,9);
% bar(x1_b, h1_b, 'b');
% title('加密后Image 1 - Blue Channel');
% 
% subplot(2,6,10);
% bar(x2_r, h2_r, 'r');
% title('加密后Image 2 - Red Channel');
% 
% subplot(2,6,11);
% bar(x2_g, h2_g, 'g');
% title('加密后Image 2 - Green Channel');
% 
% subplot(2,6,12);
% bar(x2_b, h2_b, 'b');
% title('加密后Image 2 - Blue Channel');


[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);


% 计算image1的直方图
[h1_r_1, x1_r_1] = imhist(img11_RGB_b(:,:,1));
[h1_g_1, x1_g_1] = imhist(img11_RGB_b(:,:,2));
[h1_b_1, x1_b_1] = imhist(img11_RGB_b(:,:,3));

% 计算image2的直方图
[h2_r_1, x2_r_1] = imhist(img22_RGB_b(:,:,1));
[h2_g_1, x2_g_1] = imhist(img22_RGB_b(:,:,2));
[h2_b_1, x2_b_1] = imhist(img22_RGB_b(:,:,3));





% 计算image1的直方图
[h1_r, x1_r] = imhist(jiamihou_1(:,:,1));
[h1_g, x1_g] = imhist(jiamihou_1(:,:,2));
[h1_b, x1_b] = imhist(jiamihou_1(:,:,3));

% 计算image2的直方图
[h2_r, x2_r] = imhist(jiamihou_2(:,:,1));
[h2_g, x2_g] = imhist(jiamihou_2(:,:,2));
[h2_b, x2_b] = imhist(jiamihou_2(:,:,3));







% 在一个图形窗口中展示直方图

figure(1);
subplot(1,1,1);
hold on;
bar(x1_r_1, h1_r_1, 'r');
bar(x1_g_1, h1_g_1, 'g');
bar(x1_b_1, h1_b_1, 'b');
xlim([0,250])
ylim([0,4500])
title('Histogram of R, G and B');
saveas(gcf, 'h1.png');

% 读取图像并裁剪成正方形
im = imread('h1.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h1.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'h1.png');  % 保存调整大小后的图像





figure(2);
subplot(1,1,1);
hold on;
bar(x2_r_1, h2_r_1, 'r');
bar(x2_g_1, h2_g_1, 'g');
bar(x2_b_1, h2_b_1, 'b');
xlim([0,250])
ylim([0,4500])
title('Histogram of R, G and B');
saveas(gcf, 'h2.png');

% 读取图像并裁剪成正方形
im = imread('h2.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h2.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'h2.png');  % 保存调整大小后的图像



figure(3);
subplot(1,1,1);
hold on;
bar(x1_r, h1_r, 'r');
bar(x1_g, h1_g, 'g');
bar(x1_b, h1_b, 'b');
xlim([0,250])
ylim([0,1200])
title('Histogram of R, G and B');
saveas(gcf, 'h3.png');

% 读取图像并裁剪成正方形
im = imread('h3.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h3.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'h3_resized.png');  % 保存调整大小后的图像



figure(4); 
subplot(1,1,1);
hold on;
bar(x2_r, h2_r, 'r');
bar(x2_g, h2_g, 'g');
bar(x2_b, h2_b, 'b');
xlim([0,250])
ylim([0,1200])
title('Histogram of R, G and B');
saveas(gcf, 'h4.png');

% 读取图像并裁剪成正方形
im = imread('h4.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h3.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'h4.png');  % 保存调整大小后的图像











case 8
%相关系数矩阵

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);



[r1_1_R,u1_1_R,v1_1_R,u2_1_R,v2_1_R,u3_1_R,v3_1_R,u4_1_R,v4_1_R]=ImCoef(img11_RGB(:,:,1),4000);
[r1_1_G,u1_1_G,v1_1_G,u2_1_G,v2_1_G,u3_1_G,v3_1_G,u4_1_G,v4_1_G]=ImCoef(img22_RGB(:,:,2),4000);
[r1_1_B,u1_1_B,v1_1_B,u2_1_B,v2_1_B,u3_1_B,v3_1_B,u4_1_B,v4_1_B]=ImCoef(img22_RGB(:,:,3),4000);


[r1_2_R,u1_2_R,v1_2_R,u2_2_R,v2_2_R,u3_2_R,v3_2_R,u4_2_R,v4_2_R]=ImCoef(img11_RGB(:,:,1),4000);
[r1_2_G,u1_2_G,v1_2_G,u2_2_G,v2_2_G,u3_2_G,v3_2_G,u4_2_G,v4_2_G]=ImCoef(img11_RGB(:,:,2),4000);
[r1_2_B,u1_2_B,v1_2_B,u2_2_B,v2_2_B,u3_2_B,v3_2_B,u4_2_B,v4_2_B]=ImCoef(img11_RGB(:,:,3),4000);


[r1_3_R,u1_3_R,v1_3_R,u2_3_R,v2_3_R,u3_3_R,v3_3_R,u4_3_R,v4_3_R]=ImCoef(jiamihou_1(:,:,1),4000);
[r1_3_G,u1_3_G,v1_3_G,u2_3_G,v2_3_G,u3_3_G,v3_3_G,u4_3_G,v4_3_G]=ImCoef(jiamihou_2(:,:,2),4000);
[r1_3_B,u1_3_B,v1_3_B,u2_3_B,v2_3_B,u3_3_B,v3_3_B,u4_3_B,v4_3_B]=ImCoef(jiamihou_2(:,:,3),4000);


[r1_4_R,u1_4_R,v1_4_R,u2_4_R,v2_4_R,u3_4_R,v3_4_R,u4_4_R,v4_4_R]=ImCoef(jiamihou_1(:,:,1),4000);
[r1_4_G,u1_4_G,v1_4_G,u2_4_G,v2_4_G,u3_4_G,v3_4_G,u4_4_G,v4_4_G]=ImCoef(jiamihou_1(:,:,2),4000);
[r1_4_B,u1_4_B,v1_4_B,u2_4_B,v2_4_B,u3_4_B,v3_4_B,u4_4_B,v4_4_B]=ImCoef(jiamihou_1(:,:,3),4000);


% figure;
% %sgtitle('加密前图1的R通道在水平，垂直，正对角和反对角方向上的相关系数');
% subplot(2,4,1)
% plot(u1_1_R,v1_1_R,'r.','linewidth',3,'markersize',3);
% axis([0 300 0 300]);
% set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',18,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
% %title('加密前水平');set(gca,'FontName','宋体');
% saveas(gcf, '1.png');
% 
% 
% subplot(2,4,2)
% plot(u2_1_R,v2_1_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm,\ity\rm+1)');
% %title('加密前垂直');set(gca,'FontName','宋体');
% saveas(gcf, '2.png');
% 
% subplot(2,4,3)
% plot(u3_1_R,v3_1_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm+1)');
% %title('加密前正对角');set(gca,'FontName','宋体');
% saveas(gcf, '3.png');
% 
% subplot(2,4,4)
% plot(u4_1_R,v4_1_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% %xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm-1,\ity\rm+1)');
% %title('加密前反对角');set(gca,'FontName','宋体');
% saveas(gcf, '4.png');
% 
% subplot(2,4,5)
% plot(u1_3_R,v1_3_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm,\ity\rm+1)');
% %title('加密后水平');set(gca,'FontName','宋体');
% saveas(gcf, '5.png');
% 
% 
% subplot(2,4,6)
% plot(u2_3_R,v2_3_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm,\ity\rm+1)');
% %title('加密后垂直');set(gca,'FontName','宋体');
% saveas(gcf, '6.png');
% 
% subplot(2,4,7)
% plot(u3_3_R,v3_3_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm+1)');
% %title('加密后正对角');set(gca,'FontName','宋体');
% saveas(gcf, '7.png');
% 
% subplot(2,4,8)
% plot(u4_4_R,v4_4_R,'r.','linewidth',3,'markersize',3);
% axis([0 250 0 250]);
% set(gca,'XTick',0:50:250,'YTick',0:50:250,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250'});
% %xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm-1,\ity\rm+1)');
% %title('加密后反对角');set(gca,'FontName','宋体');
% saveas(gcf, '8.png');
% 
% 
% l1=Correlation_of_adjacent_pixels(IMG1(:,:,1),1,10000);
% l2=Correlation_of_adjacent_pixels(IMG1(:,:,1),2,10000);
% l3=Correlation_of_adjacent_pixels(IMG1(:,:,1),3,10000);
% 
% 
% fprintf('垂直: %f\n', l2);
% fprintf('水平: %f\n', l1);
% fprintf('对角: %f\n', l3);


% subplot(1,1,1)
% plot(u1_1_R,v1_1_R,'b.','linewidth',3,'markersize',3);
% xlim([0,300])
% ylim([0,300])
% set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
% set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
% set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% % xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% % ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
% title('Horizontal');
% 
% % 设置坐标轴比例
% aspect_ratio = diff(xlim) / diff(ylim);
% pbaspect([1, aspect_ratio, 1]);
% 
% % 保存图像
% saveas(gcf,'b1.png');
% 
% % 读取图像并裁剪成正方形
% im = imread('b1.png');
% [row, col, ~] = size(im);
% edge_length = min(row, col);
% im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
% 
% % 保存裁剪后的图像
% imwrite(im_cropped, 'b1.png');



figure (1)
subplot(1,1,1)
plot(u1_1_R,v1_1_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Horizontal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b1.png');

% 读取图像并裁剪成正方形
im = imread('b1.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b1.png');



figure (2)
subplot(1,1,1)
plot(u2_1_R,v2_1_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Vertical');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b2.png');

% 读取图像并裁剪成正方形
im = imread('b2.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b2.png');





figure (3)
subplot(1,1,1)
plot(u3_1_R,v3_1_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Diagonal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b3.png');

% 读取图像并裁剪成正方形
im = imread('b3.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b3.png');



figure (4)
subplot(1,1,1)
plot(u4_1_R,v4_1_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Anti diagonal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b4.png');

% 读取图像并裁剪成正方形
im = imread('b4.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b4.png');


figure (5)
subplot(1,1,1)
plot(u1_3_R,v1_3_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Horizontal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b5.png');

% 读取图像并裁剪成正方形
im = imread('b5.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b5.png');


figure (6)
subplot(1,1,1)
plot(u2_3_R,v2_3_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Vertical');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b6.png');

% 读取图像并裁剪成正方形
im = imread('b6.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b6.png');



figure (7)
subplot(1,1,1)
plot(u3_3_R,v3_3_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Diagonal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b7.png');

% 读取图像并裁剪成正方形
im = imread('b7.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b7.png');





figure (8)
subplot(1,1,1)
plot(u4_3_R,v4_3_R,'r.','linewidth',3,'markersize',3);
xlim([0,300])
ylim([0,300])
set(gca,'XTick',0:50:300,'YTick',0:50:300,'fontsize',22,'fontname','times new roman');
set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
set(gca,'YTickLabel',{'0','50','100','150','200','250','300'});
% xlabel('Pixel gray value on location(\itx\rm,\ity\rm)');
% ylabel('Pixel gray value on location(\itx\rm+1,\ity\rm)');
title('Anti diagonal');

% 设置坐标轴比例
aspect_ratio = diff(xlim) / diff(ylim);
pbaspect([1, aspect_ratio, 1]);

% 保存图像
saveas(gcf,'b8.png');

% 读取图像并裁剪成正方形
im = imread('b8.png');
[row, col, ~] = size(im);
edge_length = min(row, col);
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);

% 保存裁剪后的图像
imwrite(im_cropped, 'b8.png');


%r= ImCoef_function( jiamihou_1,2000 );
end




