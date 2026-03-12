function Line = New_Saomiao_2_changfangxing(img1)
% 
% [a, b] = size(img1);
% if a > b %m大于n
%     m = a;
%     n = b;
%     img1 = rot90(img1, 1);
% else
%     m = b;
%     n = a;
% end


[a, b] = size(img1);
[m, n] = deal(max(a, b), min(a, b));

if a > b %m大于n
    img1 = rot90(img1, 1);
end

Line1=zeros(1,(n*n-n*(m-n+1))/2);

for i=1:(n-2)/2+1
for j=1:4*(i-1)+1

    x=(n-2*(i-1)+floor(j/2));
    y=2+floor((j-1)/4)*2-mod(j,2);
    Line1( (4*(i-1)-2)*(i-1)/2 +j)=img1(x,y);

end
end


Line2 = zeros(1, (m-n+1)*n); % 预分配空间
for i = 1:m-n+1
    for j = 1:n
        y = j + (i-1);
        x = j;
        Line2((i-1)*(n)+j) = img1(x, y);
    end
end



Line3 = zeros(1,(n*n-n*(m-n+1))/2);
for i = (n-2)/2+1 : -1 : 1
    for j = 1 : 4*(i-1)+1
        y = (n-2*(i-1) + floor(j/2))+(m-n);
        x = 2 + floor((j-1)/4)*2 - mod(j, 2);
        Line3((4*(n-2)/2+1+4*i+1)*((n-2)/2+1-i)/2+j) = img1(x, y); 

    end
end

Line = horzcat(Line1, Line2, Line3);



end


