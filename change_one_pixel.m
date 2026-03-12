function image = change_one_pixel(image)
% 随机改变一张图像image的一个像素点,使其值加1
% 输入:image,三维图像array 
% 返回:image_new,改变后的图像
image=uint8(image);
[M, N,L] = size(image);   % 获取图像大小

% 随机生成像素坐标
i = randi(M);  
j = randi(N);
k = randi(L);  


% 改变选中的像素点
image(i, j,k) = image(i, j,k)+1;

%image(i, j,k) =255;

% disp(i)
% disp(j)
% disp(k)

end