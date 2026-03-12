function [NPCR,UACI] = function_NPCRUACI(image1, image2)  
% 计算两幅图像image1和image2之间的NPCR
% 输入:image1和image2,三维图像array  
% 返回:NPCR,双精度浮点数

[M, N] = size(image1);
image1 = double(image1); 
image2 = double(image2);  
different = (image1 ~= image2);    
NPCR = 100 * sum(sum(sum(different))) / (M*N);


[M, N] = size(image1);
image1 = double(image1); 
image2 = double(image2);
UACI = 100 * sum(sum(sum(abs(image1 - image2)))) / (255 * M * N);




end  


