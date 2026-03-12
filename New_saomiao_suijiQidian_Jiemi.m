function img1 = New_saomiao_suijiQidian_Jiemi(term2, Line, n)
    Line1 = Zhongjiandian_Wangfan_Jiemi(term2, Line, n*n);
    img1 = New_Saomiao_Jiemi(Line1, n);
end

function Line1 = Zhongjiandian_Wangfan_Jiemi(zhongdian, Line, jieshu)
    line_s1 = zeros(1, zhongdian);   % term-1
    line_s2 = zeros(1, jieshu - zhongdian);   % size*size-term+1
    min_val = min(zhongdian, jieshu - zhongdian);

    for i = 1:min_val
        line_s1(i) = Line(2*(i-1)+1);
    end
    for i = 1:min_val
        line_s2(i) = Line(2*i);
    end

    if zhongdian > jieshu - zhongdian
        line_s1(min_val+1:zhongdian) = Line(2*min_val+1:jieshu);
    else
        line_s2(min_val+1:jieshu-zhongdian) = Line(2*min_val+1:jieshu);
    end

    line_s1 = fliplr(line_s1);
    Line1 = horzcat(line_s1, line_s2);
    Line1 = uint8(Line1);
end

function [img] = New_Saomiao_Jiemi(Line, n)
% Initialize img with zeros
img = zeros(n, n);

% Reconstruct Line1, Line2, and Line3 from Line
len_line1 = (n*n - n) / 2;
len_line2 = n;


Line1 = Line(1:len_line1);
Line2 = Line(len_line1 + 1:len_line1 + len_line2);
Line3 = Line(len_line1 + len_line2 + 1:end);

% Reconstruct Line1

for i = 1:(n-2)/2 + 1
    for j = 1:4*(i-1) + 1
        x = (n - 2*(i-1) + floor(j/2));
        y = 2 + floor((j-1)/4) * 2 - mod(j, 2);
        img(x, y) = Line1( (4*(i-1)-2)*(i-1)/2 +j);
    end
end

% Reconstruct Line2

for i = 1:n
    img(i,i) = Line2(i);

end

% Reconstruct Line3
k = 1;
for i = (n-2)/2 + 1:-1:1
    for j = 1:4*(i-1) + 1
        y = (n - 2*(i-1) + floor(j/2));
        x = 2 + floor((j-1)/4) * 2 - mod(j, 2);
        img(x, y) = Line3(k);
        k = k + 1;
    end
end

end

function y = Mod_4_xiangxia(j)
    y = floor((j-1)/4);
end
