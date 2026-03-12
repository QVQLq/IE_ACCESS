function [outputArg1] = jian(inputArg1,inputArg2)

for i=1:3
for k=1:512

for j=1:512
outputArg1(k,j,i)=abs(inputArg1(k,j,i)-inputArg2(k,j,i));
end

end

end

end

