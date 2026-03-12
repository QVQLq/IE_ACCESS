function img1 = Decrypt_Saomiao_2_changfangxing(Line, m, n)

% 从Line中恢复Line1、Line2和Line3
Line1 = Line(1:(n*n-n*(m-n+1))/2);
Line2 = Line((n*n-n*(m-n+1))/2+1:(n*n-n*(m-n+1))/2+(m-n+1)*n);
Line3 = Line((n*n-n*(m-n+1))/2+(m-n+1)*n+1:end);

img1 = zeros(m, n);

% 从Line1中恢复图像的左上部分
idx = 1;
for i=1:(n-2)/2+1
    for j=1:4*(i-1)+1
        x=(n-2*(i-1)+floor(j/2));
        y=2+floor((j-1)/4)*2-mod(j,2);
        img1(x,y) = Line1(idx);
        idx = idx + 1;
    end
end

% 从Line2中恢复图像的对角线部分
idx = 1;
for i = 1:m-n+1
    for j = 1:n
        y = j + (i-1);
        x = j;
        img1(x, y) = Line2(idx);
        idx = idx + 1;
    end
end

% 从Line3中恢复图像的右下部分
idx = 1;
for i = (n-2)/2+1 : -1 : 1
    for j = 1 : 4*(i-1)+1
        y = (n-2*(i-1) + floor(j/2))+(m-n);
        x = 2 + floor((j-1)/4)*2 - mod(j, 2);
        img1(x, y) = Line3(idx);
        idx = idx + 1;
    end
end

% 如果原始图像被旋转，将其旋转回原始方向
if m < n
    img1 = rot90(img1, -1);
end

end

