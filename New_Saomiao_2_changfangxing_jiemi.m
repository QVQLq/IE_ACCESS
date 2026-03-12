function jiemi = New_Saomiao_2_changfangxing_jiemi(Line, a, b)
    [m, n] = deal(max(a, b), min(a, b));
    jiemi = zeros(m, n);

    Line1_length = (n*n - n*(m-n+1)) / 2;
    Line1 = Line(1:Line1_length);
    Line2_start = Line1_length + 1;
    Line2_end = Line2_start + (m-n+1)*n - 1;
    Line2 = Line(Line2_start:Line2_end);
    Line3 = Line(Line2_end+1:end);

    % 重构 Line1
    idx = 1;
    for i = 1:(n-2)/2+1
        for j = 1:4*(i-1)+1
            x = (n - 2*(i-1) + floor(j/2));
            y = 2 + floor((j-1)/4)*2 - mod(j,2);
            if x <= m && y <= n && idx <= length(Line1)
                jiemi(x, y) = Line1(idx);
                idx = idx + 1;
            end
        end
    end

    % 重构 Line2
    idx = 1;
    for i = 1:m-n+1
        for j = 1:n
            x = j;
            y = j + (i-1);
            if x <= m && y <= n && idx <= length(Line2)
                jiemi(x, y) = Line2(idx);
                idx = idx + 1;
            end
        end
    end

    % 重构 Line3
    idx = 1;
    for i = (n-2)/2+1 : -1 : 1
        for j = 1:4*(i-1)+1
            x = 2 + floor((j-1)/4)*2 - mod(j,2);
            y = (n - 2*(i-1) + floor(j/2)) + (m-n);
            if x <= m && y <= n && idx <= length(Line3)
                jiemi(x, y) = Line3(idx);
                idx = idx + 1;
            end
        end
    end

    % 如果需要，旋转图像
    if a > b
        jiemi = rot90(jiemi, -1);
    end
end

