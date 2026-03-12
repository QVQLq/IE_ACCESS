close all
clear

% 
% img11_RGB = imread('img-00025-00001.jpg'); 
% img22_RGB = imread('img-00029-00001.jpg'); 
% 
% img11_RGB = imread('img-00025-00001.jpg'); 
% img22_RGB = imread('img-00021-00001.jpg'); 

% img11_RGB = imread('RGB_baboon.bmp'); 
% img22_RGB = imread('RGB_Lena.bmp'); 


% img11_RGB = imread('Lung1.jpg'); 
% img22_RGB = imread('epigastrium1.jpg'); 

% img11_RGB = imread('IM00055.jpg'); 
% img22_RGB = imread('IMG0001.jpg');

% img11_RGB = imread('IM00056.jpg'); 
% img22_RGB = imread('IM00057.jpg'); 
% 

% img11_RGB = imread('black_image.png'); 
% img22_RGB = imread('black_image.png');

% img11_RGB = imread('white_image.png'); 
% img22_RGB = imread('white_image.png'); 
% 
% img11_RGB = imread('black_image.png'); 
% img22_RGB = imread('black_image.png');

% img11_RGB = imread('RGB256_House.tiff'); 
% img22_RGB = imread('RGB256_Tree.tiff');

% img11_RGB = imread('RGB_Lena.bmp'); 
% img22_RGB = imread('RGB_baboon.bmp');
% 

% img11_RGB = imread('image_1.jpg'); 
% img22_RGB = imread('image_2.jpg');

% img11_RGB = imread('RGB256_Couple.tiff'); 
% img22_RGB = imread('');

%img22_RGB = imread('GREY256_Airplane.tiff');

% img11_RGB = imread('RGB256_House.tiff'); 
 % img22_RGB = imread('RGB256_Tree.tiff');

% P1=imread('GERY_Airplane.tiff'); 
% P2=imread('GREY_Aerial.tiff'); 
% P3=imread('GREY_APC.tiff'); 
% P4=imread('GREY_Truck.tiff'); 
% P5=imread('GREY_tank.tiff'); 
% P6=imread('GREY_Couple.tiff'); 
% p1=imread('GREY_Baboon.bmp'); 
% p1=imread('GREY_pepperplain.bmp'); 

% P1 = imread('GREY256_Aerial.tiff'); 
% P2= imread('GREY256_Airplane.tiff');
% P3= imread('GREY256_ChemicalPlant.tiff');
% P4= imread('GREY256_Cloack.tiff');
% P5= imread('GREY256_Moon surface.tiff');
% P6= imread('GREY256_ResolutionChart.tiff');

% P1=imread("IM1.jpg");
% P1=P1(:,:,1);
% P2=imread("IM2.jpg");
% P2=P2(:,:,1);
% P3=imread("IM3.jpg");
% P3=P3(:,:,1);
% P4=imread("IM4.jpg");
% P4=P4(:,:,1);
% P5=imread("IM5.jpg");
% P5=P5(:,:,1);
% P6=imread("IM6.jpg");
% P6=P6(:,:,1);

P1=imread("Viral Pneumonia (1).png");

P2=imread("Viral Pneumonia (2).png");

P3=imread("Viral Pneumonia (3).png");

P4=imread("Viral Pneumonia (4).png");

P5=imread("Viral Pneumonia (5).png");

P6=imread("Viral Pneumonia (6).png");


% P1=imread("image_1.jpg");
% P1=P1(:,:,1);
% P2=imread("image_2.jpg");
% P2=P2(:,:,1);
% P3=imread("image_3.jpg");
% P3=P3(:,:,1);
% P4=imread("image_4.jpg");
% P4=P4(:,:,1);
% P5=imread("image_5.jpg");
% P5=P5(:,:,1);
% P6=imread("image_6.jpg");
% P6=P6(:,:,1);

% P1=imresize(P1,[256 256]);
% P2=imresize(P2,[256 256]);
% P3=imresize(P3,[256 256]);
% P4=imresize(P4,[256 256]);
% P5=imresize(P5,[256 256]);
% P6=imresize(P6,[256 256]);

% P1=imread("RGB_Lena.bmp");
% P1=P1(:,:,1);
% P2=imread("RGB_Peppers.tiff");
% P2=P2(:,:,1);
% P3=imread("RGB_Sailboat.tiff");
% P3=P3(:,:,1);
% P4=imread("RGB_baboon.bmp");
% P4=P4(:,:,1);
% P5=imread("RGB_Airplane.tiff");
% P5=P5(:,:,1);
% P6=imread("GREY_Couple.tiff");
% P6=P6(:,:,1);
% 
img11_RGB = double(cat(3,P1,P2,P3)); 
img22_RGB = double(cat(3,P4,P5,P6));






%option
%1=测试NPCR,UACI
%2=高斯噪声
%3=椒盐噪声
%4=裁剪攻击
%5=水平垂直对角相关  
%6=信息熵
%7=直方图分析
%8=相邻像素相关性图
%9=密钥
%10=PSNR
%11=SSIM
%12=VIH
%13=3D直方图
%14=chi-square
%15=一次
%16=3D 相邻像素相关性图

option=3;


switch option

case 1


%生成6*512*512的置乱加扩散的IMG1
IMG1=Shengchengtupian_Jiami(img11_RGB,img22_RGB);
n=10;
NPCR_sum=0;
UACI_sum=0;

for k=1:n

%改变原图的一个点的像素使其＋1
    if  mod(k,2)==0
 img33_RGB = change_one_pixel(img22_RGB);IMG2=Shengchengtupian_Jiami(img11_RGB,img33_RGB);
    else
 img33_RGB = change_one_pixel(img11_RGB);IMG2=Shengchengtupian_Jiami(img33_RGB,img22_RGB);

    end


%连成512*（512*6）的Horz_1和Horz_2
Horz_1=horzcat(IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3),IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6));
Horz_2=horzcat(IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3),IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6));


%检测其NPCR,UACI
[NPCR,UACI] = function_NPCRUACI(Horz_1, Horz_2) ;

%fprintf('NPCR: %f\n', NPCR);
%fprintf('UACI: %f\n', UACI);
disp(NPCR)
disp(UACI)
NPCR_sum=NPCR+NPCR_sum;
UACI_sum=UACI+UACI_sum;
end
NPCR_ave=double(NPCR_sum/n);
UACI_ave=double(UACI_sum/n);
 %disp(NPCR_ave)
 %disp(UACI_ave)
fprintf('NPCR:%f,UACI:%f\n',NPCR_ave,UACI_ave);





 case 2

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);

img3_RGB = img11_RGB; 
img4_RGB = img22_RGB;
[IMG2] = Shengchengtupian_Jiami(img3_RGB,img4_RGB);
IMG2=uint8(IMG2);
%高斯噪声


% IMG2(:,:,1) =  (imnoise(IMG2(:,:,1), 'gaussian',  0,0.00001));
% IMG2(:,:,2) =  (imnoise(IMG2(:,:,2), 'gaussian',  0,0.00001));
% IMG2(:,:,3)=  (imnoise(IMG2(:,:,3), 'gaussian',  0,0.00001));
% IMG2(:,:,4) =  (imnoise(IMG2(:,:,4), 'gaussian', 0, 0.00001));
% IMG2(:,:,5) =  (imnoise(IMG2(:,:,5), 'gaussian',  0,0.00001));
% IMG2(:,:,6) = (imnoise(IMG2(:,:,6), 'gaussian',  0,0.00001));



jiamihou_3=uint8(cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3)));
jiamihou_4=uint8(cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6)));
[img33_RGB_b,img44_RGB_b] = Shengchengtupian_Jiemi(IMG2);


% n=5;
% 
% img33_RGB_b(:,:,1)= medfilt2(img33_RGB_b(:,:,1),[n,n]);
% img33_RGB_b(:,:,2)= medfilt2(img33_RGB_b(:,:,2),[n,n]);
% img33_RGB_b(:,:,3)= medfilt2(img33_RGB_b(:,:,3),[n,n]);
% img44_RGB_b(:,:,1)= medfilt2(img44_RGB_b(:,:,1),[n,n]);
% img44_RGB_b(:,:,2)= medfilt2(img44_RGB_b(:,:,2),[n,n]);
% img44_RGB_b(:,:,3)= medfilt2(img44_RGB_b(:,:,3),[n,n]);

imwrite(jiamihou_3,'1.png')
imwrite(jiamihou_4,'2.png')
imwrite(img33_RGB_b,'3.png')
imwrite(img44_RGB_b,'4.png')

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
img11_RGB=uint8(img11_RGB);
img22_RGB=uint8(img22_RGB);
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);


img3_RGB = img11_RGB; 
img4_RGB = img22_RGB;
[IMG2] = Shengchengtupian_Jiami(img3_RGB,img4_RGB);
IMG2=uint8(IMG2);

n1=1;
IMG2(:,:,1) =  (imnoise(IMG2(:,:,1), 'salt & pepper',n1));
IMG2(:,:,2) =  (imnoise(IMG2(:,:,2), 'salt & pepper', n1));
IMG2(:,:,3)=  (imnoise(IMG2(:,:,3), 'salt & pepper', n1));
IMG2(:,:,4) =  (imnoise(IMG2(:,:,4), 'salt & pepper', n1));
IMG2(:,:,5) =  (imnoise(IMG2(:,:,5), 'salt & pepper', n1));
IMG2(:,:,6) = (imnoise(IMG2(:,:,6), 'salt & pepper', n1));
% % 

% IMG2(:,:,1) = imnoise(IMG2(:,:,1),'speckle',0.0001);
% IMG2(:,:,2) = imnoise(IMG2(:,:,2),'speckle',0.0001);
% IMG2(:,:,3) = imnoise(IMG2(:,:,3),'speckle',0.0001);
% IMG2(:,:,4) = imnoise(IMG2(:,:,4),'speckle',0.0001);
% IMG2(:,:,5) = imnoise(IMG2(:,:,5),'speckle',0.0001);
% IMG2(:,:,6) = imnoise(IMG2(:,:,6),'speckle',0.0001);
% 
% IMG2(:,:,1) =  (imnoise(IMG2(:,:,1), 'gaussian',  0,0.0001));
% IMG2(:,:,2) =  (imnoise(IMG2(:,:,2), 'gaussian',  0,0.0001));
% IMG2(:,:,3)=  (imnoise(IMG2(:,:,3), 'gaussian',  0,0.00001));
% IMG2(:,:,4) =  (imnoise(IMG2(:,:,4), 'gaussian', 0, 0.0001));
% IMG2(:,:,5) =  (imnoise(IMG2(:,:,5), 'gaussian',  0,0.0001));
% IMG2(:,:,6) = (imnoise(IMG2(:,:,6), 'gaussian',  0,0.0001));

% IMG2(:,:,1) = imnoise(IMG2(:,:,1),'poisson');
% IMG2(:,:,2) = imnoise(IMG2(:,:,2),'poisson');
% IMG2(:,:,3) = imnoise(IMG2(:,:,3),'poisson');
% IMG2(:,:,4) = imnoise(IMG2(:,:,4),'poisson');
% IMG2(:,:,5) = imnoise(IMG2(:,:,5),'poisson');
% IMG2(:,:,6) = imnoise(IMG2(:,:,6),'poisson');

jiamihou_3=uint8(cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3)));
jiamihou_4=uint8(cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6)));



[img33_RGB_b,img44_RGB_b] = Shengchengtupian_Jiemi(IMG2);
jiamicat=cat(6,img33_RGB_b(:,:,1),img33_RGB_b(:,:,2),img33_RGB_b(:,:,3),img44_RGB_b(:,:,1),img44_RGB_b(:,:,2),img44_RGB_b(:,:,3));



% n=5;
% 
% img33_RGB_b(:,:,1)= medfilt2(img33_RGB_b(:,:,1),[n,n]);
% img33_RGB_b(:,:,2)= medfilt2(img33_RGB_b(:,:,2),[n,n]);
% img33_RGB_b(:,:,3)= medfilt2(img33_RGB_b(:,:,3),[n,n]);
% img44_RGB_b(:,:,1)= medfilt2(img44_RGB_b(:,:,1),[n,n]);
% img44_RGB_b(:,:,2)= medfilt2(img44_RGB_b(:,:,2),[n,n]);
% img44_RGB_b(:,:,3)= medfilt2(img44_RGB_b(:,:,3),[n,n]);


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

% imwrite(jiamihou_3,'1.png')
% imwrite(jiamihou_4,'2.png')
% imwrite(img33_RGB_b,'3.png')
% imwrite(img44_RGB_b,'4.png')



for i=1:512
    for k=1:512
          if i==1 
              jiamicat(i,k,1)=0;
              jiamicat(i,k,2)=0;
              jiamicat(i,k,3)=0;
              jiamicat(i,k,4)=0;
              jiamicat(i,k,5)=0;
              jiamicat(i,k,6)=0;
          elseif i==512
               jiamicat(i,k,1)=0;
              jiamicat(i,k,2)=0;
              jiamicat(i,k,3)=0;
              jiamicat(i,k,4)=0;
              jiamicat(i,k,5)=0;
              jiamicat(i,k,6)=0;
          elseif k==1
               jiamicat(i,k,1)=0;
              jiamicat(i,k,2)=0;
              jiamicat(i,k,3)=0;
              jiamicat(i,k,4)=0;
              jiamicat(i,k,5)=0;
              jiamicat(i,k,6)=0;
          elseif k==512
               jiamicat(i,k,1)=0;
              jiamicat(i,k,2)=0;
              jiamicat(i,k,3)=0;
              jiamicat(i,k,4)=0;
              jiamicat(i,k,5)=0;
              jiamicat(i,k,6)=0;
           end

    end

end



imwrite(jiamicat(:,:,1),'03-1.png')
imwrite(jiamicat(:,:,2),'03-2.png')
imwrite(jiamicat(:,:,3),'03-3.png')
imwrite(jiamicat(:,:,4),'03-4.png')
imwrite(jiamicat(:,:,5),'03-5.png')
imwrite(jiamicat(:,:,6),'03-6.png')





imwrite(img22_RGB, 'h2.png');  % 保存调整大小后的图像
% 读取图像并裁剪成正方形
im = imread('h2.png');
[row, col, ~] = size(im);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h2.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
imwrite(k1, 'o2.png');  % 保存调整大小后的图像





% 
% 
% 
% 
% 
% imwrite(jiamihou_4, 'h2.png');  % 保存调整大小后的图像
% % 读取图像并裁剪成正方形
% im = imread('h2.png');
% [row, col, ~] = size(im);
% edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
% im_cropped = imcrop(im, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
% imwrite(im_cropped, 'h2.png');
% 
% % 调整图像大小
% targetSize = [657, 657];  % 设置目标尺寸为 657x657
% k1 = imresize(im_cropped, targetSize);
% imwrite(k1, 'jiamihou_4.png');  % 保存调整大小后的图像



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
% I_r_1 =IMG2(:,:,1);
% I_r_1(256:512,:)=0;
% I_g_1 =IMG2(:,:,2);
% I_g_1(256:512,:)=0;
% I_b_1 =IMG2(:,:,3);
% I_b_1(256:512,:)=0;
% I_r_2 =IMG2(:,:,4);
% I_r_2(256:512,:)=0;
% I_g_2 =IMG2(:,:,5);
% I_g_2(256:512,:)=0;
% I_b_2 =IMG2(:,:,6);
% I_b_2(256:512,:)=0;


% n=128;
% I_r_1 =IMG2(:,:,1);
% I_r_1(256-n:256+n,256-n:256+n)=0;
% I_g_1 =IMG2(:,:,2);
% I_g_1(256-n:256+n,256-n:256+n)=0;
% I_b_1 =IMG2(:,:,3);
% I_b_1(256-n:256+n,256-n:256+n)=0;
% I_r_2 =IMG2(:,:,4);
% I_r_2(256-n:256+n,256-n:256+n)=0;
% I_g_2 =IMG2(:,:,5);
% I_g_2(256-n:256+n,256-n:256+n)=0;
% I_b_2 =IMG2(:,:,6);
% I_b_2(256-n:256+n,256-n:256+n)=0;

% for i=1:512
% I_r_1 =IMG2(:,:,1);
% I_r_1(i:512,i)=0;
% I_g_1 =IMG2(:,:,2);
% I_g_1(i:512,i)=0;
% I_b_1 =IMG2(:,:,3);
% I_b_1(i:512,i)=0;
% I_r_2 =IMG2(:,:,4);
% I_r_2(i:512,i)=0;
% I_g_2 =IMG2(:,:,5);
% I_g_2(i:512,i)=0;
% I_b_2 =IMG2(:,:,6);
% I_b_2(i:512,i)=0;
% 
% end

I_r_1 =IMG2(:,:,1);
I_g_1 =IMG2(:,:,2);
I_b_1 =IMG2(:,:,3);
I_r_2 =IMG2(:,:,4);
I_g_2 =IMG2(:,:,5);
I_b_2 =IMG2(:,:,6);



for i = 1:512
    for j = 1:i
        I_r_1(i, j) = 0;
    end
end

for i = 1:512
    for j = 1:i
        I_g_1(i, j) = 0;
    end
end


for i = 1:512
    for j = 1:i
        I_b_1(i, j) = 0;
    end
end

for i = 1:512
    for j = 1:i
        I_r_2(i, j) = 0;
    end
end

for i = 1:512
    for j = 1:i
        I_g_2(i, j) = 0;
    end
end


for i = 1:512
    for j = 1:i
        I_b_2(i, j) = 0;
    end
end

img1111=cat(3,I_r_1,I_g_1,I_b_1);
img2222=cat(3,I_r_2,I_g_2,I_b_2);

imwrite(img1111,'test9.png')
imwrite(img2222,'test10.png')


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

imwrite(img33_RGB_b,'test11.png')
imwrite(img44_RGB_b,'test12.png')



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



jiamicat=uint8(cat(6,img1111,img2222));
imwrite(jiamicat(:,:,1),'xieqie1_qian.png')
imwrite(jiamicat(:,:,2),'xieqie2_qian.png')
imwrite(jiamicat(:,:,3),'xieqie3_qian.png')
imwrite(jiamicat(:,:,4),'xieqie4_qian.png')
imwrite(jiamicat(:,:,5),'xieqie5_qian.png')
imwrite(jiamicat(:,:,6),'xieqie6_qian.png')





jiamicat=cat(6,img33_RGB_b,img44_RGB_b);
imwrite(jiamicat(:,:,1),'xieqie1.png')
imwrite(jiamicat(:,:,2),'xieqie2.png')
imwrite(jiamicat(:,:,3),'xieqie3.png')
imwrite(jiamicat(:,:,4),'xieqie4.png')
imwrite(jiamicat(:,:,5),'xieqie5.png')
imwrite(jiamicat(:,:,6),'xieqie6.png')









case 5
   %水平垂直对角相关     

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);

%imshow(img22_RGB_b)


% figure
% subplot(1,1,1);
% [x1, y1] = PixelCorrelationDiagram(jiamihou_1(:,:,1));
% title('第一张加密前的图像R通道的水平垂直对角相关 ')
% plot(x1, y1, '.');


N=5000;
[r1,u11,v11,u21,v21,u31,v31,u41,v41]=ImCoef(jiamihou_1(:,:,1),N);
[r2,u12,v12,u22,v22,u32,v32,u42,v42]=ImCoef(jiamihou_1(:,:,2),N);
[r3,u13,v13,u23,v23,u33,v33,u43,v43]=ImCoef(jiamihou_1(:,:,3),N);
[r4,u14,v14,u24,v24,u34,v34,u44,v44]=ImCoef(jiamihou_2(:,:,1),N);
[r5,u15,v15,u25,v25,u35,v35,u45,v45]=ImCoef(jiamihou_2(:,:,2),N);
[r6,u16,v16,u26,v26,u36,v36,u46,v46]=ImCoef(jiamihou_2(:,:,3),N);


disp((r1+r2+r3+r4+r5+r6)/6)



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


[IMG1] = uint8(Shengchengtupian_Jiami(img11_RGB,img22_RGB));
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
imshow(jiamihou_1)

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


% jiamihou=horzcat(img11_RGB(:,:,1),img11_RGB(:,:,2),img11_RGB(:,:,3),img22_RGB(:,:,1),img22_RGB(:,:,2),img22_RGB(:,:,3));
% entropy2 = entropy(jiamihou);
% fprintf('平均信息熵2: %f\n', entropy2);
% 
% 
% 
% jiamihou=horzcat(IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3),IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6));
% entropy2 = entropy(jiamihou);
% fprintf('平均信息熵2: %f\n', entropy2);
% 



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
ylim([0,17000])
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
ylim([0,17000])
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
imwrite(k1, 'h3.png');  % 保存调整大小后的图像



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
% [r1_1_G,u1_1_G,v1_1_G,u2_1_G,v2_1_G,u3_1_G,v3_1_G,u4_1_G,v4_1_G]=ImCoef(img22_RGB(:,:,2),4000);
% [r1_1_B,u1_1_B,v1_1_B,u2_1_B,v2_1_B,u3_1_B,v3_1_B,u4_1_B,v4_1_B]=ImCoef(img22_RGB(:,:,3),4000);


% [r1_2_R,u1_2_R,v1_2_R,u2_2_R,v2_2_R,u3_2_R,v3_2_R,u4_2_R,v4_2_R]=ImCoef(img11_RGB(:,:,1),4000);
% [r1_2_G,u1_2_G,v1_2_G,u2_2_G,v2_2_G,u3_2_G,v3_2_G,u4_2_G,v4_2_G]=ImCoef(img11_RGB(:,:,2),4000);
% [r1_2_B,u1_2_B,v1_2_B,u2_2_B,v2_2_B,u3_2_B,v3_2_B,u4_2_B,v4_2_B]=ImCoef(img11_RGB(:,:,3),4000);


[r1_3_R,u1_3_R,v1_3_R,u2_3_R,v2_3_R,u3_3_R,v3_3_R,u4_3_R,v4_3_R]=ImCoef(jiamihou_1(:,:,1),4000);
%[r1_3_G,u1_3_G,v1_3_G,u2_3_G,v2_3_G,u3_3_G,v3_3_G,u4_3_G,v4_3_G]=ImCoef(jiamihou_2(:,:,2),4000);
%[r1_3_B,u1_3_B,v1_3_B,u2_3_B,v2_3_B,u3_3_B,v3_3_B,u4_3_B,v4_3_B]=ImCoef(jiamihou_2(:,:,3),4000);


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



case 9
%生成6*512*512的置乱加扩散的IMG1

IMG1=Key_of_Shengchengtupian_Jiami(img11_RGB,img22_RGB,0);
n=1;
NPCR_sum=0;
UACI_sum=0;


img111=cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3));
img222=cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6));



for k=1:n
%改变原图的一个点的像素使其＋1
IMG2=Key_of_Shengchengtupian_Jiami(img11_RGB,img22_RGB,k);

img111=cat(3,IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3));
img222=cat(3,IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6));


%连成512*（512*6）的Horz_1和Horz_2
Horz_1=horzcat(IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3),IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6));
Horz_2=horzcat(IMG2(:,:,1),IMG2(:,:,2),IMG2(:,:,3),IMG2(:,:,4),IMG2(:,:,5),IMG2(:,:,6));


%检测其NPCR,UACI
[NPCR,UACI] = function_NPCRUACI(Horz_1, Horz_2) ;

%fprintf('NPCR: %f\n', NPCR);
%fprintf('UACI: %f\n', UACI);
 %disp(NPCR)
 %disp(UACI)
NPCR_sum=NPCR+NPCR_sum;
UACI_sum=UACI+UACI_sum;
end
NPCR_ave=double(NPCR_sum/n);
UACI_ave=double(UACI_sum/n);
 disp(NPCR_ave)
 disp(UACI_ave)
%fprintf('当a=%d,当b=%d,NPCR:%f,UACI:%f\n', a,b,NPCR_ave,UACI_ave);






% figure
% subplot(3, 2, 1)
% imshow(img11_RGB )
% %title('第一张加密前的图像')
% 
% subplot(3, 2, 2)
% imshow(img22_RGB )
% %title('第二张加密前的图像')
% 
% subplot(3, 2, 5)
% imshow(img11_RGB_b)
% %title('第一张加密后的图像')
% 
% subplot(3, 2, 6)
% imshow(img22_RGB_b)
% %title('第二张加密后的图像')


case 10
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));

 n1=0.00001;
IMG1(:,:,1) =  (imnoise(IMG1(:,:,1), 'salt & pepper',n1));
IMG1(:,:,2) =  (imnoise(IMG1(:,:,2), 'salt & pepper', n1));
IMG1(:,:,3)=  (imnoise(IMG1(:,:,3), 'salt & pepper', n1));
IMG1(:,:,4) =  (imnoise(IMG1(:,:,4), 'salt & pepper', n1));
IMG1(:,:,5) =  (imnoise(IMG1(:,:,5), 'salt & pepper', n1));
IMG1(:,:,6) = (imnoise(IMG1(:,:,6), 'salt & pepper', n1));

% IMG1(:,:,1) = imnoise(IMG1(:,:,1),'speckle',n1);
% IMG1(:,:,2) = imnoise(IMG1(:,:,2),'speckle',n1);
% IMG1(:,:,3) = imnoise(IMG1(:,:,3),'speckle',n1);
% IMG1(:,:,4) = imnoise(IMG1(:,:,4),'speckle',n1);
% IMG1(:,:,5) = imnoise(IMG1(:,:,5),'speckle',n1);
% IMG1(:,:,6) = imnoise(IMG1(:,:,6),'speckle',n1);


% IMG1(:,:,1) =  (imnoise(IMG1(:,:,1), 'gaussian',  0,n1));
% IMG1(:,:,2) =  (imnoise(IMG1(:,:,2), 'gaussian',  0,n1));
% IMG1(:,:,3)=  (imnoise(IMG1(:,:,3), 'gaussian',  0,n1));
% IMG1(:,:,4) =  (imnoise(IMG1(:,:,4), 'gaussian', 0, n1));
% IMG1(:,:,5) =  (imnoise(IMG1(:,:,5), 'gaussian',  0,n1));
% IMG1(:,:,6) = (imnoise(IMG1(:,:,6), 'gaussian',  0,n1));



[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);



% img11_RGB_b=jiamihou_1;
% img22_RGB_b=jiamihou_2;

y1=PSNR_RGB(img11_RGB,img11_RGB_b);
y2=PSNR_RGB(img22_RGB,img22_RGB_b);



disp((y1+y2)/2)

re1=ssim(img11_RGB,jiamihou_1);
re2=ssim(img22_RGB,jiamihou_1);


disp((re1+re2)/2)



case 11


% img11_RGB=imresize(img11_RGB,[256 256]);
% img22_RGB=imresize(img22_RGB,[256 256]);
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));

 n1=0.00001;
IMG1(:,:,1) =  (imnoise(IMG1(:,:,1), 'salt & pepper',n1));
IMG1(:,:,2) =  (imnoise(IMG1(:,:,2), 'salt & pepper', n1));
IMG1(:,:,3)=  (imnoise(IMG1(:,:,3), 'salt & pepper', n1));
IMG1(:,:,4) =  (imnoise(IMG1(:,:,4), 'salt & pepper', n1));
IMG1(:,:,5) =  (imnoise(IMG1(:,:,5), 'salt & pepper', n1));
IMG1(:,:,6) = (imnoise(IMG1(:,:,6), 'salt & pepper', n1));

% IMG1(:,:,1) = imnoise(IMG1(:,:,1),'speckle',n1);
% IMG1(:,:,2) = imnoise(IMG1(:,:,2),'speckle',n1);
% IMG1(:,:,3) = imnoise(IMG1(:,:,3),'speckle',n1);
% IMG1(:,:,4) = imnoise(IMG1(:,:,4),'speckle',n1);
% IMG1(:,:,5) = imnoise(IMG1(:,:,5),'speckle',n1);
% IMG1(:,:,6) = imnoise(IMG1(:,:,6),'speckle',n1);

% IMG1(:,:,1) =  (imnoise(IMG1(:,:,1), 'gaussian',  0,n1));
% IMG1(:,:,2) =  (imnoise(IMG1(:,:,2), 'gaussian',  0,n1));
% IMG1(:,:,3)=  (imnoise(IMG1(:,:,3), 'gaussian',  0,n1));
% IMG1(:,:,4) =  (imnoise(IMG1(:,:,4), 'gaussian', 0, n1));
% IMG1(:,:,5) =  (imnoise(IMG1(:,:,5), 'gaussian',  0,n1));
% IMG1(:,:,6) = (imnoise(IMG1(:,:,6), 'gaussian',  0,n1));


[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);

ssimsum=0;psnrsum=0;
% for n=1:3
% 
% re1=ssim(uint8(img11_RGB(:,:,n)),uint8(jiamihou_1(:,:,n)));
% 
% re2=ssim(uint8(img22_RGB(:,:,n)),uint8(jiamihou_2(:,:,n)));
% 
% re3=psnr(uint8(img11_RGB(:,:,n)),uint8(jiamihou_1(:,:,n)));
% 
% re4=psnr(uint8(img22_RGB(:,:,n)),uint8(jiamihou_2(:,:,n)));
% 
% ssimsum=(re1+re2)/2+ssimsum;
% psnrsum=(re3+re4)/2+psnrsum;
% 
% end
% disp(ssimsum/3)
% disp(psnrsum/3)


re1=ssim(uint8(img11_RGB(:,:,1)),uint8(jiamihou_1(:,:,1)));
disp(re1)

re1=ssim(uint8(img11_RGB(:,:,2)),uint8(jiamihou_1(:,:,2)));
disp(re1)

re1=ssim(uint8(img11_RGB(:,:,3)),uint8(jiamihou_1(:,:,3)));
disp(re1)

re1=ssim(uint8(img22_RGB(:,:,1)),uint8(jiamihou_2(:,:,1)));
disp(re1)

re1=ssim(uint8(img22_RGB(:,:,2)),uint8(jiamihou_2(:,:,2)));
disp(re1)

re1=ssim(uint8(img22_RGB(:,:,3)),uint8(jiamihou_2(:,:,3)));
disp(re1)

disp(re1)

re1=psnr(uint8(img11_RGB(:,:,1)),uint8(jiamihou_1(:,:,1)));
disp(re1)

re1=psnr(uint8(img11_RGB(:,:,2)),uint8(jiamihou_1(:,:,2)));
disp(re1)

re1=psnr(uint8(img11_RGB(:,:,3)),uint8(jiamihou_1(:,:,3)));
disp(re1)

re1=psnr(uint8(img22_RGB(:,:,1)),uint8(jiamihou_2(:,:,1)));
disp(re1)

re1=psnr(uint8(img22_RGB(:,:,2)),uint8(jiamihou_2(:,:,2)));
disp(re1)

re1=psnr(uint8(img22_RGB(:,:,3)),uint8(jiamihou_2(:,:,3)));
disp(re1)









case 12
img11_RGB=imresize(img11_RGB,[256 256]);
img22_RGB=imresize(img22_RGB,[256 256]);

    
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));






% sum1=0;sum2=0;
% for n=1:3
% vih3_imhist = imhist(img11_RGB(:,:,n));
% vih3 = var(vih3_imhist);
% disp(vih3)
% sum1=sum1+vih3;
% end
% 
% 
% for n=1:3
% vih3_imhist = imhist(img22_RGB(:,:,n));
% vih3 = var(vih3_imhist);
% disp(vih3)
% sum2=sum2+vih3;
% end

sum1=0;sum2=0;
for n=1:3
vih3_imhist = imhist(jiamihou_1(:,:,n));
vih3 = var(vih3_imhist);
disp(vih3)
sum1=sum1+vih3;
end


for n=1:3
vih3_imhist = imhist(jiamihou_2(:,:,n));
vih3 = var(vih3_imhist);
disp(vih3)
sum2=sum2+vih3;
end





case 13

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));

% imwrite(jiamihou_1(:,:,1), 'e1.png');
% imwrite(jiamihou_1(:,:,2), 'e2.png');
% imwrite(jiamihou_1(:,:,3), 'e3.png');
% imwrite(jiamihou_2(:,:,1), 'e4.png');
% imwrite(jiamihou_2(:,:,2), 'e5.png');
% imwrite(jiamihou_2(:,:,3), 'e6.png');

imwrite(uint8(img11_RGB(:,:,1)), 'o1.png');
imwrite(uint8(img11_RGB(:,:,2)), 'o2.png');
imwrite(uint8(img11_RGB(:,:,3)), 'o3.png');
imwrite(uint8(img22_RGB(:,:,1)), 'o4.png');
imwrite(uint8(img22_RGB(:,:,2)), 'o5.png');
imwrite(uint8(img22_RGB(:,:,3)), 'o6.png');



imwrite(uint8(jiamihou_1(:,:,1)), 'e1.png');
imwrite(uint8(jiamihou_1(:,:,2)), 'e2.png');
imwrite(uint8(jiamihou_1(:,:,3)), 'e3.png');
imwrite(uint8(jiamihou_2(:,:,1)), 'e4.png');
imwrite(uint8(jiamihou_2(:,:,2)), 'e5.png');
imwrite(uint8(jiamihou_2(:,:,3)), 'e6.png');

figure
imshow(uint8(jiamihou_1(:,:,1)))
figure
imshow(uint8(jiamihou_1(:,:,2)))
figure
imshow(uint8(jiamihou_1(:,:,3)))
figure
imshow(uint8(jiamihou_2(:,:,1)))
figure
imshow(uint8(jiamihou_2(:,:,2)))
figure
imshow(uint8(jiamihou_2(:,:,3)))

% imwrite(IMG1(:,:,1), 'o1.png');
% imwrite(IMG1(:,:,2), 'o2.png');
% imwrite(IMG1(:,:,3), 'o3.png');
% imwrite(IMG1(:,:,4), 'o4.png');
% imwrite(IMG1(:,:,5), 'o5.png');
% imwrite(IMG1(:,:,6), 'o6.png');






case 14

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);



chiSquareValue1 = chi2(jiamihou_1);
chiSquareValue2 = chi2(jiamihou_2);
chiSquareValue=(chiSquareValue1+chiSquareValue2)/2;

% 显示卡方检验结果
fprintf('Chi-square value: %.2f\n', chiSquareValue);

case 15
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
% jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
% jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
% [img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);








case 16
img11_RGB = imread('img-00025-00001.jpg'); 
img22_RGB = imread('img-00029-00001.jpg'); 
[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));
[img11_RGB_b,img22_RGB_b] = Shengchengtupian_Jiemi(IMG1);
N=20000;
[r1_1_R,u1_1_R,v1_1_R,u2_1_R,v2_1_R,u3_1_R,v3_1_R,u4_1_R,v4_1_R]=ImCoef(img11_RGB(:,:,1),N);
% [r1_1_G,u1_1_G,v1_1_G,u2_1_G,v2_1_G,u3_1_G,v3_1_G,u4_1_G,v4_1_G]=ImCoef(img22_RGB(:,:,2),N);
% [r1_1_B,u1_1_B,v1_1_B,u2_1_B,v2_1_B,u3_1_B,v3_1_B,u4_1_B,v4_1_B]=ImCoef(img22_RGB(:,:,3),N);
% [r1_2_R,u1_2_R,v1_2_R,u2_2_R,v2_2_R,u3_2_R,v3_2_R,u4_2_R,v4_2_R]=ImCoef(img11_RGB(:,:,1),N);
% [r1_2_G,u1_2_G,v1_2_G,u2_2_G,v2_2_G,u3_2_G,v3_2_G,u4_2_G,v4_2_G]=ImCoef(img11_RGB(:,:,2),N);
% [r1_2_B,u1_2_B,v1_2_B,u2_2_B,v2_2_B,u3_2_B,v3_2_B,u4_2_B,v4_2_B]=ImCoef(img11_RGB(:,:,3),N);
[r1_3_R,u1_3_R,v1_3_R,u2_3_R,v2_3_R,u3_3_R,v3_3_R,u4_3_R,v4_3_R]=ImCoef(jiamihou_1(:,:,1),N);
%[r1_3_G,u1_3_G,v1_3_G,u2_3_G,v2_3_G,u3_3_G,v3_3_G,u4_3_G,v4_3_G]=ImCoef(jiamihou_2(:,:,2),N);
%[r1_3_B,u1_3_B,v1_3_B,u2_3_B,v2_3_B,u3_3_B,v3_3_B,u4_3_B,v4_3_B]=ImCoef(jiamihou_2(:,:,3),N);
[r1_4_R,u1_4_R,v1_4_R,u2_4_R,v2_4_R,u3_4_R,v3_4_R,u4_4_R,v4_4_R]=ImCoef(jiamihou_1(:,:,1),N);
[r1_4_G,u1_4_G,v1_4_G,u2_4_G,v2_4_G,u3_4_G,v3_4_G,u4_4_G,v4_4_G]=ImCoef(jiamihou_1(:,:,2),N);
[r1_4_B,u1_4_B,v1_4_B,u2_4_B,v2_4_B,u3_4_B,v3_4_B,u4_4_B,v4_4_B]=ImCoef(jiamihou_1(:,:,3),N);    
figure;
% 绘制第一个面
h1 = plot3(zeros(size(u1_1_R)), u1_1_R, v1_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
hold on;
% 绘制第二个面
h2 = plot3(ones(size(u2_1_R)), u2_1_R, v2_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 绘制第三个面
h3 = plot3(2 * ones(size(u3_1_R)), u3_1_R, v3_1_R, 'r.', 'linewidth', 3, 'markersize', 3);
% 设置颜色
set(h1, 'Color', [0.00, 0.45, 0.74]);
set(h2, 'Color', [0.85, 0.33, 0.10]);
set(h3, 'Color', [0.93, 0.69, 0.13]);
% 设置坐标轴标签等
ylabel('pixel value');
zlabel('adjacent pixel value');
% 修改x轴刻度标签
ax = gca;
ax.XTick = [0, 1, 2];

       
end