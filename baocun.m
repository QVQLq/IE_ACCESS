function [k1] = baocun(x1)
% 读取图像并裁剪成正方形
[row, col, ~] = size(x1);
edge_length = min(row, col) + 100;  % 增加裁剪后图像的大小
im_cropped = imcrop(x1, [(col - edge_length) / 2, (row - edge_length) / 2, edge_length, edge_length]);
imwrite(im_cropped, 'h1.png');

% 调整图像大小
targetSize = [657, 657];  % 设置目标尺寸为 657x657
k1 = imresize(im_cropped, targetSize);
end

