function [x, y] = PixelCorrelationDiagram(img)
% 输入：img 是一个 M 行 N 列的图像矩阵
% 输出：x 和 y 是长度为 MN 的向量，可用于生成像素相关图

[M, N] = size(img);
x = reshape(img, [1, M*N]);
y = zeros(1, M*N);

% 水平相关
for i = 1:M
    for j = 1:N
        if j == N
            y((i-1)*N+j) = img(i, 1);
        else
            y((i-1)*N+j) = img(i, j+1);
        end
    end
end

% 垂直相关
for i = 1:M
    for j = 1:N
        if i == M
            y((i-1)*N+j) = img(1, j);
        else
            y((i-1)*N+j) = img(i+1, j);
        end
    end
end

% 对角相关
for i = 1:M
    for j = 1:N
        if i == M && j == N
            y((i-1)*N+j) = img(1, 1);
        elseif i == M
            y((i-1)*N+j) = img(1, j+1);
        elseif j == N
            y((i-1)*N+j) = img(i+1, 1);
        else
            y((i-1)*N+j) = img(i+1, j+1);
        end
    end
end

end
