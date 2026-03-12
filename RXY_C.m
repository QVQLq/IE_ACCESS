clc; clear ; close all;
K=[1.1 2 3.3 4.4 2000];       %K=[k,N0,x0,y0 ,z0,uL,uS,uC]
img11_RGB = imread('RGB_Lena.bmp'); 
img22_RGB = imread('RGB_baboon.bmp');      

[IMG1] = Shengchengtupian_Jiami(img11_RGB,img22_RGB);
jiamihou_1=uint8(cat(3,IMG1(:,:,1),IMG1(:,:,2),IMG1(:,:,3)));
jiamihou_2=uint8(cat(3,IMG1(:,:,4),IMG1(:,:,5),IMG1(:,:,6)));



%P2=imread('baboon.bmp'); P3=imread('fruits.bmp');P4=imread('flowers.bmp');
% RP2=P2(:,:,1);GP2=P2(:,:,2);BP2=P2(:,:,3);  
% RP3=P3(:,:,1);GP3=P3(:,:,2);BP3=P3(:,:,3);         
% RP4=P4(:,:,1);GP4=P4(:,:,2);BP4=P4(:,:,3);  
r=zeros(1,4);


 %%%C1 = TpEncrypt( P1,K ); 



%  RC1=C1(:,:,1);GC1=C1(:,:,2);BC1=C1(:,:,3); 

jiamihou=jiamihou_2(:,:,3);

 for i=1:200
 r=r+rxy_f(jiamihou);
 end
 rr=r/200;
%r=rxy_f(P1);
disp(rr)