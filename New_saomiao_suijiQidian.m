function Line = New_saomiao_suijiQidian(term2,img1,n)


Line1=zeros(1,(n*n-n)/2);

for i=1:(n-2)/2+1
for j=1:4*(i-1)+1

    x=(n-2*(i-1)+floor(j/2));
    y=2+floor((j-1)/4)*2-mod(j,2);
    Line1( (4*(i-1)-2)*(i-1)/2 +j)=img1(x,y);

end
end


    Line2=zeros(1,n);
    for i=1:n
        Line2(i)=img1(i,i);
    end





Line3 = zeros(1, (n*n-n)/2);
for i = (n-2)/2+1 : -1 : 1
    for j = 1 : 4*(i-1)+1
        
        y = (n-2*(i-1) + floor(j/2));
        x = 2 + floor((j-1)/4)*2 - mod(j, 2);

        Line3((4*(n-2)/2+1+4*i+1)*((n-2)/2+1-i)/2+j) = img1(x, y); 

    end
end





Line=horzcat(Line1,Line2,Line3);


line_s1 = fliplr(Line(1:term2));
line_s2 = Line(term2+1:n*n);


len1 = length(line_s1);   
len2 = length(line_s2);
Line_new = zeros(1, n*n) + NaN;

if len1 > len2
    for k = 1:len2
        Line_new(2*(k-1)+1) = line_s1(k);
        Line_new(2*(k-1)+2) = line_s2(k);
    end
    Line_new = horzcat(Line_new, line_s1(len1-(len1-len2)+1:len1));
else
    for k = 1:len1
        Line_new(2*(k-1)+1) = line_s1(k);
        Line_new(2*(k-1)+2) = line_s2(k);
    end
    Line_new = horzcat(Line_new, line_s2(len2-(len2-len1)+1:len2));
end

Line_new(isnan(Line_new)) = [];
Line = Line_new;

end




