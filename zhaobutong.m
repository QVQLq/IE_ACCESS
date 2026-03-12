function sum = zhaobutong(P1,P2)
[m,n]=size(P1);

sum=0;
for i=1:m

        for j=1:n
            if (P1(i,j)==P2(i,j))
            else 
                sum=sum+1;
            end
        end

end

end

