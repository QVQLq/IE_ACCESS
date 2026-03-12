img1=imread("brain1.jpg");
img2=imread("brain2.jpg");

img11=img1(:,:,1);
img22=img1(:,:,2);
img33=img1(:,:,3);
img44=img2(:,:,1);
img55=img2(:,:,2);
img66=img2(:,:,3);


[IMG] = Copy_of_Shengchengtupian_Jiami(img1,img2);

% img111=IMG(:,:,1);
% img222=IMG(:,:,2);
% img333=IMG(:,:,3);
% img444=IMG(:,:,4);
% img555=IMG(:,:,5);
% img666=IMG(:,:,6);

img111=cat(3,IMG(:,:,1),IMG(:,:,2),IMG(:,:,3));
img222=cat(3,IMG(:,:,4),IMG(:,:,5),IMG(:,:,6));


figure
subplot(2, 2, 1)
imshow(img1)
%title('第一张加密前的图像')
imwrite(img1, 'barin11.png');

subplot(2, 2, 2)
imshow(img2)
%title('第二张加密前的图像')
imwrite(img2, 'brain22.png');

subplot(2, 2, 3)
imshow(img111 )
%title('第一张加密前的图像')
imwrite(img111, 'img111 .png');

subplot(2, 2, 4)
imshow(img222 )
%title('第二张加密前的图像')
imwrite(img222, 'img222 .png');


