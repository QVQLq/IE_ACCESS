function Line= New_Saomiao_2(img,n)



k=1;
Line1=zeros(1,(n*n-n)/2);

for i=1:(n-2)/2+1
for j=1:4*(i-1)+1

    x=(n-2*(i-1)+floor(j/2));

    if mod(j,2)==1
    
        output = Mod_4_xiangxia(j);
            y=1+output*2;
    else
        output = Mod_4_xiangxia(j);
             y=2+output*2;
    end


    Line1(k)=img(x,y);
    k=k+1;
end

end


    Line2=zeros(1,n);
    k=1;
    for i=1:n
        x=i;
        y=i;
   
        Line2(k)=img(x,y);
        k=k+1;
    end






k=1;
Line3=zeros(1,(n*n-n)/2);


for i=(n-2)/2+1 :-1:1   %2-1
for j=1:4*(i-1)+1        %1-5 1-1
     
    y=(n-2*(i-1)+floor(j/2));

    if mod(j,2)==1   %1 1 3
           output = Mod_4_xiangxia(j);

            x=1+output*2;

      
    else     %2 2
            output = Mod_4_xiangxia(j);
            x=2+output*2;
    end

   % Line(1,k)=x;
    %Line(2,k)=y;
   Line3(k)=img(x,y);
    k=k+1;


end
end


Line=horzcat(Line1,Line2,Line3);


end


function y = Mod_4_xiangxia(x)
    y = floor((x-1)/4);
end




